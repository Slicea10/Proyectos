# BuscaMapas.spec
block_cipher = None

a = Analysis(
    ['get_usb_and_excel_paths.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinterdnd2'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='BuscaMapas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,                  # no console window
    icon='buscaMapasLogo.ico'       # on macOS change to .icns
)

app = BUNDLE(
    exe,
    name='BuscaMapas.app',
    icon='buscaMapasLogo.icns',
    bundle_identifier=None,
)
