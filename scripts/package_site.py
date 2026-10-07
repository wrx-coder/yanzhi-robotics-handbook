"""打包可搬移的本地网站与维护源码，不包含缓存或测试输出。"""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parent.parent
archive=ROOT/'研知-本地科研手册.zip'
files=[ROOT/name for name in ['index.html','启动网站.sh','README.md','验证记录.md']]
for directory in ['dist','data','projects','scripts','examples']:
    files.extend(p for p in (ROOT/directory).rglob('*') if p.is_file() and not any(
        part in ['__pycache__','.git','.venv','node_modules'] for part in p.parts) and p.suffix!='.pyc')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as package:
    for path in sorted(files):
        assert not path.is_symlink()
        info=zipfile.ZipInfo('研知-本地科研手册/'+path.relative_to(ROOT).as_posix(),(2026,9,21,0,0,0))
        info.external_attr=(0o100755 if path.suffix=='.sh' else 0o100644)<<16
        package.writestr(info,path.read_bytes(),compress_type=zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(archive) as package:
    assert package.testzip() is None
    for path in files:
        member = '研知-本地科研手册/' + path.relative_to(ROOT).as_posix()
        assert package.read(member) == path.read_bytes(), member
print(f'{archive.name} · {len(files)} 个文件 · {archive.stat().st_size/1024:.1f} KB')
print('全部打包文件与工作区逐字节一致（含技能正文及离线索引）')
