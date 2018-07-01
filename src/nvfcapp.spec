# -*- mode: python -*-

block_cipher = None


a = Analysis(['nvfcapp.py'],
             pathex=['/home/m6d/Documents/nvfcApp/src'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

nvfc_ui = [('nvfcapp.ui','/home/m6d/Documents/nvfcApp/src/nvfcapp.ui', 'DATA')]
nvfc_images = [('nvfcApp_128x128.png', '/home/m6d/Documents/nvfcApp/src/nvfcApp_128x128.png', 'DATA')]
nvfc_images += [('chart_32x32.png', '/home/m6d/Documents/nvfcApp/src/chart_32x32.png', 'DATA')]
nvfc_images += [('info_32x32.png', '/home/m6d/Documents/nvfcApp/src/info_32x32.png', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='nvfcapp',
          debug=False,
          strip=False,
          upx=True,
          icon="/home/m6d/Documents/nvfcApp/nvfcApp_64x64.png",
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas + nvfc_ui + nvfc_images,
               strip=False,
               upx=True,
               icon="/home/m6d/Documents/nvfcApp/nvfcApp_64x64.png",
               name='nvfcapp')
