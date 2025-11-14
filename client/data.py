from core import res_path

STATUS = "Beta"
VER1 = "3.1"
VER2 = "b5"
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
名单为Excel xlsx文件，表头必须有包含“姓名”或“名字”的格，和包含“性别”的格。程序会根据这两格下面的数据识别学生名字和性别。
教室为Excel xlsx文件，程序会将所有有4个边边框，且内容为空白或学生名字的单元格视为一个座位。每组相连且背景色相同的单元格会被视为一个小组。在一个座位格子中，可以写上同学名字，相当于提前分配座位。
如果无法理解，可以看看测试数据（名单：test1.xlsx；教室：test2.xlsx）。
""".strip()
