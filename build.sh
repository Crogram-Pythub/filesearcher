# _*_ coding:utf-8 _*_

pyinstaller\
    --clean\
    --noconfirm\
    -w\
    build.spec

# or shell
# pyinstaller -F -w --clean -y src/app.py

# sign app
# chmod +x dist/文件搜索工具.app/Contents/MacOS/文件搜索工具
# sudo codesign --force --deep --sign - ./dist/文件搜索工具.app

