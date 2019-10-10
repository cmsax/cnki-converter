#!/bin/bash
case "${TRAVIS_OS_NAME}" in
    osx)
        cp -vf /usr/local/lib/python2.7/site-packages/shiboken2/libshiboken2-python2.7v.5.13.dylib /usr/local/lib/python2.7/site-packages/PySide2/
        cp -vf /usr/local/lib/python2.7/site-packages/shiboken2/libshiboken2-python2.7v.5.13.dylib /usr/local/lib/python2.7/site-packages/PyInstaller/hooks/
        pyinstaller --name="CNKI-Converter-darwin" --windowed -F --icon ./icon.icns --osx-bundle-identifier cnki-converter main.py
        ;;
    windows)
        pyinstaller --name="CNKI-Converter-windows" --windowed -F main.py
        ;;
esac
