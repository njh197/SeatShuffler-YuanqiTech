import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import sys
import data
import core

class SeatShufflerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"SeatShuffler {data.VERSION}")
        self.root.geometry("600x450")
        self.root.resizable(False, False)  # 锁定窗口大小
        self.root.iconbitmap(core.res_path('icon.ico'))
        
        # 设置字体
        self.font_style = ("宋体", 14)
        
        # 初始化保存的路径
        self.saved_student_path = ""
        self.saved_classroom_path = ""
        self.saved_output_path = ""
        self.saved_method = "请选择"
        
        # 创建菜单栏
        self.create_menubar()
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 显示输入页面
        self.show_input_page()
    
    def create_menubar(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 添加"关于"菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="格式说明", command=self.show_format_help)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def show_about(self):
        """显示关于信息"""
        msg = f"""
SeatShuffler {data.VERSION}
Copyright (C) 2025 元气科技工作室 YuanqiTech Studio. All rights reserved.

第三方许可证信息: 
Python (Python License)
OpenPyXL (MIT License)
Pyinstaller (GPLv2 with addition)
""".strip()
        messagebox.showinfo("关于", msg)
    
    def show_input_page(self):
        """显示输入页面"""
        # 清除现有内容
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # 标题
        title_label = tk.Label(
            self.main_frame, 
            text=f"SeatShuffler 座位随机分配系统", 
            font=("宋体", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # 输入框架
        input_frame = tk.Frame(self.main_frame)
        input_frame.pack(fill="both", expand=True, pady=20)
        
        # 名单输入
        self.create_file_input(input_frame, "名单文件:", "选择txt文件", self.select_student_file, 0)
        
        # 教室输入
        self.create_file_input(input_frame, "教室文件:", "选择xlsx文件", self.select_classroom_file, 1)
        
        # 输出文件输入
        self.create_file_input(input_frame, "输出文件:", "选择位置", self.select_output_file, 2, is_output=True)
        
        # 方案选择
        method_frame = tk.Frame(input_frame)
        method_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        
        method_label = tk.Label(method_frame, text="分配方案:", font=self.font_style)
        method_label.pack(side="left", padx=(0, 10))
        
        self.method_var = tk.StringVar()
        self.method_combo = ttk.Combobox(
            method_frame, 
            textvariable=self.method_var,
            values=data.METHODS,
            state="readonly",
            font=self.font_style,
            width=10
        )
        self.method_combo.pack(side="left")
        
        # 设置保存的值
        self.file_vars["名单"].set(self.saved_student_path)
        self.file_vars["教室"].set(self.saved_classroom_path)
        self.file_vars["输出"].set(self.saved_output_path)
        self.method_var.set(self.saved_method)
        
        # 完成按钮
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(side="bottom", fill="x", pady=20)
        
        self.complete_btn = tk.Button(
            button_frame,
            text="完成",
            font=self.font_style,
            command=self.process_data,
            bg="#4CAF50",
            fg="white",
            width=10
        )
        self.complete_btn.pack(side="right")
    
    def create_file_input(self, parent, label_text, button_text, command, row, is_output=False):
        """创建文件输入行"""
        frame = tk.Frame(parent)
        frame.grid(row=row, column=0, columnspan=3, sticky="ew", pady=10)
        
        # 标签
        label = tk.Label(frame, text=label_text, font=self.font_style)
        label.pack(side="left", padx=(0, 10))
        
        # 文件路径显示
        self.file_vars = getattr(self, 'file_vars', {})
        var_name = label_text.replace(":", "").replace("文件", "")
        self.file_vars[var_name] = tk.StringVar()
        
        # 输入框
        entry = tk.Entry(
            frame, 
            textvariable=self.file_vars[var_name],
            font=self.font_style,
            width=25
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 选择文件按钮
        file_btn = tk.Button(
            frame,
            text=button_text,
            font=self.font_style,
            command=command
        )
        file_btn.pack(side="left")
    
    def select_student_file(self):
        """选择学生名单文件"""
        filename = filedialog.askopenfilename(
            title="选择名单文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_vars["名单"].set(filename)
            self.saved_student_path = filename
    
    def select_classroom_file(self):
        """选择教室文件"""
        filename = filedialog.askopenfilename(
            title="选择教室文件",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.file_vars["教室"].set(filename)
            self.saved_classroom_path = filename
    
    def select_output_file(self):
        """选择输出文件位置"""
        filename = filedialog.asksaveasfilename(
            title="选择输出文件位置",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if filename:
            self.file_vars["输出"].set(filename)
            self.saved_output_path = filename
    
    def show_format_help(self):
        """显示文件格式说明"""
        help_text = """名单文件格式说明：
        
每行一个学生姓名，一个性别，例如：
张三 男
李四 男
王五 女
...

请确保使用UTF-8编码保存文件。"""
        messagebox.showinfo("格式说明", help_text)
    
    def process_data(self):
        """处理数据并执行算法"""
        # 验证输入
        student_file = self.file_vars["名单"].get()
        classroom_file = self.file_vars["教室"].get()
        output_file = self.file_vars["输出"].get()
        method_index = self.method_combo.current()
        
        # 保存当前选择
        self.saved_student_path = student_file
        self.saved_classroom_path = classroom_file
        self.saved_output_path = output_file
        self.saved_method = self.method_var.get()
        
        if not student_file:
            messagebox.showerror("错误", "请选择名单文件！")
            return
        
        if not classroom_file:
            messagebox.showerror("错误", "请选择教室文件！")
            return
        
        if not output_file:
            messagebox.showerror("错误", "请选择输出文件位置！")
            return
        
        if method_index == -1:
            messagebox.showerror("错误", "请选择分配方案！")
            return
        
        try:
            # 禁用按钮，防止重复点击
            self.complete_btn.config(state="disabled")
            
            # 执行算法，传递输出文件路径作为参数
            result = core.shuffle(student_file, classroom_file, method_index, output_file)
            
            # 显示完成页面
            self.show_complete_page(output_file)
            
            # 尝试打开结果文件
            self.open_result_file(output_file)
            
        except Exception as e:
            messagebox.showerror("错误", f"执行过程中出现错误：\n{str(e)}")
            # 重新启用按钮
            self.complete_btn.config(state="normal")
    
    def open_result_file(self, result_file):
        """打开结果文件"""
        if not os.path.exists(result_file):
            messagebox.showwarning("警告", f"未找到结果文件: {result_file}")
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
            messagebox.showwarning("警告", f"无法自动打开结果文件: {str(e)}")
    
    def show_complete_page(self, output_file):
        """显示完成页面"""
        # 清除现有内容
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # 完成消息
        complete_label = tk.Label(
            self.main_frame,
            text="完成！",
            font=("宋体", 24, "bold"),
            fg="green"
        )
        complete_label.pack(expand=True)
        
        # 结果文件提示
        result_label = tk.Label(
            self.main_frame,
            text=f"结果文件已保存为 {os.path.basename(output_file)}",
            font=self.font_style
        )
        result_label.pack(pady=10)
        
        # 返回按钮
        back_btn = tk.Button(
            self.main_frame,
            text="返回",
            font=self.font_style,
            command=self.show_input_page,
            width=10
        )
        back_btn.pack(side="bottom", pady=20)

def main():
    root = tk.Tk()
    app = SeatShufflerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()