"""
API类模块
"""
import os
import sys
import shutil
import tempfile
import logging
from backend.gen import numberGen
from .cache_manager import clear_webview_cache, get_cache_info, format_size


class Api:
    def __init__(self) -> None:
        numberGen.__init__(self)
        self._window = None

    def set_window(self, window):
        self._window = window

    def quit(self):
        self._window.destroy()

    # 数据生成相关方法
    def randomName(self, sex):
        return numberGen.random_name(self, sex)
    
    def randomIdCard(self, sex, birth_date):
        return numberGen.random_id_card(self, sex, birth_date)
    
    def randomPhoneNumber(self):
        return numberGen.random_phone_number(self)
    
    def randomEmail(self):
        return numberGen.random_email(self)
    
    def randomCompanyName(self):
        return numberGen.random_company_name(self)
    
    def randomSocialCreditCode(self):
        return numberGen.random_credit_code(self)
    
    def randomOrganizationCode(self):
        return numberGen.random_organ_code(self)
    
    def randomZhongzhengCode(self):
        return numberGen.random_pbc_code(self)
    
    def randomBankAccount(self, bankType):
        return numberGen.random_bank_account(self, bankType)
    
    def generateIdCardImage(self, name, sex, birth_date, idCard, directoryPath):
        return numberGen.handle_image(self, name, sex, birth_date, idCard, directoryPath)
    
    def generateBusinessImage(self, companyName, creditCode, name, directoryPath):
        return numberGen.handle_business_image(self, companyName, creditCode, name, directoryPath)
    
    def changeDirectory(self, directoryType):
        return numberGen.change_directory(self, directoryType)
    
    def checkPath(self, directoryPath):
        return numberGen.check_path(self, directoryPath)

    # 窗口控制相关方法
    def destroyApp(self):
        """关闭窗口"""
        self._window.destroy()

    def minimizeApp(self):
        """最小化窗口"""
        self._window.minimize()

    def maximizeApp(self):
        """最大化窗口"""
        self._window.maximize()

    def restoreApp(self):
        """还原窗口"""
        self._window.restore()

    def resizeApp(self, width, height):
        """调整窗口大小"""
        self._window.resize(width, height)

    def test(self):
        self._window.resize(1420, 720)
    
    # 缓存管理相关方法
    def clearCache(self):
        """清除浏览器缓存"""
        try:
            self._window.evaluate_js("""
                localStorage.clear();
                sessionStorage.clear();
                location.reload(true);
            """)
            return "缓存已清除"
        except Exception as e:
            return f"清除缓存失败: {str(e)}"
    
    def clearSystemCache(self):
        """清除系统缓存目录"""
        try:
            success = clear_webview_cache()
            if success:
                return "系统缓存清除成功"
            else:
                return "未找到需要清除的缓存目录"
        except Exception as e:
            return f"清除系统缓存失败: {str(e)}"
    
    def getCacheInfo(self):
        """获取缓存信息"""
        try:
            cache_info = get_cache_info()
            
            result = {
                'total_size': format_size(cache_info['total_size']),
                'total_files': cache_info['total_files'],
                'directories': []
            }
            
            for dir_info in cache_info['directories']:
                result['directories'].append({
                    'path': dir_info['path'],
                    'size': format_size(dir_info['size']),
                    'files': dir_info['files'],
                    'exists': dir_info['exists']
                })
            
            return result
            
        except Exception as e:
            return f"获取缓存信息失败: {str(e)}"