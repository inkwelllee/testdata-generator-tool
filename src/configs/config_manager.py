"""
配置管理器
"""
import os
import sys
from typing import Dict, List
from .constants import (
    BANK_PREFIXES,
    NAME_DATA,
    COMPANY_NAME_DATA,
    PHONE_PREFIXES,
    IMAGE_CONFIG,
    AREA_INFO,
)


class ConfigManager:
    """配置管理器（单例模式）"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._base_dir = self._detect_base_dir()
        self._area_codes: List[str] = []
        self._initialized = True

    @staticmethod
    def _detect_base_dir() -> str:
        """检测基础目录路径"""
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
    def area_codes(self) -> List[str]:
        """地区编码列表（懒加载）"""
        if not self._area_codes:
            self._area_codes = self._load_area_codes()
        return self._area_codes

    def _load_area_codes(self) -> List[str]:
        """加载地区编码"""
        area_code_path = os.path.join(self._base_dir, 'areaCode.txt')
        try:
            with open(area_code_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            # 尝试备用路径
            alt_path = os.path.join(self._base_dir, '../assets/areaCode.txt')
            with open(alt_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines() if line.strip()]

    def get_font_path(self, font_name: str) -> str:
        """
        获取字体文件路径

        Args:
            font_name: 字体配置名称

        Returns:
            字体文件完整路径
        """
        font_config = IMAGE_CONFIG.get('FONTS', {})
        font_file = font_config.get(font_name, font_config.get('DEFAULT', 'hei.ttf'))
        return os.path.join(self._base_dir, 'fonts', font_file)

    def get_image_path(self, image_name: str) -> str:
        """
        获取图片文件路径

        Args:
            image_name: 图片文件名

        Returns:
            图片文件完整路径
        """
        return os.path.join(self._base_dir, 'images', image_name)

    # 配置属性
    @property
    def bank_prefixes(self) -> Dict[str, List[str]]:
        return BANK_PREFIXES

    @property
    def name_data(self) -> Dict[str, List[str]]:
        return NAME_DATA

    @property
    def company_name_data(self) -> Dict[str, List[str]]:
        return COMPANY_NAME_DATA

    @property
    def phone_prefixes(self) -> List[str]:
        return PHONE_PREFIXES

    @property
    def image_config(self) -> Dict:
        return IMAGE_CONFIG

    @property
    def area_info(self) -> Dict[int, str]:
        return AREA_INFO
