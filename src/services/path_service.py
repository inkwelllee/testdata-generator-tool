"""
路径服务
"""
import os
import sys
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
        return os.path.join(os.path.expanduser("~"), "Desktop")

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
