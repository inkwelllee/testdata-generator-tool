"""
API类模块 - 提供给前端调用的接口
"""
import logging
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

    def test(self) -> None:
        """测试方法"""
        self._window.resize(1420, 720)

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
