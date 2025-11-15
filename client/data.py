import os, sys, tomllib, logging

STATUS = "Beta"
VER1 = "4.0"
VER2 = "b6"
VERSION = f"{STATUS} {VER1} ({VER2})"
METHODS = ["男女混合", "男女分开", "完全随机"]

def res_path(relative_path):
    """获取打包后资源文件的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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

if not os.path.exists('config.toml'):
    with open('config.toml', 'w', encoding = 'utf8') as f:
        data = '''log_level = "info"
'''
        f.write(data)

with open('config.toml', 'rb') as f:
    data = tomllib.load(f)

log_level = {"debug":logging.DEBUG, "info":logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL,
             0:logging.DEBUG, 1:logging.info, 2:logging.WARNING, 3:logging.ERROR, 4:logging.CRITICAL}[data['log_level']]

class Logger:
    def __init__(self, logname="SeatShuffler.log", loglevel=log_level, loggername=None):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(loglevel)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(loglevel)
        if not self.logger.handlers:
            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            # 定义handler的输出格式
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            formatter = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)s:%(lineno)d: %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            # 给logger添加handler
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
            
            self.logger.debug("add handler")
        self.logger.debug("set logger")
    def getlog(self):
        self.logger.debug("get logger")
        return self.logger
