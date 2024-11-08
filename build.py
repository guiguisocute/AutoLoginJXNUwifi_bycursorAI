import PyInstaller.__main__
import os

# 确保assets目录存在
if not os.path.exists('assets'):
    os.makedirs('assets')

# 确保config.json存在
if not os.path.exists('config.json'):
    with open('config.json', 'w') as f:
        f.write('{}')

PyInstaller.__main__.run([
    'main.py',
    '--name=JXNU校园网登录器',
    '--windowed',
    '--onefile',
    '--icon=assets/icon.ico',
    '--add-data=assets/icon.ico;assets',
    '--add-data=config.json;.',
    '--clean',
    '--noconfirm'
]) 