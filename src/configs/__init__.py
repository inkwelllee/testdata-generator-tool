"""
配置模块
"""
from .config_manager import ConfigManager
from .constants import (
    BANK_PREFIXES,
    NAME_DATA,
    COMPANY_NAME_DATA,
    PHONE_PREFIXES,
    IMAGE_CONFIG,
    AREA_INFO,
)

__all__ = [
    'ConfigManager',
    'BANK_PREFIXES',
    'NAME_DATA',
    'COMPANY_NAME_DATA',
    'PHONE_PREFIXES',
    'IMAGE_CONFIG',
    'AREA_INFO',
]
