#!/bin/bash

wine python -m nuitka --jobs=$(nproc) --standalone \
    --onefile --mingw64 --lto=no --assume-yes-for-downloads \
    --windows-console-mode=attach \
    --include-data-dir=data=data \
    --onefile-windows-splash-screen-image=data/splash.png \
    --windows-icon-from-ico=data/icon.ico \
    --company-name="Koeger" --product-name="Bumo-GCode" \
    --file-version=x.x.x --product-version=x.x.x \
    --file-description="Bumo-GCode" --copyright="2026" \
    --output-filename=app.exe src/app.py
