import mimetypes
import os
import sys
import webview
import logging
import ctypes

# 设置 DPI 感知（必须在创建窗口前设置）
if sys.platform == 'win32':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# 导入自定义模块
from src.utils.logger import setup_logging, log_startup_info
from src.utils.api import Api, load_window_config
from src.utils.cache_manager import clear_webview_cache

# 配置选项
CONFIG = {
    # 日志配置
    'enable_file_logging_in_production': True,   # 打包后是否启用文件日志
    'use_pywebview_directory': True,             # 是否使用pywebview目录
    
    # 缓存配置
    'clear_cache_on_startup': False,             # 启动时是否清除缓存 (开发时可设为True)
}

# 设置日志
log_file_path, logs_directory = setup_logging(
    CONFIG['enable_file_logging_in_production'],
    CONFIG['use_pywebview_directory']
)

# 记录程序启动信息
log_startup_info(
    log_file_path, 
    logs_directory, 
    CONFIG['enable_file_logging_in_production'],
    CONFIG['use_pywebview_directory']
)

# 配置关闭提示
chinese = {
    'global.quitConfirmation': '暂别勿思念，转瞬与亲见',
}

if getattr(sys, 'frozen', None):
    web_dir = os.path.join(sys._MEIPASS, 'gui')
else:
    web_dir = os.path.join(os.path.abspath("."), 'gui')


def main():
    logging.info("程序开始执行 => main")
    
    # 启动时清除缓存（如果配置启用）
    if CONFIG['clear_cache_on_startup']:
        logging.info("启动时清除缓存...")
        clear_webview_cache()
    
    # 实例化Api类
    api = Api()
    logging.info("程序开始执行 => api")
    
    # 系统分辨率
    screens = webview.screens
    screens = screens[0]
    screenWidth = screens.width
    screenHeight = screens.height
    logging.info("程序开始执行 => screens")

    # 窗口大小
    initWidth = 750
    initHeight = 385

    # 计算窗口居中位置
    posX = int((screenWidth - initWidth) / 2)
    posY = int((screenHeight - initHeight) / 2)
    logging.info("程序开始执行 => window position")
    
    # 设置MIME类型
    mimetypes.add_type('application/javascript', '.js')
    logging.info("程序开始执行 => mimetypes")

    # 读取窗口配置
    window_config = load_window_config()
    always_on_top = window_config.get('alwaysOnTop', False)
    logging.info(f"窗口置顶状态: {always_on_top}")

    # 创建窗口
    #window = webview.create_window(title='BlingBling', url='http://localhost:8098', width=initWidth, height=initHeight, x=posX, y=posY, js_api=api, resizable=True, on_top=always_on_top, text_select=False, confirm_close=False, frameless=True, easy_drag=False)
    #window = webview.create_window(title='BlingBling', url='http://inkwell.top/gen_ui', width=initWidth, height=initHeight, js_api=api, resizable=True, on_top=always_on_top, text_select=False, confirm_close=False, frameless=True, easy_drag=False)
    window = webview.create_window(
        'BlingBling',
        'assets/ui/index.html', 
        width=initWidth, 
        height=initHeight, 
        x=posX,
        y=posY,
        js_api=api, 
        resizable=True, 
        on_top=always_on_top,
        text_select=False, 
        confirm_close=False, 
        frameless=True, 
        easy_drag=False
    )
    logging.info("程序开始执行 => window")
    
    api.set_window(window)
    logging.info("程序开始执行 => api.set_window(window)")

    # 窗口显示后调整大小（修复 DPI 缩放问题）
    def on_shown():
        window.resize(initWidth, initHeight)
        logging.info("窗口大小已调整")

    # 启动webview
    webview.start(
        on_shown,
        localization=chinese,
        http_server=True,
        private_mode=False,
        gui=None,
        debug=False
    )
    logging.info("程序开始执行 => webview.start")


if __name__ == '__main__':
    main()