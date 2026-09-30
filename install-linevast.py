#!/usr/bin/env python3
"""Install the public release in the confirmed ASPHAM cPanel document root."""
import argparse,hashlib,json,os,shutil,tarfile,time
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('archive',type=Path);parser.add_argument('--sha256',required=True);parser.add_argument('--root',type=Path,default=Path('/home/mcaesthe/migration-org-20260928/aspham/public'));args=parser.parse_args()
archive=args.archive.resolve();root=args.root.resolve()
if root!=Path('/home/mcaesthe/migration-org-20260928/aspham/public'):raise SystemExit('Unexpected document root')
if hashlib.sha256(archive.read_bytes()).hexdigest()!=args.sha256:raise SystemExit('Archive checksum mismatch')
release=archive.parent/('prepared-'+time.strftime('%Y%m%d-%H%M%S'));release.mkdir(mode=0o700)
with tarfile.open(archive) as tar:
 for member in tar.getmembers():
  if member.issym() or member.islnk() or os.path.commonpath([str((release/member.name).resolve()),str(release.resolve())]) != str(release.resolve()):raise SystemExit('Unsafe archive member')
 tar.extractall(release)
manifest=json.loads((release/'manifest.json').read_text())
for path,digest in manifest.items():
 file=release/'public'/path
 if hashlib.sha256(file.read_bytes()).hexdigest()!=digest:raise SystemExit('File checksum mismatch: '+path)
assert (release/'public/index.html').is_file()
backup=root.parent/('public-before-'+time.strftime('%Y%m%d-%H%M%S'))
backup_archive=archive.parent/('backup-'+time.strftime('%Y%m%d-%H%M%S')+'.tar.gz')
if root.exists():
 with tarfile.open(backup_archive,'w:gz') as tar:tar.add(root,arcname='public')
 with tarfile.open(backup_archive) as tar:assert 'public/index.html' in tar.getnames()
 if (root/'.well-known').exists():shutil.copytree(root/'.well-known',release/'public/.well-known',dirs_exist_ok=True)
 root.rename(backup)
try: (release/'public').rename(root)
except Exception:
 if backup.exists():backup.rename(root)
 raise
for path in root.rglob('*'):os.chmod(path,0o755 if path.is_dir() else 0o644)
os.chmod(root,0o755)
receipt={'installed_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'domain':'aspham.org','document_root':str(root),'archive_sha256':args.sha256,'verified_files':len(manifest),'pages':len(json.loads((release/'routes.json').read_text())),'previous_root':str(backup) if backup.exists() else None,'backup_archive':str(backup_archive) if backup_archive.exists() else None,'public_https':'not_yet_verified'}
(archive.parent/'INSTALL-RESULT.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
