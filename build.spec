[setup]
description = HTML to EXE Converter with Electron Support
version = 1.0.2
title = HTML to EXE

[files]
main.py = 
config.json = 

[requires]
tkinter = 
json = 
shutil = 
os = 

[commands]
pyinstaller --onefile --windowed main.py -n htmltoexe