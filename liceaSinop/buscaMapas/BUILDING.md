# Map Extractor Desktop App

Instructions for turning `get_usb_and_excel_paths.py` in this folder into a desktop application with PyInstaller.

## 1. Environment setup
- Use a local Python 3.10+ installation on the target platform (macOS builds on macOS, Windows builds on Windows, etc. – PyInstaller does not cross‑compile).
- Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install pyinstaller
```

> `tkinterdnd2` in `requirements.txt` is optional. If it fails to install, the app falls back to the standard file picker.

## 2. Build the application

Run PyInstaller from the `liceaSinop/buscaMapas` directory using the included spec:

```bash
cd liceaSinop/buscaMapas
pyinstaller MapExtractor.spec --noconfirm
```

Artifacts:
- `dist/MapExtractor` contains the bundled application (`MapExtractor.app` on macOS, `MapExtractor.exe` inside the folder on Windows, and an executable on Linux).
- `build/` holds temporary files and can be deleted after verifying the build.

The spec automatically switches between the `.icns` and `.ico` files generated from `buscaMapasLogo.png`, so the application shows the provided logo on every platform.

## 3. Code signing & notarisation (macOS)

If you need to distribute on macOS outside your machine, consider codesigning and notarising the `.app`. Without signing, Gatekeeper may warn users. Refer to Apple’s documentation or run:

```bash
codesign --deep --force --sign "Developer ID Application: <Your Name>" dist/MapExtractor/MapExtractor.app
```

## 4. Rebuilding after changes

Any time you modify the Python sources:
1. Clean previous artifacts if desired: `rm -rf build dist MapExtractor.spec.__pycache__`.
2. Rerun the PyInstaller command above.

## 5. Troubleshooting tips
- If pandas fails to read Excel files, ensure `openpyxl` is installed (already listed in `requirements.txt`).
- For drag & drop support, install `tkinterdnd2` on the target machine before building.
- When sharing the app, distribute the entire folder generated inside `dist/MapExtractor` or use `--onefile` in the PyInstaller command if you prefer a single executable (note that startup can be slower).
