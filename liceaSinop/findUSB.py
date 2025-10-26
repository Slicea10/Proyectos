import os
import platform
from pathlib import Path

def _find_on_macos(label: str):
    """Find a USB volume by label on macOS."""
    vols = Path("/Volumes")
    if not vols.exists():
        return None
    for p in vols.iterdir():
        if p.is_dir() and p.name.strip().lower() == label.lower():
            return str(p.resolve())
    return None

def _find_on_linux(label: str):
    """Find a USB volume by label on Linux."""
    candidates = [
        Path("/media") / os.environ.get("USER", ""),
        Path("/run/media") / os.environ.get("USER", ""),
        Path("/media"),
        Path("/mnt"),
    ]
    for base in candidates:
        if base.exists():
            for p in base.iterdir():
                if p.is_dir() and p.name.strip().lower() == label.lower():
                    return str(p.resolve())
    return None

def _find_on_windows(label: str):
    """Find a USB volume by label on Windows."""
    import string
    import ctypes
    from ctypes import wintypes

    GetLogicalDrives = ctypes.windll.kernel32.GetLogicalDrives
    GetVolumeInformationW = ctypes.windll.kernel32.GetVolumeInformationW

    drive_bitmask = GetLogicalDrives()
    for i, letter in enumerate(string.ascii_uppercase):
        if drive_bitmask & (1 << i):
            root = f"{letter}:\\"
            vol_name_buf = ctypes.create_unicode_buffer(261)
            fs_name_buf = ctypes.create_unicode_buffer(261)
            serial = wintypes.DWORD()
            max_comp_len = wintypes.DWORD()
            fs_flags = wintypes.DWORD()
            ok = GetVolumeInformationW(
                wintypes.LPCWSTR(root),
                vol_name_buf,
                len(vol_name_buf),
                ctypes.byref(serial),
                ctypes.byref(max_comp_len),
                ctypes.byref(fs_flags),
                fs_name_buf,
                len(fs_name_buf)
            )
            if ok and vol_name_buf.value.strip().lower() == label.lower():
                return root
    return None

def getUSBRoute(label: str = "KINGSTON"):
    """
    Return the path of a USB drive with the given volume label.
    Works on macOS, Windows, and Linux.
    Returns None if not found.
    """
    sysname = platform.system().lower()
    if "darwin" in sysname or "mac" in sysname:
        return _find_on_macos(label)
    elif "windows" in sysname:
        return _find_on_windows(label)
    else:
        return _find_on_linux(label)
