"""One setup skill, non-skill references, and safe retirement of older copies."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path, PurePosixPath
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import install as installer


class CombinedSetupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundles = {host: installer.build_bundle(host) for host in ('pi', 'claude-code')}

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='maks-setup-')
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name).resolve() / 'project'

    def prepare(self, host='pi', bundle=None):
        with patch.object(installer, 'build_bundle', return_value=bundle or self.bundles[host]):
            return installer.prepare_install(self.project, host)

    @staticmethod
    def legacy_bundle(current, unified=False):
        registry = deepcopy(current.registry)
        setup = registry['skills'][installer.SETUP_SKILL]
        roots = tuple(str(PurePosixPath(setup[key]).parent) + '/' for key in ('canonical_path', 'discovery_path'))
        reference_roots = tuple(root + 'references/' for root in roots)
        files = {path: spec for path, spec in current.files.items()
                 if not path.startswith(reference_roots if unified else roots)}
        files.update(current.retired_files)
        for source, name in [('matt', 'setup-matt-pocock-skills'), ('pstack', 'setup-pstack')]:
            candidates = [path for path in current.retired_files if path.endswith('/' + name + '/SKILL.md')]
            canonical = next(path for path in candidates if path.startswith(installer.PRIVATE + '/'))
            public = next((path for path in candidates if not path.startswith(installer.PRIVATE + '/')), None)
            registry['skills'][name] = {'source': source, 'kind': 'upstream', 'canonical_path': canonical, 'discovery_path': public}
        registry['entry_points'].insert(1, 'setup-matt-pocock-skills')
        registry.pop('setup_references')
        registry['counts'] = {'entry_points': 23 if unified else 22, 'on_demand': 54,
                              'total_original_skills': 76,
                              'entry_points_by_source': {'matt': 9, 'pstack': 1, 'addy': 12}}
        if unified:
            registry['counts']['integration_skills'] = 1
            registry['counts']['entry_points_by_source']['workflow'] = 1
            public = str(PurePosixPath(setup['discovery_path']).parent)
            attributes = ''.join(f'{json.dumps(path)} -text\n' for path in ['SKILL.md', 'agents/openai.yaml'])
            files[public + '/.gitattributes'] = installer.FileSpec(attributes.encode())
        else:
            del registry['skills'][installer.SETUP_SKILL]
            registry['entry_points'].remove(installer.SETUP_SKILL)
        files[f'{installer.PRIVATE}/registry.json'] = installer.FileSpec(installer.json_bytes(registry))
        return replace(current, files=files, registry=registry)

    def install_legacy(self, host='pi', unified=False):
        legacy = self.legacy_bundle(self.bundles[host], unified)
        old_block = installer.START + b'\nLegacy workflow rules\n' + installer.END
        with patch.object(installer, 'instruction_block', return_value=old_block):
            plan = self.prepare(host, legacy)
        installer.apply_plan(plan)
        return plan

    def test_only_combined_setup_is_a_registered_skill(self):
        for host, bundle in self.bundles.items():
            with self.subTest(host=host):
                record = bundle.registry['skills'][installer.SETUP_SKILL]
                self.assertEqual(record['kind'], 'integration')
                self.assertEqual(bundle.registry['counts']['entry_points'], 22)
                self.assertEqual(bundle.registry['counts']['total_original_skills'], 74)
                self.assertEqual(bundle.registry['counts']['on_demand'], 53)
                for name in ['setup-matt-pocock-skills', 'setup-pstack']:
                    self.assertNotIn(name, bundle.registry['skills'])
                    self.assertFalse(any(path.endswith('/' + name + '/SKILL.md') for path in bundle.files))
                for source, path in bundle.registry['setup_references'].items():
                    self.assertTrue(path.endswith('/SETUP.txt'))
                    self.assertIn(path, bundle.files)
                    original = ROOT / ('upstream/matt/skills/engineering/setup-matt-pocock-skills/SKILL.md' if source == 'matt' else 'upstream/pstack/skills/setup-pstack/SKILL.md')
                    self.assertEqual(bundle.files[path].data, original.read_bytes())

    def test_installed_setup_and_templates_are_preserved_without_old_skills(self):
        plan = self.prepare()
        installer.apply_plan(plan)
        record = plan.bundle.registry['skills'][installer.SETUP_SKILL]
        expected = (ROOT / 'workflow/skills/setup-agentic-workflow/SKILL.md').read_bytes()
        self.assertEqual((self.project / record['canonical_path']).read_bytes(), expected)
        self.assertEqual((self.project / record['discovery_path']).read_bytes(), expected)
        folder = (self.project / record['canonical_path']).parent
        self.assertTrue((folder / 'references/matt/issue-tracker-local.md').is_file())
        self.assertTrue((folder / 'references/matt/domain.md').is_file())
        self.assertFalse(list((folder / 'references').rglob('SKILL.md')))
        self.assertFalse(list((folder / 'references').rglob('SETUP.md')))
        self.assertIn('allow_implicit_invocation: false', (folder / 'agents/openai.yaml').read_text())
        self.assertLess(len(expected.decode().splitlines()), 200)
        installer.check_installation(self.project)

    def test_skill_keeps_canonical_instructions_and_approval_guards(self):
        text = (ROOT / 'workflow/skills/setup-agentic-workflow/SKILL.md').read_text(encoding='utf-8')
        for guard in ['references/matt/SETUP.txt', 'references/pstack/SETUP.txt', 'constraint-driven-development',
                      'context-engineering', 'AGENTS.md', 'If missing, create', 'If present, preserve',
                      'installer-owned', 'one shared intake', 'global rule only', 'Re-running',
                      'Addy has no dedicated upstream setup skill', 'not installed, enforced or passing']:
            self.assertIn(guard.casefold(), text.casefold())

    def test_managed_instructions_and_host_runbook_recommend_one_setup(self):
        for host, command in [('pi', '/skill:setup-agentic-workflow'), ('claude-code', '/setup-agentic-workflow')]:
            plan = self.prepare(host)
            installer.apply_plan(plan)
            runbook = (self.project / installer.PRIVATE / 'WORKFLOW.md').read_text(encoding='utf-8')
            self.assertIn(command, runbook)
            self.assertIn('do not need to run three setup flows', runbook)
            self.project.rename(self.project.with_name(host))

    def test_both_published_profiles_retire_only_the_known_owned_files(self):
        for host in self.bundles:
            for unified in (False, True):
                with self.subTest(host=host, unified=unified):
                    self.project.mkdir()
                    instruction = 'CLAUDE.md' if host == 'claude-code' else 'AGENTS.md'
                    user_text = b'# User rules\r\nPreserve these exactly.\r\n'
                    (self.project / instruction).write_bytes(user_text)
                    old = self.install_legacy(host, unified)
                    before = {path: spec.data for path, spec in old.bundle.files.items() if spec.source and path not in old.bundle.retired_files}
                    plan = self.prepare(host)
                    self.assertFalse(any('remain discoverable' in message and 'setup-matt-pocock-skills' in message for message in plan.warnings))
                    removed = {change.relative for change in plan.changes if change.data is None}
                    self.assertEqual(removed, set(plan.bundle.retired_files))
                    installer.apply_plan(plan)
                    for path in removed:
                        self.assertFalse((self.project / path).exists(), path)
                    for path, data in before.items():
                        if path in self.bundles[host].files and not path.startswith(tuple(str(PurePosixPath(self.bundles[host].registry['skills'][installer.SETUP_SKILL][key]).parent) for key in ['canonical_path', 'discovery_path'])):
                            self.assertEqual((self.project / path).read_bytes(), data)
                    self.assertTrue((self.project / instruction).read_bytes().startswith(user_text))
                    installer.check_installation(self.project)
                    self.assertEqual(self.prepare(host).changes, [])
                    self.project.rename(self.project.with_name(f'{host}-{unified}'))

    def test_legacy_missing_helper_record_cannot_hide_inside_setup_update(self):
        self.install_legacy()
        state_path = self.project / installer.STATE
        state = json.loads(state_path.read_text())
        helper = self.bundles['pi'].registry['skills']['grilling']['canonical_path']
        (self.project / helper).unlink()
        del state['files'][helper]
        state_path.write_bytes(installer.json_bytes(state))
        with self.assertRaisesRegex(installer.InstallError, 'inventory is incomplete'):
            self.prepare()
        self.assertTrue((self.project / '.agents/skills/setup-matt-pocock-skills/SKILL.md').exists())

    def test_locally_changed_retired_skill_blocks_removal(self):
        self.install_legacy(unified=True)
        path = self.project / '.agents/skills/setup-matt-pocock-skills/SKILL.md'
        path.write_bytes(path.read_bytes() + b'\nLocal changes\n')
        with self.assertRaisesRegex(installer.InstallError, 'Locally changed'):
            self.prepare()
        self.assertTrue(path.read_bytes().endswith(b'Local changes\n'))

    def test_unowned_retired_skill_blocks_removal(self):
        self.install_legacy(unified=True)
        state_path = self.project / installer.STATE
        state = json.loads(state_path.read_text())
        path = '.agents/skills/setup-matt-pocock-skills/SKILL.md'
        state['files'][path]['owned'] = False
        state_path.write_bytes(installer.json_bytes(state))
        with self.assertRaisesRegex(installer.InstallError, 'unowned'):
            self.prepare()
        self.assertTrue((self.project / path).exists())

    def test_unmanaged_standalone_setup_is_not_deleted(self):
        folder = self.project / '.agents/skills/setup-pstack'
        folder.mkdir(parents=True)
        original = (ROOT / 'upstream/pstack/skills/setup-pstack/SKILL.md').read_bytes()
        (folder / 'SKILL.md').write_bytes(original)
        with self.assertRaisesRegex(installer.InstallError, 'Unmanaged standalone setup'):
            self.prepare()
        self.assertEqual((folder / 'SKILL.md').read_bytes(), original)
        self.assertFalse((self.project / installer.PRIVATE).exists())

    def test_check_detects_a_standalone_setup_reintroduced_after_install(self):
        installer.apply_plan(self.prepare())
        folder = self.project / '.agents/skills/setup-pstack'
        folder.mkdir()
        (folder / 'SKILL.md').write_bytes((ROOT / 'upstream/pstack/skills/setup-pstack/SKILL.md').read_bytes())
        with self.assertRaisesRegex(installer.InstallError, 'still discoverable'):
            installer.check_installation(self.project)
        self.assertTrue((folder / 'SKILL.md').exists())

    def test_user_extras_in_retired_folder_survive(self):
        self.install_legacy(unified=True)
        extra = self.project / '.agents/skills/setup-matt-pocock-skills/my-notes.txt'
        extra.write_bytes(b'User-owned extra')
        installer.apply_plan(self.prepare())
        self.assertEqual(extra.read_bytes(), b'User-owned extra')
        self.assertFalse((extra.parent / 'SKILL.md').exists())
        installer.check_installation(self.project)

    def test_failure_after_retirement_restores_removed_files(self):
        self.install_legacy(unified=True)
        before = {p.relative_to(self.project).as_posix(): p.read_bytes() for p in self.project.rglob('*') if p.is_file()}
        plan = self.prepare()
        real_write = installer.atomic_write
        def fail_state(path, data, mode):
            if path == self.project / installer.STATE:
                raise OSError('injected retirement failure')
            real_write(path, data, mode)
        with patch.object(installer, 'atomic_write', side_effect=fail_state):
            with self.assertRaisesRegex(OSError, 'injected retirement failure'):
                installer.apply_plan(plan)
        after = {p.relative_to(self.project).as_posix(): p.read_bytes() for p in self.project.rglob('*') if p.is_file()}
        self.assertEqual(after, before)

    def test_conflicting_combined_setup_is_not_overwritten_during_update(self):
        self.install_legacy()
        path = self.project / '.agents/skills/setup-agentic-workflow/SKILL.md'
        path.parent.mkdir(parents=True)
        content = b'---\nname: setup-agentic-workflow\ndescription: User custom setup.\n---\nKeep me.\n'
        path.write_bytes(content)
        with self.assertRaisesRegex(installer.InstallError, 'conflicts'):
            self.prepare()
        self.assertEqual(path.read_bytes(), content)
        self.assertTrue((self.project / '.agents/skills/setup-matt-pocock-skills/SKILL.md').exists())

    def test_forged_legacy_counts_on_current_inventory_are_refused(self):
        installer.apply_plan(self.prepare())
        state_path = self.project / installer.STATE
        state = json.loads(state_path.read_text())
        state['counts'] = self.legacy_bundle(self.bundles['pi']).registry['counts']
        state_path.write_bytes(installer.json_bytes(state))
        with self.assertRaisesRegex(installer.InstallError, 'not the exact supported setup upgrade'):
            self.prepare()

    def test_setup_docs_outside_owned_marker_remain_valid_on_reinstall(self):
        installer.apply_plan(self.prepare())
        path = self.project / 'AGENTS.md'
        added = b'\n## Agent skills\n\nRead docs/agents/domain.md and CONSTRAINTS.md.\n'
        path.write_bytes(path.read_bytes() + added)
        (self.project / 'CONSTRAINTS.md').write_bytes(b'# Approved constraints\n')
        installer.check_installation(self.project)
        self.assertEqual(self.prepare().changes, [])
        self.assertTrue(path.read_bytes().endswith(added))


if __name__ == '__main__':
    unittest.main()
