"""
API类模块 - 提供给前端调用的接口
"""
import hashlib
import json
import logging
import os
import sys
import time
from typing import Dict, Optional

from src.generators import (
    IDGenerator,
    PhoneGenerator,
    CompanyGenerator,
    BankGenerator,
    VehicleGenerator,
    PersonalGenerator,
)
from src.services import ImageService, PathService
from src.configs import ConfigManager
from .cache_manager import clear_webview_cache, get_cache_info, format_size


# 配置文件路径
def get_config_path() -> str:
    """获取配置文件路径"""
    if sys.platform == "win32":
        base_dir = os.path.join(os.environ.get('APPDATA', ''), 'pywebview')
    else:
        base_dir = os.path.join(os.path.expanduser('~'), '.pywebview')
    return os.path.join(base_dir, 'app_config.json')


def _load_config() -> Dict:
    """加载配置文件"""
    config_path = get_config_path()
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"加载配置文件失败: {e}")
    return {}


def _save_config(config: Dict) -> None:
    """保存配置文件"""
    config_path = get_config_path()
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"保存配置文件失败: {e}")


def get_config(key: str, default=None):
    """获取单个配置项"""
    config = _load_config()
    return config.get(key, default)


def set_config(key: str, value) -> None:
    """设置单个配置项"""
    config = _load_config()
    config[key] = value
    _save_config(config)


def get_all_config() -> Dict:
    """获取全部配置"""
    return _load_config()


# 兼容旧接口
def get_window_config_path() -> str:
    """获取配置文件路径（兼容旧接口）"""
    return get_config_path()


def load_window_config() -> Dict:
    """加载窗口配置（兼容旧接口）"""
    config = _load_config()
    # 返回默认值确保向后兼容
    if 'alwaysOnTop' not in config:
        config['alwaysOnTop'] = False
    return config


def save_window_config(config: Dict) -> None:
    """保存窗口配置（兼容旧接口）"""
    _save_config(config)


# ========== 验证相关 ==========

DEFAULT_PASSWORD = "inkwell"


def _hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def _ensure_password_hash() -> str:
    """确保密码哈希存在，首次启动时设置默认密码"""
    password_hash = get_config('passwordHash')
    if not password_hash:
        password_hash = _hash_password(DEFAULT_PASSWORD)
        set_config('passwordHash', password_hash)
        logging.info("首次启动，设置默认密码哈希")
    return password_hash


def getVerificationStatus() -> Dict:
    """获取验证状态"""
    _ensure_password_hash()

    is_verified = get_config('isVerified', False)
    failed_attempts = get_config('failedAttempts', 0)
    lock_until = get_config('lockUntil', 0)

    current_time = time.time()
    is_locked = lock_until > current_time
    lock_remaining_seconds = 0
    if is_locked:
        lock_remaining_seconds = int(lock_until - current_time)

    return {
        'isVerified': is_verified,
        'isLocked': is_locked,
        'lockRemainingSeconds': lock_remaining_seconds,
        'failedAttempts': failed_attempts
    }


def verifyPassword(password: str) -> Dict:
    """验证密码"""
    _ensure_password_hash()

    # 检查锁定状态
    lock_until = get_config('lockUntil', 0)
    current_time = time.time()

    if lock_until > current_time:
        remaining = int(lock_until - current_time)
        return {
            'success': False,
            'message': f'已锁定，请等待 {remaining} 秒',
            'isLocked': True,
            'lockRemainingSeconds': remaining
        }

    # 验证密码
    password_hash = get_config('passwordHash')
    input_hash = _hash_password(password)

    if input_hash == password_hash:
        # 成功：重置状态
        set_config('isVerified', True)
        set_config('failedAttempts', 0)
        set_config('lockUntil', 0)
        logging.info("密码验证成功")
        return {
            'success': True,
            'message': '验证成功',
            'isLocked': False,
            'lockRemainingSeconds': 0
        }
    else:
        # 失败：增加计数
        failed_attempts = get_config('failedAttempts', 0) + 1
        set_config('failedAttempts', failed_attempts)

        # 超过5次后锁定
        if failed_attempts > 5:
            lock_minutes = 1 + failed_attempts
            lock_until = current_time + lock_minutes * 60
            set_config('lockUntil', lock_until)
            logging.warning(f"密码验证失败 {failed_attempts} 次，锁定 {lock_minutes} 分钟")
            return {
                'success': False,
                'message': f'密码错误，已锁定 {lock_minutes} 分钟',
                'isLocked': True,
                'lockRemainingSeconds': lock_minutes * 60
            }

        logging.warning(f"密码验证失败，累计 {failed_attempts} 次")
        return {
            'success': False,
            'message': f'密码错误，已失败 {failed_attempts} 次',
            'isLocked': False,
            'lockRemainingSeconds': 0
        }


def resetVerification() -> None:
    """重置验证状态"""
    set_config('isVerified', False)
    set_config('failedAttempts', 0)
    set_config('lockUntil', 0)
    logging.info("验证状态已重置")


class Api:
    """
    API类 - 提供给前端Web调用的接口
    使用组合模式整合各生成器
    """

    def __init__(self) -> None:
        # 配置管理器
        self._config = ConfigManager()

        # 路径服务
        self._path_service = PathService()

        # 图片服务
        self._image_service = ImageService(self._config)

        # 初始化各生成器
        self._id_generator = IDGenerator(self._config.area_codes)
        self._phone_generator = PhoneGenerator(self._config.phone_prefixes)
        self._company_generator = CompanyGenerator(
            self._config.company_name_data,
            self._config.area_codes
        )
        self._bank_generator = BankGenerator(self._config.bank_prefixes)
        self._vehicle_generator = VehicleGenerator()
        self._personal_generator = PersonalGenerator(
            self._config.name_data,
            self._config.area_info
        )

        # 窗口引用
        self._window = None

    def set_window(self, window) -> None:
        """设置窗口引用"""
        self._window = window

    # ========== 数据生成方法 ==========

    def randomName(self, sex: int) -> str:
        """生成姓名"""
        return self._personal_generator.generate_name(sex)

    def randomIdCard(self, sex: int, birth_date: str) -> str:
        """生成身份证号"""
        return self._id_generator.generate(sex, birth_date)

    def randomPhoneNumber(self) -> str:
        """生成手机号"""
        return self._phone_generator.generate_phone()

    def randomEmail(self) -> str:
        """生成邮箱"""
        return self._phone_generator.generate_email()

    def randomCompanyName(self) -> str:
        """生成公司名称"""
        return self._company_generator.generate_company_name()

    def randomSocialCreditCode(self) -> str:
        """生成统一社会信用代码"""
        return self._company_generator.generate_credit_code()

    def randomOrganizationCode(self) -> str:
        """生成组织机构代码"""
        return self._company_generator.generate_org_code()

    def randomZhongzhengCode(self) -> str:
        """生成中征码"""
        return self._company_generator.generate_pbc_code()

    def randomBankAccount(self, bankType: str) -> str:
        """生成银行卡号"""
        return self._bank_generator.generate(bankType)

    def randomLicensePlate(self) -> str:
        """生成车牌号"""
        return self._vehicle_generator.generate_license_plate()

    def randomVIN(self) -> str:
        """生成车架号"""
        return self._vehicle_generator.generate_vin()

    def randomEngineNo(self) -> str:
        """生成发动机号"""
        return self._vehicle_generator.generate_engine_no()

    def randomAddress(self) -> str:
        """生成地址"""
        return self._personal_generator.generate_address()

    # ========== 图片生成方法 ==========

    def generateIdCardImage(
        self,
        name: str,
        sex: int,
        birth_date: str,
        idCard: str,
        directoryPath: str
    ) -> str:
        """生成身份证图片"""
        return self._image_service.generate_id_card_image(
            name, sex, birth_date, idCard, directoryPath
        )

    def generateBusinessImage(
        self,
        companyName: str,
        creditCode: str,
        name: str,
        directoryPath: str
    ) -> str:
        """生成营业执照图片"""
        return self._image_service.generate_business_license_image(
            companyName, creditCode, name, directoryPath
        )

    # ========== 路径方法 ==========

    def changeDirectory(self, directoryType: str) -> str:
        """
        获取目录路径

        Args:
            directoryType: 目录类型 ('desktop', 'follow', 其他)

        Returns:
            目录路径
        """
        if directoryType == 'desktop':
            return self._path_service.get_desktop_path()
        elif directoryType == 'follow':
            return self._path_service.get_current_dir()
        return ''

    def checkPath(self, directoryPath: str) -> bool:
        """检查路径是否存在"""
        return self._path_service.path_exists(directoryPath)

    # ========== 窗口控制方法 ==========

    def quit(self) -> None:
        """退出程序"""
        self._window.destroy()

    def destroyApp(self) -> None:
        """关闭窗口"""
        self._window.destroy()

    def minimizeApp(self) -> None:
        """最小化窗口"""
        self._window.minimize()

    def maximizeApp(self) -> None:
        """最大化窗口"""
        self._window.maximize()

    def restoreApp(self) -> None:
        """还原窗口"""
        self._window.restore()

    def resizeApp(self, width: int, height: int) -> None:
        """调整窗口大小"""
        self._window.resize(width, height)

    def toggleAlwaysOnTop(self) -> bool:
        """切换窗口置顶状态"""
        try:
            logging.info(f"当前 on_top 状态: {self._window.on_top}")
            self._window.on_top = not self._window.on_top
            new_state = self._window.on_top
            logging.info(f"切换后 on_top 状态: {new_state}")
            # 保存配置
            config = load_window_config()
            config['alwaysOnTop'] = new_state
            save_window_config(config)
            return new_state
        except Exception as e:
            logging.error(f"设置置顶状态失败: {e}", exc_info=True)
            return False

    def getAlwaysOnTop(self) -> bool:
        """获取保存的置顶状态"""
        config = load_window_config()
        return config.get('alwaysOnTop', False)

    def getWindowSize(self) -> Dict:
        """获取保存的窗口大小"""
        return {
            'width': get_config('windowWidth', 900),
            'height': get_config('windowHeight', 500)
        }

    def saveWindowSize(self, width: int, height: int) -> None:
        """保存窗口大小"""
        set_config('windowWidth', width)
        set_config('windowHeight', height)

    def test(self) -> None:
        """测试方法"""
        self._window.resize(1420, 720)

    # ========== 验证方法 ==========

    def getVerificationStatus(self) -> Dict:
        """获取验证状态"""
        return getVerificationStatus()

    def verifyPassword(self, password: str) -> Dict:
        """验证密码"""
        return verifyPassword(password)

    def resetVerification(self) -> None:
        """重置验证状态"""
        resetVerification()

    # ========== 缓存管理方法 ==========

    def clearCache(self) -> str:
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

    def clearSystemCache(self) -> str:
        """清除系统缓存目录"""
        try:
            success = clear_webview_cache()
            if success:
                return "系统缓存清除成功"
            return "未找到需要清除的缓存目录"
        except Exception as e:
            return f"清除系统缓存失败: {str(e)}"

    def getCacheInfo(self) -> Dict:
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
            return {'error': f"获取缓存信息失败: {str(e)}"}
