import os
import sys
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QFileDialog, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qfluentwidgets import (setTheme, Theme, PrimaryPushButton, PushButton, 
                            ComboBox, LineEdit, MessageBox, InfoBar, InfoBarPosition,
                            BodyLabel, TitleLabel, setFont, FluentIcon)

import data
import core

class InputPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.setup_ui()
        
    def setup_ui(self):
        # 标题
        title_label = TitleLabel(f"座位随机分配系统 {data.VERSION}")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)
        
        # 输入区域
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # 名单文件输入
        self.student_file_input = self.create_file_input("名单文件:", "选择txt文件", self.select_student_file)
        input_layout.addWidget(self.student_file_input)
        
        # 教室文件输入
        self.classroom_file_input = self.create_file_input("教室文件:", "选择xlsx文件", self.select_classroom_file)
        input_layout.addWidget(self.classroom_file_input)
        
        # 输出文件输入
        self.output_file_input = self.create_file_input("输出文件:", "选择位置", self.select_output_file)
        input_layout.addWidget(self.output_file_input)
        
        # 方案选择
        method_widget = QWidget()
        method_layout = QHBoxLayout(method_widget)
        method_label = BodyLabel("分配方案:")
        method_layout.addWidget(method_label)
        method_layout.addSpacing(10)
        
        self.method_combo = ComboBox()
        self.method_combo.addItems(data.METHODS)
        method_layout.addWidget(self.method_combo)
        method_layout.addStretch()
        
        input_layout.addWidget(method_widget)
        self.layout.addWidget(input_widget)
        
        # 完成按钮
        self.complete_btn = PrimaryPushButton("完成")
        self.complete_btn.clicked.connect(self.process_data)
        self.layout.addWidget(self.complete_btn, alignment=Qt.AlignRight)
        
        self.layout.addStretch()
    
    def create_file_input(self, label_text, button_text, callback):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        label = BodyLabel(label_text)
        layout.addWidget(label)
        layout.addSpacing(10)
        
        file_input = LineEdit()
        layout.addWidget(file_input, 1)  # 设置拉伸因子为1，使输入框占满剩余空间
        
        button = PushButton(button_text)
        button.clicked.connect(callback)
        layout.addWidget(button)
        
        # 保存输入框引用
        if label_text == "名单文件:":
            self.student_file_edit = file_input
        elif label_text == "教室文件:":
            self.classroom_file_edit = file_input
        elif label_text == "输出文件:":
            self.output_file_edit = file_input
        
        return widget
    
    def select_student_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "选择名单文件", "", "Text files (*.txt);;All files (*.*)"
        )
        if filename:
            self.student_file_edit.setText(filename)
    
    def select_classroom_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "选择教室文件", "", "Excel files (*.xlsx);;All files (*.*)"
        )
        if filename:
            self.classroom_file_edit.setText(filename)
    
    def select_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "选择输出文件位置", "result.xlsx", "Excel files (*.xlsx);;All files (*.*)"
        )
        if filename:
            self.output_file_edit.setText(filename)
    
    def process_data(self):
        # 获取输入值
        student_file = self.student_file_edit.text()
        classroom_file = self.classroom_file_edit.text()
        output_file = self.output_file_edit.text()
        method_index = self.method_combo.currentIndex()
        
        # 验证输入
        if not student_file:
            MessageBox("错误", "请选择名单文件！", self).exec()
            return
        
        if not classroom_file:
            MessageBox("错误", "请选择教室文件！", self).exec()
            return
        
        if not output_file:
            MessageBox("错误", "请选择输出文件位置！", self).exec()
            return
        
        try:
            # 禁用按钮，防止重复点击
            self.complete_btn.setEnabled(False)
            
            # 执行算法
            result = core.shuffle(student_file, classroom_file, method_index, output_file)
            
            # 切换到完成页面
            self.parent.switchToCompletePage(output_file)
            
            # 尝试打开结果文件
            self.open_result_file(output_file)
            
        except Exception as e:
            MessageBox("错误", f"执行过程中出现错误：\n{str(e)}", self).exec()
            # 重新启用按钮
            self.complete_btn.setEnabled(True)
    
    def open_result_file(self, result_file):
        if not os.path.exists(result_file):
            MessageBox("警告", f"未找到结果文件: {result_file}", self).exec()
            return
        
        try:
            # 根据不同操作系统打开文件
            if sys.platform == "win32":
                os.startfile(result_file)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", result_file])
            else:  # Linux
                subprocess.run(["xdg-open", result_file])
        except Exception as e:
            MessageBox("警告", f"无法自动打开结果文件: {str(e)}", self).exec()


class CompletePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.setup_ui()
        
    def setup_ui(self):
        # 完成消息
        complete_label = TitleLabel("完成！")
        complete_label.setAlignment(Qt.AlignCenter)
        complete_label.setStyleSheet("color: green;")
        self.layout.addWidget(complete_label)
        
        # 结果文件提示
        self.result_label = BodyLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)
        
        # 返回按钮
        back_btn = PrimaryPushButton("返回")
        back_btn.clicked.connect(self.parent.switchToInputPage)
        self.layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        
        self.layout.addStretch()
    
    def set_result_file(self, output_file):
        self.result_label.setText(f"结果文件已保存为 {os.path.basename(output_file)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"SeatShuffler {data.VERSION}")
        self.resize(700, 400)
        
        # 设置窗口图标
        if os.path.exists("icon.ico"):
            self.setWindowIcon(QIcon("icon.ico"))
        
        # 设置主题
        setTheme(Theme.LIGHT)
        
        # 创建堆叠窗口
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # 创建页面
        self.input_page = InputPage(self)
        self.complete_page = CompletePage(self)
        
        # 添加页面到堆叠窗口
        self.stacked_widget.addWidget(self.input_page)
        self.stacked_widget.addWidget(self.complete_page)
        
        # 显示输入页面
        self.switchToInputPage()
        
        # 创建菜单栏
        self.create_menubar()
    
    def create_menubar(self):
        # 创建菜单栏
        menubar = self.menuBar()
        
        # 添加帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        # 添加格式说明动作
        format_action = help_menu.addAction("格式说明")
        format_action.triggered.connect(self.show_format_help)
        
        # 添加关于动作
        about_action = help_menu.addAction("关于")
        about_action.triggered.connect(self.show_about)
    
    def show_about(self):
        msg = f"""
SeatShuffler {data.VERSION}
Copyright (C) 2025 元气科技工作室 YuanqiTech Studio. All rights reserved.

第三方许可证信息: 
Python (Python License)
OpenPyXL (MIT License)
Pyinstaller (GPLv2 with addition)
PySide6 (LGPL-3.0-only)
QFluentWidgets (GPL-3.0)
""".strip()
        MessageBox("关于", msg, self).exec()
    
    def show_format_help(self):
        help_text = """名单文件格式说明：
        
每行一个学生姓名，一个性别，例如：
张三 男
李四 男
王五 女
...

请确保使用UTF-8编码保存文件。"""
        MessageBox("格式说明", help_text, self).exec()
    
    def switchToInputPage(self):
        self.stacked_widget.setCurrentWidget(self.input_page)
        # 重新启用完成按钮
        self.input_page.complete_btn.setEnabled(True)
    
    def switchToCompletePage(self, output_file):
        self.complete_page.set_result_file(output_file)
        self.stacked_widget.setCurrentWidget(self.complete_page)


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    if os.path.exists("icon.ico"):
        app.setWindowIcon(QIcon("icon.ico"))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()