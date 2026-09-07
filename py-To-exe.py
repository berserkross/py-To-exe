import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
import sys


class PyToExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Python转EXE工具")
        self.root.geometry("700x700")
        self.root.resizable(True, True)

        # 变量
        self.script_path = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.path.expanduser("~\\Desktop"))
        self.icon_path = tk.StringVar()
        self.one_file = tk.BooleanVar(value=True)
        self.windowed = tk.BooleanVar(value=False)
        self.hide_console = tk.BooleanVar(value=True)
        self.add_pyinstaller = tk.BooleanVar(value=False)

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        # 主框架
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(main_frame, text="Python转EXE工具", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Python脚本路径
        script_frame = tk.Frame(main_frame)
        script_frame.pack(fill=tk.X, pady=5)
        tk.Label(script_frame, text="Python脚本:", width=12, anchor="w").pack(side=tk.LEFT)
        tk.Entry(script_frame, textvariable=self.script_path, state="readonly", width=40).pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        tk.Button(script_frame, text="选择", command=self.select_script).pack(side=tk.LEFT)

        # 输出目录
        output_frame = tk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=5)
        tk.Label(output_frame, text="输出目录:", width=12, anchor="w").pack(side=tk.LEFT)
        tk.Entry(output_frame, textvariable=self.output_dir, state="readonly", width=40).pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        tk.Button(output_frame, text="选择", command=self.select_output_dir).pack(side=tk.LEFT)

        # 图标路径
        icon_frame = tk.Frame(main_frame)
        icon_frame.pack(fill=tk.X, pady=5)
        tk.Label(icon_frame, text="图标文件:", width=12, anchor="w").pack(side=tk.LEFT)
        tk.Entry(icon_frame, textvariable=self.icon_path, state="readonly", width=40).pack(side=tk.LEFT, padx=(10, 5), fill=tk.X, expand=True)
        tk.Button(icon_frame, text="选择", command=self.select_icon).pack(side=tk.LEFT)

        # 选项框架
        options_frame = tk.LabelFrame(main_frame, text="打包选项", padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=10)

        # 单文件选项
        tk.Checkbutton(options_frame, text="打包为单个exe文件 (推荐)", variable=self.one_file).pack(anchor="w", pady=2)

        # 窗口模式选项
        tk.Checkbutton(options_frame, text="窗口模式 (GUI应用)", variable=self.windowed).pack(anchor="w", pady=2)

        # 控制台隐藏选项
        tk.Checkbutton(options_frame, text="隐藏控制台窗口 (适用于GUI应用)", variable=self.hide_console).pack(anchor="w", pady=2)

        # 自动安装PyInstaller选项
        tk.Checkbutton(options_frame, text="自动安装PyInstaller (如未安装)", variable=self.add_pyinstaller).pack(anchor="w", pady=2)

        # 操作按钮
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="开始打包", command=self.start_conversion, bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="清除缓存", command=self.clean_cache, bg="#FF9800", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="清空", command=self.clear_fields, bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=10)

        # 日志显示区域
        log_frame = tk.LabelFrame(main_frame, text="打包日志", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # 创建文本框和滚动条
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪 - 请选择Python脚本")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

    def select_script(self):
        """选择Python脚本"""
        file_path = filedialog.askopenfilename(
            title="选择Python脚本",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")]
        )
        if file_path:
            self.script_path.set(file_path)
            self.status_var.set(f"已选择脚本: {os.path.basename(file_path)}")

    def select_output_dir(self):
        """选择输出目录"""
        folder_path = filedialog.askdirectory(title="选择输出目录")
        if folder_path:
            self.output_dir.set(folder_path)
            self.status_var.set(f"已选择输出目录: {folder_path}")

    def select_icon(self):
        """选择图标文件"""
        file_path = filedialog.askopenfilename(
            title="选择图标文件",
            filetypes=[("图标文件", "*.ico"), ("所有文件", "*.*")]
        )
        if file_path:
            self.icon_path.set(file_path)
            self.status_var.set(f"已选择图标: {os.path.basename(file_path)}")

    def log_message(self, message):
        """向日志框添加消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def clean_cache(self):
        """清理PyInstaller缓存"""
        try:
            script_dir = os.path.dirname(self.script_path.get())
            cache_dirs = [
                os.path.join(script_dir, "__pycache__"),
                os.path.join(script_dir, "build"),
                os.path.join(script_dir, "dist")
            ]
            
            removed_count = 0
            for cache_dir in cache_dirs:
                if os.path.exists(cache_dir):
                    import shutil
                    shutil.rmtree(cache_dir)
                    removed_count += 1
                    self.log_message(f"已删除缓存目录: {cache_dir}")
            
            if removed_count > 0:
                messagebox.showinfo("清理完成", f"已删除 {removed_count} 个缓存目录")
            else:
                messagebox.showinfo("清理完成", "没有找到需要清理的缓存目录")
                
        except Exception as e:
            messagebox.showerror("清理失败", f"清理过程中出现错误: {e}")

    def install_pyinstaller(self):
        """安装PyInstaller"""
        try:
            self.log_message("正在安装PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            self.log_message("PyInstaller安装完成!")
            return True
        except Exception as e:
            self.log_message(f"PyInstaller安装失败: {e}")
            return False

    def convert_to_exe(self):
        """执行打包操作"""
        script_path = self.script_path.get()
        output_dir = self.output_dir.get()
        icon_path = self.icon_path.get()
        one_file = self.one_file.get()
        windowed = self.windowed.get()
        hide_console = self.hide_console.get()

        # 验证输入
        if not script_path:
            messagebox.showerror("错误", "请选择Python脚本")
            return

        if not os.path.exists(script_path):
            messagebox.showerror("错误", "Python脚本不存在")
            return

        # 检查PyInstaller是否安装
        try:
            import PyInstaller
        except ImportError:
            if self.add_pyinstaller.get():
                if not self.install_pyinstaller():
                    return
            else:
                messagebox.showerror("错误", "PyInstaller未安装。请勾选'自动安装PyInstaller'选项或手动安装。")
                return

        # 构建命令
        cmd = [sys.executable, "-m", "PyInstaller"]

        # 添加选项
        if one_file:
            cmd.append("--onefile")
        
        if windowed:
            cmd.append("--windowed")
        elif hide_console:
            cmd.append("--noconsole")
        
        if icon_path:
            cmd.extend(["--icon", icon_path])
        
        # 设置输出目录
        cmd.extend(["--distpath", output_dir])
        
        # 添加脚本路径
        cmd.append(script_path)

        self.log_message(f"开始打包: {script_path}")
        self.log_message(f"执行命令: {' '.join(cmd)}")
        self.log_message("="*50)

        try:
            # 执行PyInstaller命令
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # 实时读取输出
            for line in iter(process.stdout.readline, ''):
                self.log_message(line.rstrip())

            process.wait()

            if process.returncode == 0:
                exe_name = os.path.splitext(os.path.basename(script_path))[0] + ".exe"
                exe_path = os.path.join(output_dir, exe_name)
                if os.path.exists(exe_path):
                    self.status_var.set(f"打包成功! EXE文件位于: {exe_path}")
                    self.log_message("="*50)
                    self.log_message("打包成功!")
                    messagebox.showinfo("打包成功", f"EXE文件已生成: {exe_path}")
                else:
                    self.status_var.set("打包完成，但未找到EXE文件")
                    self.log_message("警告: 打包过程完成，但未找到预期的EXE文件")
            else:
                self.status_var.set("打包失败")
                self.log_message("错误: 打包过程失败")
                messagebox.showerror("打包失败", "打包过程中出现错误，请查看日志了解详情")

        except Exception as e:
            self.status_var.set(f"打包失败: {e}")
            self.log_message(f"错误: {e}")
            messagebox.showerror("打包失败", f"打包过程中出现错误: {e}")

    def start_conversion(self):
        """开始打包进程"""
        if not self.script_path.get():
            messagebox.showerror("错误", "请选择Python脚本")
            return

        # 在新线程中执行打包，避免界面冻结
        thread = threading.Thread(target=self.convert_to_exe)
        thread.daemon = True
        thread.start()

    def clear_fields(self):
        """清空所有字段"""
        self.script_path.set("")
        self.output_dir.set(os.path.expanduser("~\\Desktop"))
        self.icon_path.set("")
        self.one_file.set(True)
        self.windowed.set(False)
        self.hide_console.set(True)
        self.add_pyinstaller.set(False)
        self.status_var.set("就绪 - 请选择Python脚本")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = PyToExeConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
