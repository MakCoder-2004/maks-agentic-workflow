#!/usr/bin/env python3
"""Install the agreed original-skill combination, without whole upstream catalogs.

No network, package installation, global configuration, hooks or skill rewriting.
Use a trusted, idle project filesystem with normal user rights: pathname checks
are not an OS sandbox against adversarial directory swaps during I/O.
Python 3.10+. Run with --help or --list before choosing a target project.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = '.maks-agentic-workflow'
STATE = f'{PRIVATE}/install.json'
SETUP_SKILL = 'setup-agentic-workflow'
START = b'<!-- maks-agentic-workflow:start -->'
END = b'<!-- maks-agentic-workflow:end -->'
HOSTS = ('pi', 'codex', 'cursor', 'claude-code')
SKILL_ROOTS = ('.agents/skills', '.claude/skills', '.cursor/skills', '.pi/skills', '.codex/skills')


class InstallError(Exception):
    """A failed precondition; no conflict is resolved by silently overwriting it."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n').encode('utf-8')


def relative_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value or '\0' in value:
        raise InstallError(f'Unsafe relative installation path: {value!r}')
    return path


def linked(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        return bool(getattr(path.lstat(), 'st_file_attributes', 0) & 0x400)
    except FileNotFoundError:
        return False


def safe_path(project: Path, relative: str) -> Path:
    """Reject links observed now; this is not race-proof directory-handle I/O."""
    parts = relative_path(relative).parts
    current = project
    for index, part in enumerate(parts):
        current = current / part
        if linked(current):
            raise InstallError(f'Refusing a symlink/junction/reparse path: {current}')
        if current.exists() and index < len(parts) - 1 and not current.is_dir():
            raise InstallError(f'Expected a directory: {current}')
    if not current.resolve().is_relative_to(project):
        raise InstallError(f'Installation path escapes the project: {relative}')
    return current


def project_path(value: Path | str) -> Path:
    project = Path(value).expanduser().resolve()
    archive_markers = ('scripts/install.py', 'workflow/selection.json', 'upstream/checksums.json')
    if (project == ROOT or project.is_relative_to(ROOT / 'upstream')
            or all((project / marker).is_file() for marker in archive_markers)):
        raise InstallError('Choose a consuming project, not this source/archive repository.')
    if project == Path(project.anchor) or project == Path.home().resolve():
        raise InstallError('Choose a project directory, not a drive root or your home directory.')
    if project.exists() and not project.is_dir():
        raise InstallError(f'The project path is not a directory: {project}')
    return project


@dataclass(frozen=True)
class FileSpec:
    data: bytes
    mode: int = 0o644
    source: str | None = None


@dataclass
class Bundle:
    host: str
    files: dict[str, FileSpec]
    registry: dict
    catalog_names: set[str]
    retired_files: dict[str, FileSpec] = field(default_factory=dict)


@dataclass(frozen=True)
class Change:
    relative: str
    data: bytes | None
    mode: int
    before: bytes | None
    before_mode: int | None


@dataclass
class Plan:
    project: Path
    bundle: Bundle
    changes: list[Change]
    warnings: list[str]
    state: dict


def source_data(path: Path, hashes: dict[str, str]) -> bytes:
    if linked(path) or not path.is_file():
        raise InstallError(f'Missing or linked source resource: {path}')
    relative = path.relative_to(ROOT).as_posix()
    data = path.read_bytes()
    if hashes.get(relative) != digest(data):
        raise InstallError(f'Original source checksum mismatch: {relative}')
    return data


def original_name(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    match = re.search(r'^name:\s*[\"\']?([a-z0-9]+(?:-[a-z0-9]+)*)[\"\']?\s*$', text, re.M)
    if not text.startswith('---\n') or not match:
        raise InstallError(f'Cannot read original skill identity: {path}')
    return match.group(1)


def build_bundle(host: str) -> Bundle:
    if host not in HOSTS:
        raise InstallError(f'Unsupported host: {host}')
    selection = json.loads((ROOT / 'workflow/selection.json').read_text(encoding='utf-8'))
    lock = json.loads((ROOT / 'sources.lock.json').read_text(encoding='utf-8'))
    hashes = json.loads((ROOT / 'upstream/checksums.json').read_text(encoding='utf-8'))
    executable = set(lock['executable_files'])
    sources = {item['id']: item for item in lock['sources']}
    indexes = {}
    catalog_names = set()
    for source in ('matt', 'pstack', 'addy', 'cursor-team-kit'):
        index = {}
        for path in sorted((ROOT / sources[source]['local_path'] / 'skills').rglob('SKILL.md')):
            name = original_name(path)
            if name in index:
                raise InstallError(f'Duplicate upstream name in {source}: {name}')
            index[name] = path.parent
            catalog_names.add(name)
        indexes[source] = index
    own_setup = ROOT / 'workflow/skills' / SETUP_SKILL
    if original_name(own_setup / 'SKILL.md') != SETUP_SKILL:
        raise InstallError('Invalid combined setup skill identity.')
    indexes['workflow'] = {SETUP_SKILL: own_setup}
    catalog_names.add(SETUP_SKILL)

    visible = {}
    selected = {}
    for section in ('entry_points', 'on_demand'):
        for source, names in selection[section].items():
            if source not in indexes:
                raise InstallError(f'Unknown source in selection: {source}')
            for name in names:
                if name not in indexes[source]:
                    raise InstallError(f'Missing selected original: {source}/{name}')
                if name in selected:
                    raise InstallError(f'Duplicate selected original identity: {name}')
                selected[name] = source
                if section == 'entry_points':
                    visible[name] = source
    if selection.get('include_pstack_principles'):
        for name in sorted(indexes['pstack']):
            if name.startswith('principle-'):
                if name in selected:
                    raise InstallError(f'Duplicate principle: {name}')
                selected[name] = 'pstack'
    if len(visible) != 22:
        raise InstallError('The reviewed selection must advertise 21 original entries plus combined setup.')

    files: dict[str, FileSpec] = {}
    public_root = '.claude/skills' if host == 'claude-code' else '.agents/skills'
    registry = {
        'format': 1,
        'profile': selection['name'],
        'host': host,
        'entry_points': list(visible),
        'skills': {},
        'sources': {},
        'roles': {},
        'external_dependencies': ['frontend-design', 'ui-ux-pro-max'],
    }

    def put(relative: str, spec: FileSpec) -> None:
        relative_path(relative)
        if relative in files:
            raise InstallError(f'Conflicting payload resources: {relative}')
        files[relative] = spec

    reference_roots = {'matt': indexes['matt']['setup-matt-pocock-skills'], 'pstack': indexes['pstack']['setup-pstack']}

    def file_spec(path: Path) -> FileSpec:
        origin = path.relative_to(ROOT).as_posix()
        if path.is_relative_to(own_setup):
            if linked(path) or not path.is_file():
                raise InstallError(f'Missing or linked integration resource: {path}')
            data = path.read_bytes()
            parts = path.relative_to(own_setup).parts
            if len(parts) > 2 and parts[0] == 'references' and parts[1] in reference_roots:
                source = parts[1]
                tail = Path(*parts[2:])
                original = (ROOT / sources[source]['local_path'] / 'LICENSE' if tail.as_posix() == 'LICENSE'
                            else reference_roots[source] / ('SKILL.md' if tail.as_posix() == 'SETUP.txt' else tail))
                if data != source_data(original, hashes):
                    raise InstallError(f'Bundled setup reference differs from its pinned original: {path}')
                origin = original.relative_to(ROOT).as_posix()
        else:
            data = source_data(path, hashes)
        return FileSpec(data, 0o755 if origin in executable else 0o644, origin)

    def copy_file(path: Path, relative: str) -> None:
        put(relative, file_spec(path))

    def copy_tree(folder: Path, destination: str) -> list[str]:
        copied = []
        for path in sorted(folder.rglob('*')):
            if linked(path):
                raise InstallError(f'Linked resource in source tree: {path}')
            if path.is_file():
                relative = path.relative_to(folder).as_posix()
                copy_file(path, f'{destination}/{relative}')
                copied.append(relative)
        return copied

    def attribute_spec(paths: list[str] | None = None) -> FileSpec:
        text = '* -text\n' if paths is None else ''.join(f'{json.dumps(p)} -text\n' for p in sorted(paths))
        return FileSpec(text.encode('utf-8'))

    def attributes(destination: str, paths: list[str] | None = None) -> None:
        put(f'{destination}/.gitattributes', attribute_spec(paths))

    retired_files = {}
    for source, folder in reference_roots.items():
        name = folder.name
        source_root = ROOT / sources[source]['local_path']
        canonical = f'{PRIVATE}/originals/{source}/{folder.relative_to(source_root).as_posix()}'
        paths = []
        for path in sorted(folder.rglob('*')):
            if path.is_file():
                relative = path.relative_to(folder).as_posix()
                paths.append(relative)
                spec = file_spec(path)
                retired_files[f'{canonical}/{relative}'] = spec
                if source == 'matt':
                    retired_files[f'{public_root}/{name}/{relative}'] = spec
        if source == 'matt':
            retired_files[f'{public_root}/{name}/.gitattributes'] = attribute_spec(paths)

    for name, source in selected.items():
        folder = indexes[source][name]
        source_root = ROOT / 'workflow' if source == 'workflow' else ROOT / sources[source]['local_path']
        canonical = (f'{PRIVATE}/integration/{folder.relative_to(source_root).as_posix()}' if source == 'workflow'
                     else f'{PRIVATE}/originals/{source}/{folder.relative_to(source_root).as_posix()}')
        copy_tree(folder, canonical)
        discovery = None
        if name in visible:
            discovery = f'{public_root}/{name}'
            paths = copy_tree(folder, discovery)
            attributes(discovery, paths)
        registry['skills'][name] = {
            'source': source,
            'kind': 'integration' if source == 'workflow' else 'upstream',
            'canonical_path': f'{canonical}/SKILL.md',
            'discovery_path': f'{discovery}/SKILL.md' if discovery else None,
        }

    for source in sorted(set(selected.values()) - {'workflow'}):
        info = sources[source]
        copy_file(ROOT / info['local_path'] / 'LICENSE', f'{PRIVATE}/originals/{source}/LICENSE')
        registry['sources'][source] = {
            'repository': info['repository'],
            'revision': info['revision'],
            'subdirectory': info['subdirectory'],
        }
    attributes(PRIVATE)
    references = ROOT / sources['addy']['local_path'] / 'references'
    copy_tree(references, f'{PRIVATE}/originals/addy/references')
    public_references = f'{PurePosixPath(public_root).parent}/references'
    ref_paths = copy_tree(references, public_references)
    attributes(public_references, ref_paths)

    pstack = ROOT / sources['pstack']['local_path']
    copy_file(pstack / 'docs/harness/claude-code.md', f'{PRIVATE}/originals/pstack/docs/harness/claude-code.md')
    role_directory = {'cursor': '.cursor/agents', 'claude-code': '.claude/agents'}.get(host)
    for role in ('poteto-agent', 'comment-sicko'):
        original = pstack / f'agents/{role}.md'
        private_role = f'{PRIVATE}/originals/pstack/agents/{role}.md'
        copy_file(original, private_role)
        native = f'{role_directory}/{role}.md' if role_directory else None
        if native:
            copy_file(original, native)
        registry['roles'][role] = {'canonical_path': private_role, 'native_path': native}
    if role_directory:
        attributes(role_directory, ['poteto-agent.md', 'comment-sicko.md'])

    setup_folder = str(PurePosixPath(registry['skills'][SETUP_SKILL]['canonical_path']).parent)
    registry['setup_references'] = {source: f'{setup_folder}/references/{source}/SETUP.txt' for source in reference_roots}
    counts = {source: sum(value == source for value in visible.values()) for source in set(visible.values())}
    registry['counts'] = {'entry_points': len(visible), 'on_demand': len(selected) - len(visible),
                          'total_original_skills': sum(source != 'workflow' for source in selected.values()),
                          'integration_skills': sum(source == 'workflow' for source in selected.values()),
                          'entry_points_by_source': counts}
    put(f'{PRIVATE}/registry.json', FileSpec(json_bytes(registry)))
    rows = []
    for name, source in visible.items():
        phase = 'One-time setup' if source == 'workflow' else 'Plan / design / handoff' if source == 'matt' else 'Build / test / PR' if source == 'pstack' else 'Relevant lifecycle gate'
        rows.append(f'| {phase} | `{name}` | {source} |')
    invocation = '/skill:poteto-mode' if host == 'pi' else '$poteto-mode' if host == 'codex' else '/poteto-mode'
    notes = {
        'pi': 'Files are laid out for Pi\'s documented .agents/skills discovery; verify discovery in your host version/configuration. Use /skill:name. Native subagents require an installed extension; original role files are supplied privately, not falsely registered as a built-in Pi feature.',
        'codex': 'Files are laid out for Codex\'s documented .agents/skills discovery; verify discovery in your host version/configuration. Use $name or its skill selector. Native custom-agent configuration is not changed; role files are supplied privately. Do not assume Cursor Task fields/model slugs are Codex APIs.',
        'cursor': 'Files are laid out for Cursor\'s documented .agents/skills discovery; verify discovery in your host version/configuration. Use /name. The two original agent files are also installed under .cursor/agents. Models, cloud agents, MCPs, browsers and credentials still require actual supported setup.',
        'claude-code': 'Files are laid out for Claude Code\'s documented .claude/skills discovery; verify discovery in your host version/configuration. Use /name. The two original roles are installed under .claude/agents, without a plugin namespace. Read originals/pstack/docs/harness/claude-code.md for the upstream Task -> Agent and model/tool mapping, but use this project\'s plain poteto-agent/comment-sicko names rather than pstack: plugin-prefixed names. No full plugins are loaded.',
    }
    text = (ROOT / 'workflow/installed-guide.md').read_text(encoding='utf-8')
    replacements = {'HOST': host, 'ENTRY_COUNT': str(len(visible)), 'HELPER_COUNT': str(len(selected) - len(visible)), 'ENTRY_ROWS': '\n'.join(rows), 'POTETO_INVOKE': invocation, 'SETUP_INVOKE': invocation.replace('poteto-mode', SETUP_SKILL), 'HOST_NOTES': notes[host]}
    for key, value in replacements.items():
        text = text.replace('{{' + key + '}}', value)
    if '{{' in text:
        raise InstallError('An installed-guide template variable is unresolved.')
    put(f'{PRIVATE}/WORKFLOW.md', FileSpec(text.encode('utf-8')))
    notice = ('# Skill attribution\n\nNo upstream skill bodies or identities have been rewritten. '
              'setup-agentic-workflow is the one integration skill explicitly requested by the user; '
              'it coordinates the unchanged original setups and is not an upstream Addy/Matt/pstack skill.\n\n')
    for source, info in registry['sources'].items():
        notice += f'- {source}: {info["repository"]}, revision `{info["revision"]}`. [Original license](originals/{source}/LICENSE).\n'
    put(f'{PRIVATE}/NOTICE.md', FileSpec(notice.encode('utf-8')))
    return Bundle(host, files, registry, catalog_names, retired_files)


def instruction_block(bundle: Bundle) -> bytes:
    text = f'''{START.decode()}
## Maks Agentic Workflow: original skills, selected scope

For one-time project configuration, invoke `setup-agentic-workflow`; it coordinates Matt/pstack setup and Addy constraints/context, creates or preserves canonical AGENTS.md, and asks before global/external changes. If an upstream instruction suggests the retired setup-matt-pocock-skills or setup-pstack command, use setup-agentic-workflow instead; their instructions are bundled references, not installed skills. Keep setup additions outside this installer-owned marker block.

Read `{PRIVATE}/WORKFLOW.md` when using this workflow. Matt owns discovery, glossary/ADRs, `to-spec` and `to-tickets`; original `poteto-mode` owns implementation, per-ticket tests/retests and PR preparation; relevant Addy skills provide quality/security/runtime/CI/CD/observability/migration/release checks. Do not run competing implementation controllers or rewrite the approved spec/ticket graph.

Only {bundle.registry['counts']['entry_points']} entry skills are advertised. Resolve originals and on-demand helpers through `{PRIVATE}/registry.json`: read the exact `canonical_path` relative to this project before following relative resource/sibling-skill paths. Helpers are deliberately not registered commands. If an upstream Skill-tool request names a hidden helper, read its canonical original rather than invoking an unrelated global namesake. Load only the helper needed, not the entire registry's skill bodies. Pass the absolute canonical poteto-mode path to every delegate. Original role definitions and host notes are in the runbook; never fabricate absent tools, independent reviewers or model support.

Approve scope/design/tickets before production implementation. Test and apply relevant Addy checks for each slice before dependent work; missing/failed/inconclusive checks are not passes. Local task edits/tests/ordinary commits may follow the approved scope. Publishing issues/labels, pushes/PRs, merge, deployment and destructive changes need their own explicit grants. Preserve unrelated work and useful rationale comments; propose wider redesign separately. UI requires the actual external frontend-design and ui-ux-pro-max skills, not homemade substitutes.
{END.decode()}'''
    return text.encode('utf-8')


def read_state(project: Path) -> dict | None:
    path = safe_path(project, STATE)
    if not path.exists():
        return None
    if not path.is_file():
        raise InstallError(f'Expected an installation manifest file: {path}')
    try:
        state = json.loads(path.read_text(encoding='utf-8'))
        if state['format'] != 1 or state['installer'] != 'maks-agentic-workflow' or state['host'] not in HOSTS:
            raise ValueError('unsupported installation identity/format/host')
        if not isinstance(state['files'], dict) or not isinstance(state['instructions'], dict):
            raise ValueError('invalid file/instruction records')
        for relative, record in state['files'].items():
            relative_path(relative)
            if not isinstance(record['owned'], bool) or not re.fullmatch(r'[a-f0-9]{64}', record['sha256']):
                raise ValueError('invalid file ownership/checksum')
            if type(record.get('mode')) is not int or record['mode'] not in (0o644, 0o755):
                raise ValueError('invalid file permission record')
        expected_instruction = 'CLAUDE.md' if state['host'] == 'claude-code' else 'AGENTS.md'
        if set(state['instructions']) != {expected_instruction}:
            raise ValueError('missing or unexpected managed instruction record')
        for relative, checksum in state['instructions'].items():
            if relative not in ('AGENTS.md', 'CLAUDE.md') or not re.fullmatch(r'[a-f0-9]{64}', checksum):
                raise ValueError('invalid managed instruction record')
        return state
    except (KeyError, TypeError, ValueError) as error:
        raise InstallError(f'Invalid existing installation manifest: {error}') from error


def read_existing(project: Path, relative: str) -> tuple[bytes | None, int | None]:
    path = safe_path(project, relative)
    if not path.exists():
        return None, None
    if not path.is_file():
        raise InstallError(f'Expected a file, refusing to replace: {path}')
    return path.read_bytes(), stat.S_IMODE(path.stat().st_mode)


def managed_slice(data: bytes) -> tuple[int, int] | None:
    starts, ends = data.count(START), data.count(END)
    if starts == ends == 0:
        return None
    if starts != 1 or ends != 1 or data.index(END) < data.index(START):
        raise InstallError('Malformed or duplicate workflow instruction markers.')
    return data.index(START), data.index(END) + len(END)


def existing_skill_names(project: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for root in SKILL_ROOTS:
        folder = safe_path(project, root)
        if not folder.exists():
            continue
        if not folder.is_dir():
            raise InstallError(f'Expected a skill directory: {folder}')
        for directory, subdirs, names in os.walk(folder, followlinks=False):
            current = Path(directory)
            for subdir in subdirs:
                if linked(current / subdir):
                    raise InstallError(f'Cannot safely inspect linked skill directory: {current / subdir}')
            if 'SKILL.md' in names:
                file = current / 'SKILL.md'
                if linked(file):
                    raise InstallError(f'Cannot safely inspect linked skill: {file}')
                name = original_name(file)
                result.setdefault(name, []).append(current.relative_to(project).as_posix())
    return result


def validate_inventory(state: dict, bundle: Bundle, allow_setup_addition: bool = False) -> set[str]:
    current = bundle.registry['counts']
    previous = dict(current, entry_points=current['entry_points'] + 1,
                    on_demand=current['on_demand'] + 1, total_original_skills=current['total_original_skills'] + 2)
    previous['entry_points_by_source'] = dict(current['entry_points_by_source'])
    previous['entry_points_by_source']['matt'] += 1
    original = dict(previous)
    original.pop('integration_skills')
    original['entry_points'] -= 1
    original['entry_points_by_source'] = {key: value for key, value in previous['entry_points_by_source'].items() if key != 'workflow'}
    prior_version = 2 if state.get('counts') == previous else 1 if state.get('counts') == original else 0
    upgrading = allow_setup_addition and prior_version != 0
    if state.get('profile') != bundle.registry['profile'] or (state.get('counts') != current and not upgrading):
        raise InstallError('Installed profile/count records differ; rerun the current installer for the supported setup update or review the metadata.')
    actual, expected = set(state['files']), set(bundle.files)
    removed, missing = actual - expected, expected - actual
    setup = bundle.registry['skills'][SETUP_SKILL]
    setup_roots = tuple(str(PurePosixPath(setup[key]).parent) + '/' for key in ('canonical_path', 'discovery_path'))
    reference_roots = tuple(root + 'references/' for root in setup_roots)
    additions = {path for path in expected if path.startswith(setup_roots if prior_version == 1 else reference_roots)}
    if removed:
        if not upgrading or removed != set(bundle.retired_files):
            raise InstallError('Unsupported obsolete managed files; only the exact standalone-setup retirement is allowed.')
    elif upgrading:
        raise InstallError('The prior setup inventory is not the exact supported setup upgrade.')
    if missing and not (upgrading and missing == additions):
        raise InstallError('The installation inventory is incomplete or the selection changed; refusing to silently adopt missing ownership records.')
    if upgrading and missing != additions:
        raise InstallError('The prior setup inventory is not the exact supported setup upgrade.')
    for relative in actual:
        spec = bundle.retired_files[relative] if relative in removed else bundle.files[relative]
        record = state['files'][relative]
        if record.get('source') != spec.source or record['mode'] != spec.mode:
            raise InstallError(f'Changed installation provenance/permission record: {relative}')
        if relative in removed and (not record['owned'] or record['sha256'] != digest(spec.data)):
            raise InstallError(f'Refusing to remove unowned or changed standalone setup file: {relative}')
    return removed


def prepare_install(value: Path | str, host: str | None = None) -> Plan:
    project = project_path(value)
    old = read_state(project)
    host = host or (old['host'] if old else 'pi')
    if old and old['host'] != host:
        raise InstallError(f'This project is already installed for {old["host"]}; refusing duplicate cross-host views. No files changed.')
    bundle = build_bundle(host)
    old_files = old['files'] if old else {}
    removed = validate_inventory(old, bundle, allow_setup_addition=True) if old else set()
    names = existing_skill_names(project)
    for name in ('setup-matt-pocock-skills', 'setup-pstack'):
        for folder in names.get(name, []):
            if f'{folder}/SKILL.md' not in removed:
                raise InstallError(f'Unmanaged standalone setup is still discoverable: {folder}. Remove it deliberately; it will not be overwritten or deleted.')
    for name in bundle.registry['entry_points']:
        expected = str(PurePosixPath(bundle.registry['skills'][name]['discovery_path']).parent)
        others = [path for path in names.get(name, []) if path != expected]
        if others:
            raise InstallError(f'Duplicate skill discovery for {name}: {", ".join(others)}. Choose one installation; nothing was overwritten.')
    warnings = ['Global skills/plugins are unchanged and may still contribute context. External UI skills are not downloaded.']
    extra = sorted((set(names) & bundle.catalog_names) - set(bundle.registry['entry_points'])
                   - {'setup-matt-pocock-skills', 'setup-pstack'})
    if extra:
        warnings.append('Pre-existing upstream/helper skills remain discoverable and are not removed: ' + ', '.join(extra))
    records = {}
    changes = []
    for relative in sorted(removed):
        before, mode = read_existing(project, relative)
        previous = old_files[relative]
        if before is None or digest(before) != previous['sha256'] or (os.name != 'nt' and mode != previous['mode']):
            raise InstallError(f'Locally changed or missing standalone setup file: {relative}. Refusing removal.')
        changes.append(Change(relative, None, previous['mode'], before, mode))
    for relative, spec in sorted(bundle.files.items()):
        before, mode = read_existing(project, relative)
        previous = old_files.get(relative)
        if previous and (before is None or digest(before) != previous['sha256']):
            raise InstallError(f'Locally changed or missing installed file: {relative}. Refusing to overwrite it.')
        if before is not None and not previous and before != spec.data:
            raise InstallError(f'Existing project file conflicts with this installation: {relative}')
        owned = previous['owned'] if previous else before is None
        if before is not None and not owned and before != spec.data:
            raise InstallError(f'Reused user-owned file cannot be updated automatically: {relative}')
        mode_change = before is not None and os.name != 'nt' and mode != spec.mode
        if mode_change and not owned:
            raise InstallError(f'Reused user-owned file has different permissions: {relative}')
        if before != spec.data or mode_change:
            changes.append(Change(relative, spec.data, spec.mode, before, mode))
        records[relative] = {'sha256': digest(spec.data), 'mode': spec.mode, 'owned': owned, 'source': spec.source}

    instruction_file = 'CLAUDE.md' if host == 'claude-code' else 'AGENTS.md'
    before, mode = read_existing(project, instruction_file)
    text = before or b''
    span = managed_slice(text)
    expected = old['instructions'].get(instruction_file) if old else None
    block = instruction_block(bundle)
    if expected:
        if span is None or digest(text[span[0]:span[1]]) != expected:
            raise InstallError(f'Locally changed or missing managed workflow block in {instruction_file}.')
        updated = text[:span[0]] + block + text[span[1]:]
    else:
        if span is not None:
            raise InstallError(f'Unowned workflow markers already exist in {instruction_file}.')
        updated = text + (b'\n\n' if text else b'') + block + b'\n'
    if before != updated:
        changes.append(Change(instruction_file, updated, mode if mode is not None else 0o644, before, mode))
    state = {
        'format': 1,
        'installer': 'maks-agentic-workflow',
        'host': host,
        'profile': bundle.registry['profile'],
        'counts': bundle.registry['counts'],
        'files': records,
        'instructions': {instruction_file: digest(block)},
    }
    before_state, state_mode = read_existing(project, STATE)
    data = json_bytes(state)
    if before_state != data:
        changes.append(Change(STATE, data, 0o644, before_state, state_mode))
    return Plan(project, bundle, changes, warnings, state)


def atomic_write(path: Path, data: bytes, mode: int) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix='.maks-install-', dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(data)
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def apply_plan(plan: Plan) -> None:
    completed = []
    created_directories = []
    try:
        for change in plan.changes:
            path = safe_path(plan.project, change.relative)
            current, current_mode = read_existing(plan.project, change.relative)
            if current != change.before or current_mode != change.before_mode:
                raise InstallError(f'Project changed after preflight: {change.relative}')
            if change.data is None:
                path.unlink()
                completed.append((change, None))
                continue
            missing = []
            directory = path.parent
            while not directory.exists():
                missing.append(directory)
                directory = directory.parent
            for directory in reversed(missing):
                directory.mkdir()
                created_directories.append(directory)
            safe_path(plan.project, change.relative)
            atomic_write(path, change.data, change.mode)
            completed.append((change, stat.S_IMODE(path.stat().st_mode)))
    except BaseException as error:
        preserved = []
        for change, written_mode in reversed(completed):
            try:
                current, mode = read_existing(plan.project, change.relative)
                if current != change.data or mode != written_mode:
                    preserved.append(change.relative)
                    continue
                path = safe_path(plan.project, change.relative)
                if change.before is None:
                    path.unlink(missing_ok=True)
                else:
                    atomic_write(path, change.before, change.before_mode if change.before_mode is not None else 0o644)
            except (InstallError, OSError):
                preserved.append(change.relative)
        for directory in reversed(created_directories):
            try:
                if not linked(directory):
                    directory.rmdir()
            except OSError:
                pass
        if preserved:
            raise InstallError('Installation failed; concurrently changed or inaccessible paths were left untouched during rollback: '
                               + ', '.join(preserved) + '. Inspect the target before retrying. Original error: ' + str(error)) from error
        raise
    empty_candidates = set()
    for change in plan.changes:
        if change.data is None:
            parent = PurePosixPath(change.relative).parent
            while parent.name not in ('skills', 'originals'):
                empty_candidates.add(parent.as_posix())
                if parent.name in ('setup-matt-pocock-skills', 'setup-pstack'):
                    break
                parent = parent.parent
    for relative in sorted(empty_candidates, key=lambda value: len(PurePosixPath(value).parts), reverse=True):
        try:
            safe_path(plan.project, relative).rmdir()
        except (InstallError, OSError):
            pass


def check_installation(value: Path | str) -> dict:
    project = project_path(value)
    state = read_state(project)
    if not state:
        raise InstallError('No managed workflow installation exists in this project.')
    validate_inventory(state, build_bundle(state['host']))
    for relative, record in state['files'].items():
        data, mode = read_existing(project, relative)
        if data is None or digest(data) != record['sha256']:
            raise InstallError(f'Missing or modified installed file: {relative}')
        if os.name != 'nt' and mode != record['mode']:
            raise InstallError(f'Changed installed file permissions: {relative}')
    for relative, checksum in state['instructions'].items():
        data, _ = read_existing(project, relative)
        span = managed_slice(data or b'')
        if span is None or digest(data[span[0]:span[1]]) != checksum:
            raise InstallError(f'Missing or modified managed workflow block: {relative}')
    registry = json.loads(safe_path(project, f'{PRIVATE}/registry.json').read_text(encoding='utf-8'))
    names = existing_skill_names(project)
    for retired in ('setup-matt-pocock-skills', 'setup-pstack'):
        if retired in names:
            raise InstallError(f'Retired standalone setup is still discoverable: {retired}')
    for name in registry['entry_points']:
        expected = str(PurePosixPath(registry['skills'][name]['discovery_path']).parent)
        if names.get(name) != [expected]:
            raise InstallError(f'Duplicate or missing discovery entry: {name}')
    return state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', '--target', default='.', help='Target project (default: current directory).')
    parser.add_argument('--host', choices=HOSTS, help='Host (default: existing installation host, otherwise pi).')
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('--dry-run', action='store_true', help='Preflight and summarize without writing any files.')
    actions.add_argument('--check', action='store_true', help='Verify the installed files, discovery entries and managed instruction block.')
    actions.add_argument('--list', action='store_true', help='List only the curated discovery entries and dependency counts; do not install.')
    args = parser.parse_args(argv)
    try:
        if args.list:
            bundle = build_bundle(args.host or 'pi')
            for source in ('workflow', 'matt', 'pstack', 'addy'):
                print(source + ':')
                for name in bundle.registry['entry_points']:
                    if bundle.registry['skills'][name]['source'] == source:
                        print('  ' + name)
            print(f"\n{bundle.registry['counts']['entry_points']} discovery entries (21 original + combined setup); {bundle.registry['counts']['on_demand']} on-demand original helpers; no full catalogs.")
        elif args.check:
            state = check_installation(args.project)
            if args.host and args.host != state['host']:
                raise InstallError(f'Installed host is {state["host"]}, not {args.host}.')
            print(f"OK: {state['counts']['entry_points']} discovery entries, original resources and workflow instructions verified.")
        else:
            plan = prepare_install(args.project, args.host)
            if not args.dry_run:
                apply_plan(plan)
            counts = plan.bundle.registry['counts']
            label = 'DRY RUN' if args.dry_run else 'INSTALLED' if plan.changes else 'ALREADY UP TO DATE'
            print(f'{label}: {plan.project} ({plan.bundle.host})')
            print(f"{counts['entry_points']} discoverable skills (21 original + combined setup); {counts['on_demand']} original helpers outside discovery.")
            print(f'{len(plan.changes)} file changes; no global installs, downloads, hooks or whole workflow archives.')
            removed = sum(change.data is None for change in plan.changes)
            if removed:
                print(f'{"Would remove" if args.dry_run else "Removed"} {removed} unchanged installer-owned standalone setup files.')
            print(f'Read {PRIVATE}/WORKFLOW.md after reloading your agent.')
            for warning in plan.warnings:
                print('Note: ' + warning)
        return 0
    except (InstallError, OSError, ValueError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
