"""
车辆信息生成器
"""
from .data_generator import DataGenerator


class VehicleGenerator(DataGenerator):
    """车辆信息生成器"""

    # 省份简称
    PROVINCES = [
        "京", "津", "沪", "渝", "冀", "豫", "云", "辽", "黑", "湘",
        "皖", "鲁", "新", "苏", "浙", "赣", "鄂", "桂", "甘", "晋",
        "蒙", "陕", "吉", "闽", "贵", "粤", "青", "藏", "川", "宁", "琼"
    ]

    # VIN码可用字符（不含I, O, Q）
    VIN_CHARS = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"

    # 发动机号可用字符
    ENGINE_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def generate_license_plate(self) -> str:
        """
        生成车牌号

        Returns:
            车牌号（如：京A12345）
        """
        province = self.random_choice(self.PROVINCES)
        alpha = self.random_choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        suffix = self.random_choices(alphanumeric, 5)
        return province + alpha + suffix

    def generate_vin(self) -> str:
        """
        生成车架号 (VIN)

        Returns:
            17位车架号
        """
        return self.random_choices(self.VIN_CHARS, 17)

    def generate_engine_no(self) -> str:
        """
        生成发动机号

        Returns:
            6-10位发动机号
        """
        length = self.random_int(6, 10)
        return self.random_choices(self.ENGINE_CHARS, length)

    def generate_all(self) -> dict:
        """
        生成所有车辆信息

        Returns:
            {车牌号, 车架号, 发动机号}
        """
        return {
            'license_plate': self.generate_license_plate(),
            'vin': self.generate_vin(),
            'engine_no': self.generate_engine_no(),
        }
