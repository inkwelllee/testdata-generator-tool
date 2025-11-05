import mimetypes
import os
import sys
import webview
import logging

# 导入自定义模块
from utils.logger import setup_logging, log_startup_info
from utils.api import Api
from utils.cache_manager import clear_webview_cache

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
    width = screens.width
    logging.info("程序开始执行 => width")
    
    # 窗口大小
    initWidth = 1200
    initHeight = 660
    logging.info("程序开始执行 => initHeight")
    
    # 设置MIME类型
    mimetypes.add_type('application/javascript', '.js')
    logging.info("程序开始执行 => mimetypes")
    
    # 创建窗口
    #window = webview.create_window(title='BlingBling', url='http://localhost:8098', width=initWidth, height=initHeight, js_api=api, resizable=True, text_select=False, confirm_close=False, frameless=True, easy_drag=False)
    #window = webview.create_window(title='BlingBling', url='http://inkwell.top/gen_ui', width=initWidth, height=initHeight, js_api=api, resizable=True, text_select=False, confirm_close=False, frameless=True, easy_drag=False)
    window = webview.create_window(
        'BlingBling', 
        'asserts/ui/index.html', 
        width=initWidth, 
        height=initHeight, 
        js_api=api, 
        resizable=True, 
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