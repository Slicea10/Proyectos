# -*- mode: python ; coding: utf-8 -*-
import platform
from pathlib import Path

block_cipher = None

project_root = Path(__name__).resolve().parent
script_path = project_root / "get_usb_and_excel_paths.py"
icon_png = project_root / "buscaMapasLogo.png"

system = platform.system().lower()
if system == "darwin":
    icon_file = project_root / "buscaMapasLogo.icns"
elif system == "windows":
    icon_file = project_root / "buscaMapasLogo.ico"
else:
    # Linux accepts PNG icons during desktop file creation; keep PNG for collect
    icon_file = icon_png

if not icon_file.exists():
    icon_file = icon_png

a = Analysis(
    [str(script_path)],
    pathex=[str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="MapExtractor",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(icon_file),
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MapExtractor",
)
