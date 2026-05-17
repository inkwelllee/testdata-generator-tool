import mimetypes
import os
import sys
import webview
import logging
import ctypes
import ctypes.wintypes

# 必须在创建任何窗口前调用，让进程感知 DPI
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

from src.utils.logger import setup_logging, log_startup_info
from src.utils.api import Api, get_config, set_config
from src.utils.cache_manager import clear_webview_cache

CONFIG = {
    'enable_file_logging_in_production': True,  # 打包后是否启用文件日志
    'use_pywebview_directory': True,            # 是否使用pywebview目录
    'clear_cache_on_startup': True,             # 启动时是否清除缓存 (开发时可设为True)
}

log_file_path, logs_directory = setup_logging(
    CONFIG['enable_file_logging_in_production'],
    CONFIG['use_pywebview_directory']
)

log_startup_info(
    log_file_path,
    logs_directory,
    CONFIG['enable_file_logging_in_production'],
    CONFIG['use_pywebview_directory']
)

chinese = {
    'global.quitConfirmation': '暂别勿思念，转瞬与亲见',
}

if getattr(sys, 'frozen', None):
    web_dir = os.path.join(sys._MEIPASS, 'gui')
else:
    web_dir = os.path.join(os.path.abspath("."), 'gui')


# 默认窗口尺寸（基准值，需要乘以 DPI 缩放）
BASE_WIDTH = 900
BASE_HEIGHT = 500


def get_dpi_scale():
    """获取 DPI 缩放因子"""
    try:
        hwnd = ctypes.windll.user32.GetDesktopWindow()
        dc = ctypes.windll.user32.GetDC(hwnd)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(dc, 88)  # LOGPIXELSX
        ctypes.windll.user32.ReleaseDC(hwnd, dc)
        return dpi / 96.0
    except Exception:
        return 1.0


def main():
    logging.info("程序开始执行 => main")

    if CONFIG['clear_cache_on_startup']:
        logging.info("启动时清除缓存...")
        clear_webview_cache()

    api = Api()
    logging.info("程序开始执行 => api")

    # 计算 DPI 缩放后的物理像素尺寸
    dpi_scale = get_dpi_scale()
    default_width = int(BASE_WIDTH * dpi_scale)
    default_height = int(BASE_HEIGHT * dpi_scale)
    set_config('defaultWindowWidth', default_width)
    set_config('defaultWindowHeight', default_height)
    logging.info(f"DPI 缩放: {dpi_scale}, 默认窗口: {default_width}x{default_height}")

    # 系统分辨率（物理像素）
    screens = webview.screens
    screen = screens[0]
    screen_width = screen.width
    screen_height = screen.height
    logging.info(f"屏幕分辨率: {screen_width}x{screen_height}")

    # 优先读取用户自定义大小（物理像素），否则使用默认大小
    custom_width = get_config('customWindowWidth')
    custom_height = get_config('customWindowHeight')
    if custom_width and custom_height:
        init_width = custom_width
        init_height = custom_height
        logging.info(f"使用自定义窗口大小: {init_width}x{init_height}")
    else:
        init_width = default_width
        init_height = default_height
        logging.info(f"使用默认窗口大小: {init_width}x{init_height}")

    # 优先读取保存的位置，否则居中（全部使用物理像素）
    saved_x = get_config('windowX')
    saved_y = get_config('windowY')
    if saved_x is not None and saved_y is not None:
        init_x = saved_x
        init_y = saved_y
        logging.info(f"使用保存的窗口位置: ({init_x}, {init_y})")
    else:
        init_x = (screen_width - init_width) // 2
        init_y = (screen_height - init_height) // 2
        logging.info(f"窗口居中位置: ({init_x}, {init_y})")

    mimetypes.add_type('application/javascript', '.js')
    logging.info("程序开始执行 => mimetypes")

    always_on_top = get_config('alwaysOnTop', False)
    logging.info(f"窗口置顶状态: {always_on_top}")

    # 创建窗口（居中显示）
    #window = webview.create_window(title='bujiaolv', url='http://localhost:8098', width=init_width, height=init_height, x=center_x, y=center_y, js_api=api, resizable=True, on_top=always_on_top, text_select=False, confirm_close=False, frameless=True, easy_drag=False)
    #window = webview.create_window(title='bujiaolv', url='http://inkwell.top/gen_ui', width=init_width, height=init_height, js_api=api, resizable=True, on_top=always_on_top, text_select=False, confirm_close=False, frameless=True, easy_drag=False)
    window = webview.create_window(
        title='bujiaolv', url='http://localhost:8098',
        width=init_width, height=init_height,
        x=init_x, y=init_y,
        js_api=api, resizable=True, on_top=always_on_top,
        text_select=False, confirm_close=False,
        frameless=True, easy_drag=False
    )
    logging.info("程序开始执行 => window")

    api.set_window(window)
    logging.info("程序开始执行 => api.set_window(window)")

    def on_closing():
        """窗口关闭时保存位置和大小（物理像素）"""
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if hwnd:
                if ctypes.windll.user32.IsZoomed(hwnd):
                    logging.info("窗口已最大化，不保存状态")
                    return

                rect = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                width = rect.right - rect.left
                height = rect.bottom - rect.top
                x = rect.left
                y = rect.top

                dw = get_config('defaultWindowWidth', default_width)
                dh = get_config('defaultWindowHeight', default_height)
                if width != dw or height != dh:
                    set_config('customWindowWidth', width)
                    set_config('customWindowHeight', height)
                    logging.info(f"保存自定义窗口大小: {width}x{height}")
                else:
                    set_config('customWindowWidth', None)
                    set_config('customWindowHeight', None)
                    logging.info("窗口大小与默认相同，清除自定义")

                set_config('windowX', x)
                set_config('windowY', y)
                logging.info(f"保存窗口位置: ({x}, {y})")
        except Exception as e:
            logging.error(f"保存窗口状态失败: {e}")

    window.events.closing += on_closing

    def on_shown():
        """窗口显示后精确设置大小（解决 frameless 窗口尺寸偏差）"""
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if hwnd:
                ctypes.windll.user32.SetWindowPos(
                    hwnd, None, init_x, init_y, init_width, init_height,
                    0x0040  # SWP_SHOWWINDOW
                )
                logging.info(f"窗口显示后调整为: {init_width}x{init_height} at ({init_x}, {init_y})")
        except Exception as e:
            logging.error(f"调整窗口大小失败: {e}")

    window.events.shown += on_shown

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
