import os
import sys
from .constants import *

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.base_dir = self._get_base_dir()
            self.assets_dir = self._get_assets_dir()
            self.initialized = True
    
    def _get_base_dir(self):
        """获取基础目录路径"""
        if getattr(sys, 'frozen', None):
            return os.path.join(sys._MEIPASS, 'assets')
        return os.path.join(os.path.abspath("."), 'assets')
    
    def _get_assets_dir(self):
        """获取资源文件目录"""
        return os.path.join(self.base_dir, 'assets')
    
    def get_font_path(self, font_name):
        """获取字体文件路径"""
        return os.path.join(self.assets_dir, IMAGE_CONFIG['FONTS'].get(font_name))
    
    def get_image_path(self, image_name):
        """获取图片文件路径"""
        return os.path.join(self.assets_dir, image_name)
    
    def get_area_codes(self):
        """获取地区编码"""
        area_code_path = os.path.join(self.assets_dir, 'areaCode.txt')
        with open(area_code_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    
    @property
    def bank_prefixes(self):
        return BANK_PREFIXES
    
    @property
    def name_data(self):
        return NAME_DATA
    
    @property
    def company_name_data(self):
        return COMPANY_NAME_DATA
    
    @property
    def phone_prefixes(self):
        return PHONE_PREFIXES
    
    @property
    def image_config(self):
        return IMAGE_CONFIG
    
    @property
    def area_info(self):
        return AREA_INFO