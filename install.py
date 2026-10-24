#!/usr/bin/env python3
"""Private GitHub entry point: authenticated temporary download, install, cleanup.

Requires Python 3.10+ and GitHub CLI access to this private repository. It does
not require a permanent clone. All installer arguments and caller-relative
project paths are preserved; temporary source is removed after installation.
"""
from __future__ import annotations

import io
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

REPOSITORY = 'MakCoder-2004/maks-agentic-workflow'
REF = 'main'
MAX_ARCHIVE_BYTES = 64 * 1024 * 1024
MAX_EXTRACTED_BYTES = 256 * 1024 * 1024
MAX_MEMBERS = 10000


class BootstrapError(Exception):
    pass


def extract_source(data: bytes, destination: Path) -> Path:
    """Extract only validated regular files/directories from a GitHub ZIP."""
    if len(data) > MAX_ARCHIVE_BYTES:
        raise BootstrapError('The downloaded source archive exceeds the size limit.')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = archive.infolist()
        if not members or len(members) > MAX_MEMBERS:
            raise BootstrapError('The source archive is empty or has too many members.')
        if sum(member.file_size for member in members) > MAX_EXTRACTED_BYTES:
            raise BootstrapError('The source archive exceeds the extracted size limit.')
        roots, seen = set(), set()
        for member in members:
            raw_name = member.orig_filename
            path = PurePosixPath(raw_name)
            if (not path.parts or path.is_absolute() or '..' in path.parts
                    or '\\' in raw_name or ':' in raw_name
                    or '\0' in raw_name):
                raise BootstrapError(f'Unsafe source archive path: {member.filename!r}')
            key = path.as_posix().casefold()
            if key in seen:
                raise BootstrapError(f'Duplicate source archive path: {member.filename!r}')
            seen.add(key)
            roots.add(path.parts[0])
            kind = stat.S_IFMT(member.external_attr >> 16)
            if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise BootstrapError(f'Linked or special source archive entry: {member.filename!r}')
        if len(roots) != 1:
            raise BootstrapError('Expected one GitHub source archive root.')
        prefix = next(iter(roots))
        if f'{prefix}/scripts/install.py'.casefold() not in seen:
            raise BootstrapError('The GitHub archive does not contain scripts/install.py.')
        for member in members:
            target = destination.joinpath(*PurePosixPath(member.filename).parts)
            if not target.resolve().is_relative_to(destination.resolve()):
                raise BootstrapError('The source archive path escapes the temporary directory.')
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, target.open('wb') as output:
                shutil.copyfileobj(source, output)
            os_mode = 0o755 if (member.external_attr >> 16) & 0o111 else 0o644
            target.chmod(os_mode)
    return destination / prefix


def download_source() -> bytes:
    gh = shutil.which('gh')
    if not gh:
        raise BootstrapError('This repository is private. Install GitHub CLI, run gh auth login, and confirm repository access.')
    try:
        result = subprocess.run([gh, 'api', f'repos/{REPOSITORY}/zipball/{REF}'],
                                capture_output=True, timeout=180)
    except subprocess.TimeoutExpired as error:
        raise BootstrapError('Timed out downloading the private GitHub installer source.') from error
    if result.returncode:
        detail = result.stderr.decode('utf-8', errors='replace').strip()
        raise BootstrapError('Cannot download the private source. Check gh auth status and repository access.'
                             + ('\\n' + detail if detail else ''))
    if len(result.stdout) > MAX_ARCHIVE_BYTES:
        raise BootstrapError('The downloaded source archive exceeds the size limit.')
    return result.stdout


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    caller = Path.cwd()
    try:
        data = download_source()
        with tempfile.TemporaryDirectory(prefix='maks-github-install-') as temporary:
            source = extract_source(data, Path(temporary))
            # Do not chdir to the source: relative --project paths belong to caller.
            process = subprocess.run([sys.executable, str(source / 'scripts/install.py'), *arguments], cwd=caller)
            return process.returncode
    except (BootstrapError, OSError, ValueError, zipfile.BadZipFile) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
