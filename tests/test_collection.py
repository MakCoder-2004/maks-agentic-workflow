"""Read-only checks for the original-skill collection, not an application test suite."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / 'sources.lock.json').read_text(encoding='utf-8'))
HASHES = json.loads((ROOT / 'upstream/checksums.json').read_text(encoding='utf-8'))


def files_under(folder):
    return {p.relative_to(folder).as_posix(): p for p in folder.rglob('*') if p.is_file()}


class OriginalCollectionTests(unittest.TestCase):
    def test_original_hashes(self):
        for rel, expected in HASHES.items():
            with self.subTest(path=rel):
                path = ROOT / rel
                self.assertTrue(path.is_file(), rel)
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected, rel)

    def test_source_files_and_licenses(self):
        source_roots = set()
        for source in LOCK['sources']:
            with self.subTest(source=source['id']):
                folder = ROOT / source['local_path']
                source_roots.add(folder)
                self.assertRegex(source['revision'], r'^[a-f0-9]{40}$')
                self.assertEqual(len(files_under(folder)), source['files'])
                self.assertIn('MIT License', (folder / 'LICENSE').read_text(encoding='utf-8'))
                for path in folder.rglob('*'):
                    if path.is_file():
                        self.assertIn(path.relative_to(ROOT).as_posix(), HASHES)
                for omitted in source['omitted_symlinks']:
                    target = folder / omitted['path']
                    self.assertFalse(target.exists())
                    self.assertTrue((target.parent / omitted['target']).resolve().exists())
        self.assertEqual(len(source_roots), 5)

    def test_active_skills_are_exact_original_copies(self):
        installed_names = set()
        counts = {}
        for skill in LOCK['active_skills']:
            with self.subTest(skill=skill['name']):
                self.assertNotIn(skill['name'], installed_names)
                installed_names.add(skill['name'])
                self.assertFalse(skill['name'].startswith('maw-'))
                original = files_under(ROOT / skill['original_path'])
                installed = files_under(ROOT / skill['installed_path'])
                self.assertEqual(set(installed), set(original))
                for rel in original:
                    self.assertEqual(original[rel].read_bytes(), installed[rel].read_bytes(), rel)
                text = installed['SKILL.md'].read_text(encoding='utf-8')
                name = re.search(r'^name:\s*[\"\']?([^\"\'\r\n]+)', text, re.M)
                self.assertIsNotNone(name)
                self.assertEqual(name.group(1).strip(), skill['name'])
                self.assertRegex(text, r'(?m)^description:')
                counts[skill['source']] = counts.get(skill['source'], 0) + 1
        self.assertEqual(counts, {'matt': 21, 'pstack': 57, 'addy': 22, 'cursor-team-kit': 3})
        self.assertEqual(counts, LOCK['active_counts'])
        self.assertEqual(len(installed_names), 103)
        actual = {p.parent.name for p in (ROOT / '.agents/skills').glob('*/SKILL.md')}
        self.assertEqual(actual, installed_names)

    def test_shared_reference_closure(self):
        for resource in LOCK['active_resources']:
            original = files_under(ROOT / resource['original_path'])
            installed = files_under(ROOT / resource['installed_path'])
            self.assertEqual(set(original), set(installed))
            for rel in original:
                self.assertEqual(original[rel].read_bytes(), installed[rel].read_bytes())
        for skill in LOCK['active_skills']:
            if skill['source'] != 'addy':
                continue
            folder = ROOT / skill['installed_path']
            for path in folder.rglob('*.md'):
                text = path.read_text(encoding='utf-8')
                for rel in re.findall(r'\]\((\.\./\.\./references/[^)#]+)(?:#[^)]*)?\)', text):
                    with self.subTest(path=str(path), reference=rel):
                        self.assertTrue((path.parent / rel).is_file())

    def test_pstack_complete_and_matt_composition_present(self):
        source = ROOT / 'upstream/pstack/skills'
        pstack_names = {p.parent.name for p in source.glob('*/SKILL.md')}
        selected = {s['name'] for s in LOCK['active_skills'] if s['source'] == 'pstack'}
        self.assertEqual(selected, pstack_names - {'setup-pstack'})
        self.assertNotIn('setup-matt-pocock-skills', {s['name'] for s in LOCK['active_skills']})
        self.assertEqual(len([n for n in selected if n.startswith('principle-')]), 24)
        self.assertEqual(len(list((ROOT / '.agents/skills/poteto-mode/playbooks').glob('*.md'))), 23)
        self.assertTrue((ROOT / 'upstream/pstack/agents/poteto-agent.md').is_file())
        self.assertTrue((ROOT / 'upstream/pstack/agents/comment-sicko.md').is_file())
        active = {s['name']: s for s in LOCK['active_skills']}
        for name in ['grill-with-docs', 'grilling', 'domain-modeling', 'to-spec', 'to-tickets']:
            self.assertEqual(active[name]['source'], 'matt')
        self.assertEqual(active['tdd']['source'], 'pstack')
        self.assertEqual(active['test-driven-development']['source'], 'addy')
        for name in ['control-ui', 'control-cli', 'deslop']:
            self.assertEqual(active[name]['source'], 'cursor-team-kit')
        for name in ['implement', 'implement-spec', 'using-agent-skills', 'incremental-implementation', 'planning-and-task-breakdown']:
            self.assertNotIn(name, active)

    def test_git_index_preserves_original_bytes_and_executable_modes(self):
        if not (ROOT / '.git').exists():
            self.skipTest('Git index is unavailable outside a checkout')
        rows = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=ROOT).split(b'\0')
        entries = {}
        for row in rows:
            if not row:
                continue
            meta, rel = row.decode('utf-8').split('\t', 1)
            mode, oid, stage = meta.split()
            self.assertEqual(stage, '0')
            entries[rel] = (mode, oid)
        if 'sources.lock.json' not in entries:
            self.skipTest('Collection has not been staged yet')
        algorithm = subprocess.check_output(['git', 'rev-parse', '--show-object-format'], cwd=ROOT, text=True).strip()
        executables = set(LOCK['executable_files'])
        self.assertEqual(len(executables), 27)
        reference_root = ROOT / 'workflow/skills/setup-agentic-workflow/references'
        preserved_paths = set(HASHES) | {p.relative_to(ROOT).as_posix() for p in reference_root.rglob('*') if p.is_file()}
        for rel in preserved_paths:
            with self.subTest(path=rel):
                data = (ROOT / rel).read_bytes()
                blob = b'blob ' + str(len(data)).encode() + b'\0' + data
                expected_oid = hashlib.new(algorithm, blob).hexdigest()
                self.assertIn(rel, entries)
                self.assertEqual(entries[rel][1], expected_oid, 'Git filters changed original bytes')
                self.assertEqual(entries[rel][0], '100755' if rel in executables else '100644')

    def test_native_loader_manifests(self):
        for name in ['matt', 'pstack-claude-code', 'addy']:
            path = ROOT / 'upstream' / name / '.claude-plugin/plugin.json'
            data = json.loads(path.read_text(encoding='utf-8'))
            self.assertTrue(data['name'])
        self.assertTrue((ROOT / 'upstream/cursor-team-kit/.cursor-plugin/plugin.json').is_file())
        self.assertFalse((ROOT / 'upstream/cursor-team-kit/.claude-plugin/plugin.json').exists())
        self.assertIn('@AGENTS.md', (ROOT / 'CLAUDE.md').read_text(encoding='utf-8'))

    def test_our_document_links_and_whitespace(self):
        docs = list((ROOT / 'docs').rglob('*.md')) + [ROOT / 'README.md', ROOT / 'NOTICE.md', ROOT / 'AGENTS.md', ROOT / 'CLAUDE.md']
        for path in docs:
            text = path.read_text(encoding='utf-8')
            for n, line in enumerate(text.splitlines(), 1):
                with self.subTest(path=str(path), line=n):
                    self.assertEqual(line, line.rstrip())
            targets = re.findall(r'\]\(([^)]+)\)', text)
            targets += re.findall(r'^\[[^\]]+\]:\s+(\S+)', text, re.M)
            for target in targets:
                if target.startswith(('https:', 'http:', 'mailto:', '#')):
                    continue
                with self.subTest(path=str(path), target=target):
                    self.assertTrue((path.parent / target.split('#', 1)[0]).exists())


if __name__ == '__main__':
    unittest.main()
