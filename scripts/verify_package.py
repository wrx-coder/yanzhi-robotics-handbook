"""解压完整交付包、离线重建，核对打包内容与重建输出逐字节一致。"""
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory(prefix='yanzhi-package-') as temp:
    with zipfile.ZipFile(ROOT/'研知-本地科研手册.zip') as package:
        assert package.testzip() is None
        package.extractall(temp)
        unpacked = Path(temp)/'研知-本地科研手册'
        before = {name:package.read(name) for name in package.namelist() if not name.endswith('/')}
    for script in ['make_embodied.py','make_learning.py','make_errors.py','make_projects.py','make_chapters.py','build.py','verify_content.py']:
        subprocess.run([sys.executable,str(unpacked/'scripts'/script)],check=True,cwd=unpacked,stdout=subprocess.DEVNULL)
    for name, contents in before.items():
        relative=Path(name).relative_to('研知-本地科研手册')
        assert (unpacked/relative).read_bytes()==contents, f'重建发生变化：{relative}'
        assert (ROOT/relative).read_bytes()==contents, f'工作区与交付包不同：{relative}'
    print(f'PASS 完整 ZIP 解压后离线重建，{len(before)} 个文件与交付包、工作区逐字节一致')
