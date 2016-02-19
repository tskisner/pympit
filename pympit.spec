# -*- mode: python -*-

block_cipher = None

scripts = [
    'pympit_startup',
    'pympit_collective',
    'pympit_fork'
]

for scr in scripts:
    a = Analysis(['bin/{}.py'.format(scr)],
        binaries=None,
        datas=None,
        hiddenimports=[],
        hookspath=[],
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher)

    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

    exe = EXE(pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name=scr,
        debug=False,
        strip=False,
        upx=False,
        console=True)
