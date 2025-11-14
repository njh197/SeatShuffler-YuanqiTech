import os
import data
os.system("rmdir __pycache__")
os.system('pyinstaller -F -w --add-data "icon.ico;." -i icon.ico ui.py')
os.rename("dist/ui.exe",f"dist/SeatShuffler {data.VER2}")