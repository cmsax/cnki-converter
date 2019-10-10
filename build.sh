#!/bin/bash
case "${TRAVIS_OS_NAME}" in
    osx)
        pyinstaller --name="CNKI-Converter-darwin" --windowed -F --icon ./icon.icns --osx-bundle-identifier cnki-converter main.py
        ;;
    linux)
        pyinstaller --name="CNKI-Converter-linux" --windowed -F main.py
        ;;
    windows)
        pyinstaller --name="CNKI-Converter-windows" --windowed -F main.py
        ;;
esac
