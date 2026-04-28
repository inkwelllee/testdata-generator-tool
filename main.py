import mimetypes
import os
import sys
import webview
import logging

# 导入自定义模块
from src.utils.logger import setup_logging, log_startup_info
from src.utils.api import Api, get_config
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
    screen = screens[0]
    screen_width = screen.width
    screen_height = screen.height
    logging.info(f"屏幕分辨率: {screen_width}x{screen_height}")

    # 读取保存的窗口大小，默认 900x500
    init_width = get_config('windowWidth', 900)
    init_height = get_config('windowHeight', 500)
    logging.info(f"窗口大小: {init_width}x{init_height}")

    # 计算居中位置
    center_x = (screen_width - init_width) // 2
    center_y = (screen_height - init_height) // 2
    logging.info(f"窗口位置: ({center_x}, {center_y})")

    # 设置MIME类型
    mimetypes.add_type('application/javascript', '.js')
    logging.info("程序开始执行 => mimetypes")

    # 读取置顶配置
    always_on_top = get_config('alwaysOnTop', False)
    logging.info(f"窗口置顶状态: {always_on_top}")

    # 创建窗口（居中显示）
    window = webview.create_window(
        title='不娇虑',
        url='http://localhost:8098',
        width=init_width,
        height=init_height,
        x=center_x,
        y=center_y,
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

    # 启动webview
    webview.start(
        localization=chinese,
        http_server=True,
        private_mode=False,
        gui=None,
        debug=False
    )
    logging.info("程序开始执行 => webview.start")


if __name__ == '__main__':
    main()