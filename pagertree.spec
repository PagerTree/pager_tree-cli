import os
import inspect
import pkgutil
import importlib

# Dynamically collect all submodules in 'commands'
# Use the directory of this spec file to locate 'commands/'
spec_dir = os.path.dirname(os.path.abspath(inspect.getfile(lambda: None)))
commands_dir = os.path.join(spec_dir, "commands")

# Dynamically collect all submodules in 'commands'
hiddenimports = []
for _, module_name, _ in pkgutil.iter_modules([commands_dir]):
    hiddenimports.append(f"commands.{module_name}")

# Debugging: Print the collected modules to verify
print("Hidden imports from 'commands':", hiddenimports)

a = Analysis(
    ['pagertree.py'],
    pathex=[spec_dir],  # Add spec_dir to pathex to ensure module resolution
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pagertree',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)