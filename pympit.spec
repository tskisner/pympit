# -*- mode: python -*-

block_cipher = None

astart = Analysis(['bin/pympit_startup.py'],
             binaries=None,
             datas=None,
             hiddenimports=['six'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyzstart = PYZ(astart.pure, astart.zipped_data,
             cipher=block_cipher)

exestart = EXE(pyzstart,
          astart.scripts,
          astart.binaries,
          astart.zipfiles,
          astart.datas,
          name='pympit_startup',
          debug=False,
          strip=False,
          upx=False,
          console=True )

acoll = Analysis(['bin/pympit_collective.py'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyzcoll = PYZ(acoll.pure, acoll.zipped_data,
             cipher=block_cipher)

execoll = EXE(pyzcoll,
          acoll.scripts,
          acoll.binaries,
          acoll.zipfiles,
          acoll.datas,
          name='pympit_collective',
          debug=False,
          strip=False,
          upx=False,
          console=True )
