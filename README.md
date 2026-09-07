# py-To-exe

Python 脚本转可执行文件图形前端（Tkinter + subprocess 调用 PyInstaller）。可选单文件/单目录、窗口模式、隐藏控制台、自定义图标、自动安装 PyInstaller、清 build/dist/__pycache__、实时打包日志。面向不想记命令行的同学把自己的小工具打成 exe。

## Features
- 选择 .py 脚本、输出目录、.ico 图标
- 选项：--onefile 单文件 / --windowed 窗口 / --noconsole 隐藏控制台 / 自动 pip 安装 PyInstaller
- 后台线程跑 PyInstaller，界面不卡死，TextBox 实时显示 stdout/stderr
- 一键清缓存：删除脚本所在目录的 __pycache__、build、dist
- 未检测到 PyInstaller 时按勾选自动 pip install
- 状态栏 + 成功/失败弹窗，输出 exe 路径

## Requirements
- Python 3.8+（PyInstaller 6.x 支持 3.8+；打什么版本目标建议在对应系统本机打）[3](@ref)
- Tkinter（标准库；Linux 补 python3-tk）
- PyInstaller（工具可自动装；或手动 pip install pyinstaller）[3](@ref)

## Install
git clone https://github.com/berserkross/py-To-exe.git
cd py-To-exe
pip install pyinstaller
python py-To-exe.py

## Usage
1. 选择脚本，例如 ContinuousPaste.py
2. 输出目录默认桌面，可改
3. 选项：
   - GUI 程序（Tkinter/PyQt）：勾单文件 + 窗口模式 + 隐藏控制台
   - 命令行程序：单文件，不勾窗口/不勾隐藏控制台
4. 可选图标 .ico
5. 开始打包；完成后到输出目录取 <脚本名>.exe
等效命令行（工具后台生成类似命令）：
   python -m PyInstaller --onefile --noconsole --icon=app.ico --distpath OUT script.py
窗口程序也可 --windowed；多文件/资源用 --add-data；隐式缺失模块用 --hidden-import。[6,11,15](@ref)

## Platform notes
- PyInstaller 不是交叉编译器：在 Windows 打 Windows exe，在 macOS 打 macOS 应用，在 Linux 打 Linux 可执行文件；不能一台机器出三平台。[3](@ref)
- Windows：单文件启动会解压到临时目录，稍慢；杀软可能误报单文件，重要分发用代码签名或改 --onedir。[8,11](@ref)
- macOS：GUI 用 --windowed --noconsole；若分发给别人通常还要签名/授权，单纯自己用可先不打签。
- Linux：可打无控制台 ELF，但本工具 UI 默认按 Windows 路径/桌面输出写，Linux 自行改输出目录。
- 第三方依赖：如果脚本用 numpy/Pillow/pyautogui 等，确保在打包环境已 pip 安装；PyInstaller 大多自动收集，少数需 --hidden-import 或 --add-data。[14,15](@ref)

## Use cases
把自己写的 Tkinter 小工具、数据处理脚本、实验室内部工具打包给不装 Python 的同学运行。

## Known limitations
- 当前 UI 输出路径、默认桌面按 Windows 风格；非 Windows 需手动改输出目录
- 不生成/编辑 .spec，不处理复杂隐藏导入、二进制、动态库路径
- 不带代码签名、不带 Updater、不带 NSIS/Inno 安装包
- 大项目建议先用 --onedir 调试，再切 --onefile 分发
