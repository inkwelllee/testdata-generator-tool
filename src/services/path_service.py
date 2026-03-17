"""
路径服务
"""
import os
import sys
import logging
from typing import Optional


class PathService:
    """路径服务，处理各种路径相关操作"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._base_dir = self._detect_base_dir()

    @staticmethod
    def _detect_base_dir() -> str:
        """
        检测基础目录

        Returns:
            基础目录路径
        """
        if getattr(sys, 'frozen', None):
            # 打包环境
            return os.path.join(sys._MEIPASS, 'assets')
        else:
            # 开发环境
            return os.path.join(os.path.abspath("."), 'assets')

    @property
    def base_dir(self) -> str:
        """基础目录"""
        return self._base_dir

    @property
    def images_dir(self) -> str:
        """图片目录"""
        return os.path.join(self._base_dir, 'images')

    @property
    def fonts_dir(self) -> str:
        """字体目录"""
        return os.path.join(self._base_dir, 'fonts')

    @property
    def ui_dir(self) -> str:
        """UI目录"""
        return os.path.join(self._base_dir, 'ui')

    def get_image_path(self, filename: str) -> str:
        """
        获取图片完整路径

        Args:
            filename: 图片文件名

        Returns:
            完整路径
        """
        return os.path.join(self.images_dir, filename)

    def get_font_path(self, filename: str) -> str:
        """
        获取字体完整路径

        Args:
            filename: 字体文件名

        Returns:
            完整路径
        """
        return os.path.join(self.fonts_dir, filename)

    def get_data_path(self, filename: str) -> str:
        """
        获取数据文件完整路径

        Args:
            filename: 数据文件名

        Returns:
            完整路径
        """
        return os.path.join(self._base_dir, filename)

    def read_lines(self, filename: str) -> list:
        """
        读取文件并返回行列表

        Args:
            filename: 文件名

        Returns:
            行列表（已去除空白）
        """
        file_path = self.get_data_path(filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]

    def get_desktop_path(self) -> str:
        """获取桌面路径"""
        if sys.platform == 'win32':
            # 方法1: 使用注册表读取（最可靠）
            try:
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
                )
                desktop_path, _ = winreg.QueryValueEx(key, "Desktop")
                winreg.CloseKey(key)
                if desktop_path and os.path.exists(desktop_path):
                    logging.info(f"[get_desktop_path] 注册表获取成功: {desktop_path}")
                    return desktop_path
                logging.warning(f"[get_desktop_path] 注册表路径无效: {desktop_path}")
            except Exception as e:
                logging.warning(f"[get_desktop_path] 注册表方式失败: {e}")

            # 方法2: 使用 ctypes 调用 SHGetFolderPathW
            try:
                import ctypes
                from ctypes import wintypes

                buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
                # SHGetFolderPathW(hwnd, nFolder, hToken, dwFlags, pszPath)
                # CSIDL_DESKTOP = 0
                result = ctypes.windll.shell32.SHGetFolderPathW(0, 0, 0, 0, buf)
                if result == 0 and buf.value:
                    logging.info(f"[get_desktop_path] ctypes获取成功: {buf.value}")
                    return buf.value
                logging.warning(f"[get_desktop_path] ctypes方式失败, result={result}")
            except Exception as e:
                logging.warning(f"[get_desktop_path] ctypes方式异常: {e}")

            # 方法3: 尝试常见的桌面路径
            user_profile = os.environ.get('USERPROFILE', '')
            logging.info(f"[get_desktop_path] USERPROFILE环境变量: {user_profile}")

            if not user_profile:
                # 尝试其他方式获取用户目录
                user_profile = os.path.expandvars('%USERPROFILE%')
                logging.info(f"[get_desktop_path] expandvars USERPROFILE: {user_profile}")

            possible_paths = [
                os.path.join(user_profile, "Desktop"),      # 英文系统
                os.path.join(user_profile, "桌面"),          # 中文系统
            ]
            for path in possible_paths:
                logging.info(f"[get_desktop_path] 检查路径: {path}, 存在: {os.path.exists(path)}")
                if os.path.exists(path):
                    logging.info(f"[get_desktop_path] 找到桌面路径: {path}")
                    return path

        # 默认方式
        default_path = os.path.join(os.path.expanduser("~"), "Desktop")
        logging.info(f"[get_desktop_path] 使用默认路径: {default_path}")
        return default_path

    def get_current_dir(self) -> str:
        """获取当前工作目录"""
        return os.getcwd()

    def path_exists(self, path: str) -> bool:
        """检查路径是否存在"""
        return os.path.exists(path)

    def ensure_dir(self, path: str) -> str:
        """
        确保目录存在，如不存在则创建

        Args:
            path: 目录路径

        Returns:
            目录路径
        """
        os.makedirs(path, exist_ok=True)
        return path
