"""Private GitHub bootstrap tests; no network or real project mutation."""
from contextlib import redirect_stderr
import importlib.util
import io
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('github_bootstrap', ROOT / 'install.py')
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


def archive_bytes(entries=None):
    buffer = io.BytesIO()
    raw_names = []
    with zipfile.ZipFile(buffer, 'w') as archive:
        for name, data, mode in entries or [
            ('repo-main/scripts/install.py', b'# fixture installer\n', stat.S_IFREG | 0o755),
            ('repo-main/workflow/selection.json', b'{}\n', stat.S_IFREG | 0o644),
        ]:
            info = zipfile.ZipInfo(name)
            if info.filename != name:
                raw_names.append((info.filename.encode(), name.encode()))
            info.external_attr = mode << 16
            archive.writestr(info, data)
    result = buffer.getvalue()
    for normalized, original in raw_names:
        if len(normalized) != len(original):
            raise ValueError('Fixture filename substitution must preserve ZIP header lengths')
        result = result.replace(normalized, original)
    return result


class GitHubBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='maks-bootstrap-test-')
        self.addCleanup(self.temporary.cleanup)
        self.destination = Path(self.temporary.name).resolve() / 'source'
        self.destination.mkdir()

    def test_extracts_valid_source_without_rewriting_files(self):
        root = bootstrap.extract_source(archive_bytes(), self.destination)
        self.assertEqual(root.name, 'repo-main')
        self.assertEqual((root / 'scripts/install.py').read_bytes(), b'# fixture installer\n')
        if os.name != 'nt':
            self.assertTrue((root / 'scripts/install.py').stat().st_mode & 0o111)

    def test_archive_paths_cannot_escape_or_use_windows_drive_syntax(self):
        for name in ['../escape', '/absolute', 'repo-main/../../escape', 'C:/escape', 'repo-main\\escape']:
            with self.subTest(path=name):
                data = archive_bytes([
                    ('repo-main/scripts/install.py', b'# fixture', stat.S_IFREG | 0o644),
                    (name, b'untrusted', stat.S_IFREG | 0o644),
                ])
                with self.assertRaisesRegex(bootstrap.BootstrapError, 'Unsafe source archive path'):
                    bootstrap.extract_source(data, self.destination)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_symlink_and_special_entries_are_refused(self):
        for mode in [stat.S_IFLNK | 0o777, stat.S_IFIFO | 0o644]:
            data = archive_bytes([
                ('repo-main/scripts/install.py', b'# fixture', stat.S_IFREG | 0o644),
                ('repo-main/link', b'../../outside', mode),
            ])
            with self.assertRaisesRegex(bootstrap.BootstrapError, 'Linked or special'):
                bootstrap.extract_source(data, self.destination)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_duplicate_case_colliding_paths_are_refused(self):
        data = archive_bytes([
            ('repo-main/scripts/install.py', b'one', stat.S_IFREG | 0o644),
            ('repo-main/scripts/INSTALL.py', b'two', stat.S_IFREG | 0o644),
        ])
        with self.assertRaisesRegex(bootstrap.BootstrapError, 'Duplicate'):
            bootstrap.extract_source(data, self.destination)

    def test_missing_installer_or_multiple_roots_are_refused(self):
        with self.assertRaisesRegex(bootstrap.BootstrapError, 'does not contain'):
            bootstrap.extract_source(archive_bytes([('repo-main/README.md', b'Nothing', stat.S_IFREG | 0o644)]), self.destination)
        data = archive_bytes([
            ('repo-main/scripts/install.py', b'# fixture', stat.S_IFREG | 0o644),
            ('another-root/file', b'Unexpected', stat.S_IFREG | 0o644),
        ])
        with self.assertRaisesRegex(bootstrap.BootstrapError, 'one GitHub source archive root'):
            bootstrap.extract_source(data, self.destination)

    def test_archive_size_limits_are_checked_before_extraction(self):
        data = archive_bytes()
        with patch.object(bootstrap, 'MAX_ARCHIVE_BYTES', 1):
            with self.assertRaisesRegex(bootstrap.BootstrapError, 'size limit'):
                bootstrap.extract_source(data, self.destination)
        with patch.object(bootstrap, 'MAX_EXTRACTED_BYTES', 1):
            with self.assertRaisesRegex(bootstrap.BootstrapError, 'extracted size limit'):
                bootstrap.extract_source(data, self.destination)
        with patch.object(bootstrap, 'MAX_MEMBERS', 1):
            with self.assertRaisesRegex(bootstrap.BootstrapError, 'too many members'):
                bootstrap.extract_source(data, self.destination)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_download_preserves_caller_cwd_args_exit_code_and_cleans_up(self):
        caller = Path.cwd()
        delegated = []
        def run(command, **kwargs):
            self.assertEqual(kwargs['cwd'], caller)
            self.assertEqual(command[0], sys.executable)
            entry = Path(command[1])
            self.assertTrue(entry.is_file())
            self.assertEqual(command[2:], ['--project', '.', '--host', 'pi', '--dry-run'])
            delegated.append(entry)
            return subprocess.CompletedProcess(command, 7)
        with patch.object(bootstrap, 'download_source', return_value=archive_bytes()), patch.object(bootstrap.subprocess, 'run', side_effect=run):
            self.assertEqual(bootstrap.main(['--project', '.', '--host', 'pi', '--dry-run']), 7)
        self.assertEqual(len(delegated), 1)
        self.assertFalse(delegated[0].exists())
        self.assertEqual(Path.cwd(), caller)

    def test_private_download_uses_authenticated_github_cli_and_is_size_bounded(self):
        data = archive_bytes()
        with patch.object(bootstrap.shutil, 'which', return_value='gh'), patch.object(bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess(['gh'], 0, data, b'')) as run:
            self.assertEqual(bootstrap.download_source(), data)
        self.assertEqual(run.call_args.args[0], ['gh', 'api', 'repos/MakCoder-2004/maks-agentic-workflow/zipball/main'])
        self.assertTrue(run.call_args.kwargs['capture_output'])
        self.assertEqual(run.call_args.kwargs['timeout'], 180)
        with patch.object(bootstrap.shutil, 'which', return_value='gh'), patch.object(bootstrap.subprocess, 'run', return_value=subprocess.CompletedProcess(['gh'], 0, data, b'')), patch.object(bootstrap, 'MAX_ARCHIVE_BYTES', 2):
            with self.assertRaisesRegex(bootstrap.BootstrapError, 'size limit'):
                bootstrap.download_source()

    def test_private_repository_requires_authenticated_github_cli(self):
        with patch.object(bootstrap.shutil, 'which', return_value=None), patch.object(bootstrap.subprocess, 'run') as run:
            with self.assertRaisesRegex(bootstrap.BootstrapError, 'private.*gh auth login'):
                bootstrap.download_source()
        run.assert_not_called()

    def test_download_failure_never_invokes_the_curated_installer(self):
        error = io.StringIO()
        with patch.object(bootstrap, 'download_source', side_effect=OSError('download failed')), patch.object(bootstrap.subprocess, 'run') as run, redirect_stderr(error):
            self.assertEqual(bootstrap.main(['--list']), 1)
        run.assert_not_called()
        self.assertIn('download failed', error.getvalue())

    def test_invalid_archive_never_invokes_the_curated_installer(self):
        error = io.StringIO()
        with patch.object(bootstrap, 'download_source', return_value=b'not a zip'), patch.object(bootstrap.subprocess, 'run') as run, redirect_stderr(error):
            self.assertEqual(bootstrap.main(['--list']), 1)
        run.assert_not_called()
        self.assertIn('ERROR:', error.getvalue())

    def test_network_timeout_is_reported(self):
        error = io.StringIO()
        with patch.object(bootstrap, 'download_source', side_effect=TimeoutError('request timed out')), redirect_stderr(error):
            self.assertEqual(bootstrap.main(['--list']), 1)
        self.assertIn('request timed out', error.getvalue())

    def test_empty_bootstrap_body_is_not_silently_successful(self):
        loader = "import sys;code=b'';code or sys.exit('Download failed');exec(compile(code,'<github-install>','exec'))"
        result = subprocess.run([sys.executable, '-c', loader, '--project', '.', '--host', 'pi'], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Download failed', result.stderr)


if __name__ == '__main__':
    unittest.main()
