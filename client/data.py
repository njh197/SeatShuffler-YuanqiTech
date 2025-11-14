# import logging # TODO
from core import res_path

STATUS = "Beta"
VER1 = "3.0"
VER2 = "b4"
VERSION = f"{STATUS} {VER1} ({VER2})"
METHODS = ["男女混合", "男女分开", "完全随机"]

ICON = res_path('icon.ico')

ABOUT_TEXT = f"""
SeatShuffler {VERSION} By 元气科技工作室 (25年末重生版)
此项目按GPL v3许可证开源。

第三方许可证信息: 
Python (Python License)
OpenPyXL (MIT License)
Pyinstaller (GPLv2 with addition)
PySide6 (LGPL-3.0-only)
QFluentWidgets (GPL-3.0)
""".strip()
HELP_TEXT = """
TODO
请参考测试数据
""".strip()
