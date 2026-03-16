"""
身份证生成器
"""
import random
from typing import List
from .data_generator import DataGenerator


class IDGenerator(DataGenerator):
    """身份证号码生成器"""

    def __init__(self, area_codes: List[str]):
        """
        初始化身份证生成器

        Args:
            area_codes: 地区编码列表
        """
        self.area_codes = area_codes

    @staticmethod
    def calculate_checksum(id_number: str) -> str:
        """
        计算身份证校验码

        Args:
            id_number: 前17位身份证号码

        Returns:
            校验码（第18位）
        """
        factor_arr = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
        parity_bit = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

        weight_sum = sum(int(id_number[i]) * factor_arr[i] for i in range(17))
        return parity_bit[weight_sum % 11]

    @staticmethod
    def generate_sequence_code(gender: int) -> str:
        """
        根据性别生成三位顺序码

        Args:
            gender: 性别 (1=男, 0=女)

        Returns:
            三位顺序码
        """
        while True:
            sequence_code = random.randint(100, 999)
            # 男奇数，女偶数
            if gender == 1 and sequence_code % 2 != 0:
                return str(sequence_code)
            elif gender == 0 and sequence_code % 2 == 0:
                return str(sequence_code)

    def generate(self, gender: int, birth_date: str) -> str:
        """
        生成身份证号码

        Args:
            gender: 性别 (1=男, 0=女)
            birth_date: 出生日期 (YYYY-MM-DD 格式)

        Returns:
            18位身份证号码
        """
        # 随机选择地区码
        region_code = self.random_choice(self.area_codes)

        # 处理出生日期
        birth_date_clean = birth_date.replace("-", "")

        # 生成顺序码
        sequence_code = self.generate_sequence_code(gender)

        # 拼接前17位
        id_number_17 = region_code + birth_date_clean + sequence_code

        # 计算校验码
        checksum = self.calculate_checksum(id_number_17)

        return id_number_17 + checksum
