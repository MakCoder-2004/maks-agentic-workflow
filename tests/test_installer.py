"""The consuming project must receive a compact, intact and safely managed view."""
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
import hashlib
import io
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import install as installer


class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundles = {host: installer.build_bundle(host) for host in installer.HOSTS}

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='maks-installer-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.project = self.base / 'My project with spaces'

    def prepare(self, host=None, project=None, bundle=None):
        def selected(value):
            return bundle if bundle is not None else self.bundles[value]
        with patch.object(installer, 'build_bundle', side_effect=selected):
            return installer.prepare_install(project or self.project, host)

    def installed(self, host='pi'):
        plan = self.prepare(host)
        installer.apply_plan(plan)
        return plan

    @staticmethod
    def snapshot(project):
        return {p.relative_to(project).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in project.rglob('*') if p.is_file()}

    def test_exact_discovery_selection_and_private_dependencies(self):
        bundle = self.bundles['pi']
        self.assertEqual(bundle.registry['counts'], {
            'entry_points': 22, 'on_demand': 53, 'total_original_skills': 74, 'integration_skills': 1,
            'entry_points_by_source': {'workflow': 1, 'matt': 8, 'pstack': 1, 'addy': 12},
        })
        visible = bundle.registry['entry_points']
        self.assertIn('setup-agentic-workflow', visible)
        self.assertEqual(bundle.registry['skills']['setup-agentic-workflow']['kind'], 'integration')
        self.assertIn('poteto-mode', visible)
        self.assertIn('to-spec', visible)
        self.assertIn('to-tickets', visible)
        self.assertIn('shipping-and-launch', visible)
        self.assertNotIn('domain-modeling', visible)
        self.assertNotIn('principle-prove-it-works', visible)
        self.assertNotIn('tdd', visible)
        for name in ['grilling', 'domain-modeling', 'how', 'architect', 'interrogate', 'deslop', 'tdd']:
            self.assertIsNone(bundle.registry['skills'][name]['discovery_path'])
        for name in ['implement-spec', 'using-agent-skills', 'make-bot-ui', 'ketchup-video', 'automate-me', 'teach']:
            self.assertNotIn(name, bundle.registry['skills'])
        principles = [n for n in bundle.registry['skills'] if n.startswith('principle-')]
        self.assertEqual(len(principles), 24)
        self.assertFalse(any('.claude-plugin/' in p or '/automations/' in p or '/hooks/' in p for p in bundle.files))

    def test_fresh_install_has_only_22_discovery_entries(self):
        self.installed()
        state = installer.check_installation(self.project)
        entries = list((self.project / '.agents/skills').rglob('SKILL.md'))
        self.assertEqual(len(entries), 22)
        self.assertEqual(state['counts']['entry_points'], 22)
        self.assertFalse((self.project / 'upstream').exists())
        self.assertFalse((self.project / '.claude/skills').exists())
        self.assertFalse((self.project / '.pi/agents').exists())
        block = (self.project / 'AGENTS.md').read_bytes()
        self.assertEqual(block.count(installer.START), 1)
        self.assertIn(b'canonical_path', block)
        for name, record in self.bundles['pi'].registry['skills'].items():
            self.assertTrue((self.project / record['canonical_path']).is_file(), name)
        self.assertEqual(len(list((self.project / installer.PRIVATE / 'originals').rglob('SKILL.md'))), 74)

    def test_all_original_payload_bytes_unchanged(self):
        for host, bundle in self.bundles.items():
            for path, spec in bundle.files.items():
                if spec.source:
                    with self.subTest(host=host, path=path):
                        self.assertEqual(spec.data, (ROOT / spec.source).read_bytes())
        self.assertFalse(any(name.startswith('maw-') for name in self.bundles['pi'].registry['skills']))

    def test_idempotent_install_changes_no_files_or_mtimes(self):
        self.installed()
        before = self.snapshot(self.project)
        repeated = self.prepare()
        self.assertEqual(repeated.changes, [])
        installer.apply_plan(repeated)
        self.assertEqual(self.snapshot(self.project), before)
        installer.check_installation(self.project)

    def test_preserves_bom_crlf_and_user_edits_outside_managed_block(self):
        self.project.mkdir()
        original = b'\xef\xbb\xbf# Existing project\r\nKeep these rules exactly.\r\n'
        (self.project / 'AGENTS.md').write_bytes(original)
        self.installed()
        path = self.project / 'AGENTS.md'
        self.assertTrue(path.read_bytes().startswith(original))
        suffix = b'\r\n# User-added rule\r\nKeep me too.\r\n'
        path.write_bytes(path.read_bytes() + suffix)
        before = path.read_bytes()
        self.assertEqual(self.prepare().changes, [])
        installer.check_installation(self.project)
        self.assertEqual(path.read_bytes(), before)

    def test_each_host_layout_and_original_role_definitions(self):
        for host in installer.HOSTS:
            project = self.base / host
            with self.subTest(host=host):
                plan = self.prepare(host, project)
                installer.apply_plan(plan)
                installer.check_installation(project)
                root = '.claude/skills' if host == 'claude-code' else '.agents/skills'
                self.assertEqual(len(list((project / root).rglob('SKILL.md'))), 22)
                instruction = 'CLAUDE.md' if host == 'claude-code' else 'AGENTS.md'
                self.assertIn(installer.START, (project / instruction).read_bytes())
                self.assertFalse((project / ('AGENTS.md' if host == 'claude-code' else 'CLAUDE.md')).exists())
                registry = self.bundles[host].registry
                for role, record in registry['roles'].items():
                    if host in ('cursor', 'claude-code'):
                        native = project / record['native_path']
                        self.assertEqual(native.read_bytes(), (ROOT / f'upstream/pstack/agents/{role}.md').read_bytes())
                    else:
                        self.assertIsNone(record['native_path'])
                self.assertNotIn('{{', (project / installer.PRIVATE / 'WORKFLOW.md').read_text(encoding='utf-8'))
                for document in ['WORKFLOW.md', 'NOTICE.md']:
                    file = project / installer.PRIVATE / document
                    for target in re.findall(r'\]\(([^)]+)\)', file.read_text(encoding='utf-8')):
                        if not target.startswith(('https:', 'http:', '#')):
                            self.assertTrue((file.parent / target.split('#', 1)[0]).exists(), target)

    def test_addy_shared_and_pstack_sibling_resources_resolve(self):
        for host in ('pi', 'claude-code'):
            project = self.base / host
            installer.apply_plan(self.prepare(host, project))
            registry = self.bundles[host].registry
            for name in ['security-and-hardening', 'shipping-and-launch']:
                folder = (project / registry['skills'][name]['discovery_path']).parent
                self.assertTrue((folder / '../../references/security-checklist.md').resolve().is_file())
                canonical = (project / registry['skills'][name]['canonical_path']).parent
                self.assertTrue((canonical / '../../references/security-checklist.md').resolve().is_file())
            mode = (project / registry['skills']['poteto-mode']['canonical_path']).parent
            self.assertTrue((mode / '../how/SKILL.md').resolve().is_file())
            self.assertTrue((mode / '../principle-prove-it-works/SKILL.md').resolve().is_file())
            self.assertTrue((mode / 'playbooks/opening-a-pr.md').is_file())

    def test_preview_does_not_even_create_project_directory(self):
        output = io.StringIO()
        with patch.object(installer, 'build_bundle', return_value=self.bundles['pi']), redirect_stdout(output):
            code = installer.main(['--project', str(self.project), '--dry-run'])
        self.assertEqual(code, 0)
        self.assertIn('DRY RUN', output.getvalue())
        self.assertIn('22 discoverable', output.getvalue())
        self.assertFalse(self.project.exists())

    def test_dry_run_preserves_existing_files_and_permissions(self):
        self.project.mkdir()
        path = self.project / 'AGENTS.md'
        path.write_text('Keep this file.\n', encoding='utf-8')
        before = self.snapshot(self.project)
        self.prepare()
        self.assertEqual(self.snapshot(self.project), before)
        self.assertFalse((self.project / installer.PRIVATE).exists())

    def test_unrelated_existing_skill_is_preserved(self):
        folder = self.project / '.agents/skills/my-existing-skill'
        folder.mkdir(parents=True)
        path = folder / 'SKILL.md'
        data = b'---\nname: my-existing-skill\ndescription: My own skill.\n---\nKeep this.\n'
        path.write_bytes(data)
        self.installed()
        self.assertEqual(path.read_bytes(), data)
        self.assertEqual(len(list((self.project / '.agents/skills').rglob('SKILL.md'))), 23)
        installer.check_installation(self.project)

    def test_conflicting_entry_is_refused_before_any_write(self):
        folder = self.project / '.agents/skills/to-spec'
        folder.mkdir(parents=True)
        (folder / 'SKILL.md').write_bytes(b'---\nname: to-spec\ndescription: User version.\n---\nDo not overwrite.\n')
        before = self.snapshot(self.project)
        with self.assertRaisesRegex(installer.InstallError, 'conflicts'):
            self.prepare()
        self.assertEqual(self.snapshot(self.project), before)
        self.assertFalse((self.project / installer.PRIVATE).exists())

    def test_collision_in_other_host_directory_is_refused(self):
        folder = self.project / '.claude/skills/to-spec'
        folder.mkdir(parents=True)
        source = self.bundles['pi'].files['.agents/skills/to-spec/SKILL.md'].data
        (folder / 'SKILL.md').write_bytes(source)
        with self.assertRaisesRegex(installer.InstallError, 'Duplicate skill discovery'):
            self.prepare()
        self.assertFalse((self.project / installer.PRIVATE).exists())

    def test_existing_discovered_helper_is_reported_not_deleted(self):
        folder = self.project / '.agents/skills/how'
        folder.mkdir(parents=True)
        original = (ROOT / 'upstream/pstack/skills/how/SKILL.md').read_bytes()
        (folder / 'SKILL.md').write_bytes(original)
        plan = self.prepare()
        self.assertTrue(any('how' in warning and 'not removed' in warning for warning in plan.warnings))
        installer.apply_plan(plan)
        self.assertEqual((folder / 'SKILL.md').read_bytes(), original)

    def test_identical_unowned_entry_is_reused_not_claimed(self):
        folder = self.project / '.agents/skills/to-spec'
        folder.mkdir(parents=True)
        relative = '.agents/skills/to-spec/SKILL.md'
        path = folder / 'SKILL.md'
        path.write_bytes(self.bundles['pi'].files[relative].data)
        timestamp = path.stat().st_mtime_ns
        plan = self.installed()
        self.assertFalse(plan.state['files'][relative]['owned'])
        self.assertEqual(path.stat().st_mtime_ns, timestamp)
        files = dict(self.bundles['pi'].files)
        files[relative] = replace(files[relative], data=files[relative].data + b'\nNew source version.\n')
        updated = replace(self.bundles['pi'], files=files)
        with self.assertRaisesRegex(installer.InstallError, 'user-owned'):
            self.prepare(bundle=updated)
        self.assertEqual(path.stat().st_mtime_ns, timestamp)

    def test_locally_edited_original_refuses_reinstall_and_check(self):
        self.installed()
        path = self.project / '.agents/skills/to-spec/SKILL.md'
        path.write_bytes(path.read_bytes() + b'\nA local edit.\n')
        before = self.snapshot(self.project)
        with self.assertRaisesRegex(installer.InstallError, 'Locally changed'):
            self.prepare()
        with self.assertRaisesRegex(installer.InstallError, 'modified installed file'):
            installer.check_installation(self.project)
        self.assertEqual(self.snapshot(self.project), before)

    def test_changed_managed_instruction_block_is_not_overwritten(self):
        self.installed()
        path = self.project / 'AGENTS.md'
        path.write_bytes(path.read_bytes().replace(installer.END, b'User decision\n' + installer.END))
        before = self.snapshot(self.project)
        with self.assertRaisesRegex(installer.InstallError, 'managed workflow block'):
            self.prepare()
        with self.assertRaisesRegex(installer.InstallError, 'managed workflow block'):
            installer.check_installation(self.project)
        self.assertEqual(self.snapshot(self.project), before)

    def test_missing_installed_file_is_reported_not_silently_restored(self):
        self.installed()
        (self.project / '.agents/skills/to-spec/SKILL.md').unlink()
        with self.assertRaisesRegex(installer.InstallError, 'missing installed file|changed or missing'):
            self.prepare()
        with self.assertRaisesRegex(installer.InstallError, 'Missing or modified'):
            installer.check_installation(self.project)

    def test_corrupt_markers_do_not_create_a_second_block(self):
        self.project.mkdir()
        (self.project / 'AGENTS.md').write_bytes(installer.START + b'\n' + installer.START + b'\n' + installer.END)
        with self.assertRaisesRegex(installer.InstallError, 'Malformed or duplicate'):
            self.prepare()
        self.assertFalse((self.project / installer.PRIVATE).exists())

    def test_unowned_managed_marker_is_not_adopted_silently(self):
        self.project.mkdir()
        (self.project / 'AGENTS.md').write_bytes(installer.START + b'\nUser-owned block\n' + installer.END)
        with self.assertRaisesRegex(installer.InstallError, 'Unowned workflow markers'):
            self.prepare()

    def test_shared_reference_conflict_is_refused(self):
        folder = self.project / '.agents/references'
        folder.mkdir(parents=True)
        (folder / 'security-checklist.md').write_text('My checklist', encoding='utf-8')
        before = self.snapshot(self.project)
        with self.assertRaisesRegex(installer.InstallError, 'conflicts'):
            self.prepare()
        self.assertEqual(self.snapshot(self.project), before)

    def test_host_switch_does_not_duplicate_the_install(self):
        self.installed('pi')
        before = self.snapshot(self.project)
        with self.assertRaisesRegex(installer.InstallError, 'already installed for pi'):
            self.prepare('claude-code')
        self.assertEqual(self.snapshot(self.project), before)

    def test_owned_payload_updates_only_when_unedited(self):
        self.installed()
        relative = f'{installer.PRIVATE}/WORKFLOW.md'
        files = dict(self.bundles['pi'].files)
        files[relative] = replace(files[relative], data=files[relative].data + b'\nUpdated guide.\n')
        updated = replace(self.bundles['pi'], files=files)
        plan = self.prepare(bundle=updated)
        self.assertEqual({c.relative for c in plan.changes}, {relative, installer.STATE})
        installer.apply_plan(plan)
        self.assertEqual((self.project / relative).read_bytes(), files[relative].data)
        installer.check_installation(self.project)

    def test_obsolete_manifest_entries_never_authorize_deletion(self):
        self.installed()
        readme = self.project / 'README.md'
        readme.write_bytes(b'User project.\n')
        state_path = self.project / installer.STATE
        state = json.loads(state_path.read_text(encoding='utf-8'))
        state['files']['README.md'] = {'sha256': installer.digest(readme.read_bytes()), 'owned': True, 'mode': 0o644}
        state_path.write_bytes(installer.json_bytes(state))
        with self.assertRaisesRegex(installer.InstallError, 'obsolete managed files'):
            self.prepare()
        self.assertEqual(readme.read_bytes(), b'User project.\n')

    def test_unsafe_manifest_path_is_rejected(self):
        self.installed()
        state_path = self.project / installer.STATE
        state = json.loads(state_path.read_text(encoding='utf-8'))
        state['files']['../../outside'] = {'sha256': '0' * 64, 'owned': True, 'mode': 0o644}
        state_path.write_bytes(installer.json_bytes(state))
        with self.assertRaisesRegex(installer.InstallError, 'Unsafe relative'):
            self.prepare()
        self.assertFalse((self.base / 'outside').exists())

    def test_directory_in_place_of_an_installed_file_is_refused(self):
        path = self.project / '.agents/skills/to-spec/SKILL.md'
        path.mkdir(parents=True)
        with self.assertRaises(installer.InstallError):
            self.prepare()
        self.assertTrue(path.is_dir())
        self.assertFalse((self.project / installer.PRIVATE).exists())

    def test_symlink_or_windows_junction_cannot_redirect_writes(self):
        self.project.mkdir()
        outside = self.base / 'outside'
        outside.mkdir()
        marker = outside / 'keep.txt'
        marker.write_bytes(b'untouched')
        link = self.project / '.agents'
        if os.name == 'nt':
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(outside)], capture_output=True)
            if result.returncode:
                self.skipTest('Windows junction creation is unavailable')
        else:
            link.symlink_to(outside, target_is_directory=True)
        try:
            with self.assertRaisesRegex(installer.InstallError, 'symlink/junction/reparse'):
                self.prepare()
            self.assertEqual(marker.read_bytes(), b'untouched')
            self.assertEqual(list(outside.iterdir()), [marker])
            self.assertFalse((self.project / installer.PRIVATE).exists())
        finally:
            if os.name == 'nt':
                link.rmdir()
            else:
                link.unlink()

    def test_raw_atomic_write_is_not_a_directory_swap_sandbox(self):
        # Both directories are disposable test-owned fixtures. This deliberately
        # records the documented trusted/idle-parent contract, not a safety pass.
        self.project.mkdir()
        parent = self.project / 'parent'
        parent.mkdir()
        outside = self.base / 'test-owned-outside'
        outside.mkdir()
        checked = installer.safe_path(self.project, 'parent/probe.txt')
        parent.rename(self.project / 'old-parent')
        if os.name == 'nt':
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(parent), str(outside)], capture_output=True)
            if result.returncode:
                self.skipTest('Windows junction creation is unavailable')
        else:
            parent.symlink_to(outside, target_is_directory=True)
        try:
            with self.assertRaises(installer.InstallError):
                installer.safe_path(self.project, 'parent/probe.txt')
            installer.atomic_write(checked, b'disposable race-boundary probe', 0o644)
            self.assertEqual((outside / 'probe.txt').read_bytes(), b'disposable race-boundary probe')
        finally:
            if os.name == 'nt':
                parent.rmdir()
            else:
                parent.unlink()

    def test_source_integrity_mismatch_is_not_accepted(self):
        path = ROOT / 'upstream/matt/skills/engineering/to-spec/SKILL.md'
        with self.assertRaisesRegex(installer.InstallError, 'checksum mismatch'):
            installer.source_data(path, {path.relative_to(ROOT).as_posix(): '0' * 64})

    def test_failure_after_instruction_write_rolls_back_new_install(self):
        self.project.mkdir()
        original = b'# Original project policy\r\nKeep it.\r\n'
        (self.project / 'AGENTS.md').write_bytes(original)
        plan = self.prepare()
        real_write = installer.atomic_write
        def fail_state(path, data, mode):
            if path == self.project / installer.STATE:
                raise OSError('injected final manifest write failure')
            real_write(path, data, mode)
        with patch.object(installer, 'atomic_write', side_effect=fail_state):
            with self.assertRaisesRegex(OSError, 'injected'):
                installer.apply_plan(plan)
        self.assertEqual((self.project / 'AGENTS.md').read_bytes(), original)
        self.assertEqual(list(self.project.iterdir()), [self.project / 'AGENTS.md'])

    def test_failure_rolls_back_an_existing_owned_update(self):
        self.installed()
        before = {p: data for p, (data, _) in self.snapshot(self.project).items()}
        relative = f'{installer.PRIVATE}/WORKFLOW.md'
        files = dict(self.bundles['pi'].files)
        files[relative] = replace(files[relative], data=files[relative].data + b'\nNew guide.\n')
        plan = self.prepare(bundle=replace(self.bundles['pi'], files=files))
        real_write = installer.atomic_write
        def fail_state(path, data, mode):
            if path == self.project / installer.STATE:
                raise OSError('injected update failure')
            real_write(path, data, mode)
        with patch.object(installer, 'atomic_write', side_effect=fail_state):
            with self.assertRaisesRegex(OSError, 'injected'):
                installer.apply_plan(plan)
        after = {p: data for p, (data, _) in self.snapshot(self.project).items()}
        self.assertEqual(after, before)
        installer.check_installation(self.project)

    def test_concurrent_change_after_preflight_is_preserved(self):
        self.project.mkdir()
        path = self.project / 'AGENTS.md'
        path.write_bytes(b'Before preflight')
        plan = self.prepare()
        path.write_bytes(b'Changed by the user during preflight')
        with self.assertRaisesRegex(installer.InstallError, 'changed after preflight'):
            installer.apply_plan(plan)
        self.assertEqual(path.read_bytes(), b'Changed by the user during preflight')
        self.assertFalse((self.project / installer.PRIVATE).exists())

    def test_permission_change_after_preflight_is_preserved(self):
        self.project.mkdir()
        path = self.project / 'AGENTS.md'
        path.write_bytes(b'Original user policy')
        plan = self.prepare()
        os.chmod(path, 0o444)
        changed_mode = path.stat().st_mode
        try:
            with self.assertRaisesRegex(installer.InstallError, 'changed after preflight'):
                installer.apply_plan(plan)
            self.assertEqual(path.read_bytes(), b'Original user policy')
            self.assertEqual(path.stat().st_mode, changed_mode)
            self.assertFalse((self.project / installer.PRIVATE).exists())
        finally:
            os.chmod(path, 0o644)

    def test_rollback_preserves_a_concurrent_edit_to_a_written_file(self):
        self.project.mkdir()
        policy = self.project / 'AGENTS.md'
        policy.write_bytes(b'Original policy')
        plan = self.prepare()
        edited = self.project / '.agents/skills/to-spec/SKILL.md'
        real_write = installer.atomic_write
        def concurrent_edit_then_fail(path, data, mode):
            if path == self.project / installer.STATE:
                edited.write_bytes(b'User edit during installation')
                raise OSError('injected failure after user edit')
            real_write(path, data, mode)
        with patch.object(installer, 'atomic_write', side_effect=concurrent_edit_then_fail):
            with self.assertRaisesRegex(installer.InstallError, 'concurrently changed'):
                installer.apply_plan(plan)
        self.assertEqual(edited.read_bytes(), b'User edit during installation')
        self.assertEqual(policy.read_bytes(), b'Original policy')
        self.assertFalse((self.project / installer.STATE).exists())

    def test_missing_helper_and_ownership_record_cannot_pass_check(self):
        self.installed()
        registry = self.bundles['pi'].registry
        helper = registry['skills']['grilling']['canonical_path']
        (self.project / helper).unlink()
        state_path = self.project / installer.STATE
        state = json.loads(state_path.read_text(encoding='utf-8'))
        del state['files'][helper]
        state_path.write_bytes(installer.json_bytes(state))
        with self.assertRaisesRegex(installer.InstallError, 'inventory is incomplete'):
            installer.check_installation(self.project)
        with self.assertRaisesRegex(installer.InstallError, 'inventory is incomplete'):
            self.prepare()
        self.assertFalse((self.project / helper).exists())

    def test_missing_instruction_record_cannot_pass_check(self):
        self.installed()
        state_path = self.project / installer.STATE
        state = json.loads(state_path.read_text(encoding='utf-8'))
        state['instructions'] = {}
        state_path.write_bytes(installer.json_bytes(state))
        with self.assertRaisesRegex(installer.InstallError, 'instruction record'):
            installer.check_installation(self.project)

    def test_changed_source_provenance_is_refused(self):
        self.installed()
        state_path = self.project / installer.STATE
        state = json.loads(state_path.read_text(encoding='utf-8'))
        state['files']['.agents/skills/to-spec/SKILL.md']['source'] = 'README.md'
        state_path.write_bytes(installer.json_bytes(state))
        with self.assertRaisesRegex(installer.InstallError, 'provenance'):
            installer.check_installation(self.project)
        with self.assertRaisesRegex(installer.InstallError, 'provenance'):
            self.prepare()

    def test_installation_is_relocatable(self):
        self.installed()
        destination = self.base / 'Moved project'
        self.project.rename(destination)
        installer.check_installation(destination)
        registry = json.loads((destination / installer.PRIVATE / 'registry.json').read_text(encoding='utf-8'))
        for record in registry['skills'].values():
            self.assertFalse(Path(record['canonical_path']).is_absolute())
            self.assertTrue((destination / record['canonical_path']).is_file())
        self.assertNotIn(str(ROOT), (destination / installer.PRIVATE / 'WORKFLOW.md').read_text(encoding='utf-8'))

    def test_unsafe_or_source_project_targets_are_refused(self):
        for target in [ROOT, ROOT / 'upstream/matt', Path.home(), Path(self.base.anchor)]:
            with self.subTest(target=target):
                with self.assertRaises(installer.InstallError):
                    self.prepare(project=target)
        file = self.base / 'not a directory'
        file.write_bytes(b'User file')
        with self.assertRaisesRegex(installer.InstallError, 'not a directory'):
            self.prepare(project=file)
        self.assertEqual(file.read_bytes(), b'User file')

    def test_downloaded_installer_refuses_a_different_source_archive_checkout(self):
        for marker in ['scripts/install.py', 'workflow/selection.json', 'upstream/checksums.json']:
            path = self.project / marker
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'source archive marker')
        before = self.snapshot(self.project)
        with self.assertRaisesRegex(installer.InstallError, 'source/archive repository'):
            self.prepare()
        self.assertEqual(self.snapshot(self.project), before)
        self.assertFalse((self.project / installer.PRIVATE).exists())

    def test_command_works_from_an_unrelated_working_directory(self):
        command = [sys.executable, str(ROOT / 'scripts/install.py'), '--project', str(self.project), '--host', 'pi']
        preview = subprocess.run(command + ['--dry-run'], cwd=self.base, capture_output=True, text=True)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertFalse(self.project.exists())
        applied = subprocess.run(command, cwd=self.base, capture_output=True, text=True)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertIn('22 discoverable skills (21 original + combined setup)', applied.stdout)
        checked = subprocess.run([*command, '--check'], cwd=self.base, capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertIn('OK:', checked.stdout)
        repeated = subprocess.run(command, cwd=self.base, capture_output=True, text=True)
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertIn('ALREADY UP TO DATE', repeated.stdout)

    def test_list_does_not_need_or_create_a_project(self):
        output = io.StringIO()
        with patch.object(installer, 'build_bundle', return_value=self.bundles['pi']), redirect_stdout(output):
            code = installer.main(['--list', '--project', str(self.project)])
        self.assertEqual(code, 0)
        self.assertIn('22 discovery entries', output.getvalue())
        self.assertNotIn('make-bot-ui', output.getvalue())
        self.assertFalse(self.project.exists())

    def test_check_missing_installation_is_a_clean_cli_error(self):
        error = io.StringIO()
        with redirect_stderr(error):
            code = installer.main(['--check', '--project', str(self.project)])
        self.assertEqual(code, 1)
        self.assertIn('No managed workflow installation', error.getvalue())
        self.assertFalse(self.project.exists())

    @unittest.skipUnless(shutil.which('git'), 'Git is needed only for this checkout-filter test')
    def test_git_attributes_preserve_original_bytes_in_consumer(self):
        self.installed()
        subprocess.run(['git', 'init', '-q'], cwd=self.project, check=True)
        subprocess.run(['git', '-c', 'core.autocrlf=true', 'add', '.'], cwd=self.project, check=True, capture_output=True)
        rows = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=self.project).split(b'\0')
        entries = {}
        for row in rows:
            if row:
                meta, rel = row.decode().split('\t', 1)
                entries[rel] = meta.split()[1]
        algorithm = subprocess.check_output(['git', 'rev-parse', '--show-object-format'], cwd=self.project, text=True).strip()
        for rel, spec in self.bundles['pi'].files.items():
            if spec.source:
                blob = b'blob ' + str(len(spec.data)).encode() + b'\0' + spec.data
                with self.subTest(path=rel):
                    self.assertEqual(entries[rel], hashlib.new(algorithm, blob).hexdigest())


if __name__ == '__main__':
    unittest.main()
