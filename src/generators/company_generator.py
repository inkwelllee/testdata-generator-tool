"""
公司信息生成器
"""
import random
from typing import Dict, List
from .data_generator import DataGenerator


class CompanyGenerator(DataGenerator):
    """公司信息生成器"""

    def __init__(
        self,
        company_name_data: Dict[str, List[str]],
        area_codes: List[str]
    ):
        """
        初始化公司生成器

        Args:
            company_name_data: 公司名称数据（正面词、描述词、行业词）
            area_codes: 地区编码列表
        """
        self.company_name_data = company_name_data
        self.area_codes = area_codes

    def generate_company_name(self) -> str:
        """
        生成公司名称

        Returns:
            公司名称
        """
        first_word = self.random_choice(self.company_name_data['POSITIVE_WORDS'])
        second_part = self.random_choice(self.company_name_data['DESCRIPTIVE_WORDS'])
        industry_word = self.random_choice(self.company_name_data['INDUSTRY_WORDS'])
        return f"{first_word}{second_part}{industry_word}公司"

    @staticmethod
    def calculate_check_digit(code: str) -> str:
        """
        计算统一社会信用代码校验码

        Args:
            code: 前17位代码

        Returns:
            校验码（第18位）
        """
        ws = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
        str_chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"

        if len(code) != 17:
            raise ValueError("Input code must be 17 characters long")

        for char in code:
            if char not in str_chars:
                raise ValueError(f"Character '{char}' not found in mapping table")

        sum_val = sum(str_chars.index(char) * ws[i] for i, char in enumerate(code))
        check_digit_num = 31 - (sum_val % 31)

        if check_digit_num > 30:
            return '0'
        return str_chars[check_digit_num]

    @staticmethod
    def calculate_org_code_check_digit(org_code: str) -> str:
        """
        计算组织机构代码校验码

        Args:
            org_code: 前8位组织机构代码

        Returns:
            校验码（第9位）
        """
        ws = [3, 7, 9, 10, 5, 8, 4, 2]
        str_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        sum_val = sum(str_chars.index(char) * ws[i] for i, char in enumerate(org_code[:8]))
        check_digit_num = 11 - (sum_val % 11)

        if check_digit_num == 11:
            return '0'
        elif check_digit_num == 10:
            return 'X'
        return str(check_digit_num)

    def generate_org_code(self) -> str:
        """
        生成组织机构代码

        Returns:
            9位组织机构代码（带连字符）
        """
        chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
        org_code = self.random_choices(chars, 8)
        check_digit = self.calculate_org_code_check_digit(org_code)
        return org_code + '-' + check_digit

    def generate_credit_code(self) -> str:
        """
        生成统一社会信用代码

        Returns:
            18位统一社会信用代码
        """
        # 登记管理部门代码
        management_code = self.random_choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'N', 'Y'])

        # 机构类别代码
        department_code = {
            '1': '1',
            '2': self.random_choice(['1', '9']),
            '3': self.random_choice(['1', '2', '3', '4', '5', '9']),
            '4': self.random_choice(['1', '9']),
            '5': self.random_choice(['1', '2', '3', '9']),
            '6': self.random_choice(['1', '2', '9']),
            '7': self.random_choice(['1', '2', '9']),
            '8': self.random_choice(['1', '9']),
            '9': self.random_choice(['1', '2', '3']),
            'A': self.random_choice(['1', '9']),
            'N': self.random_choice(['1', '2', '3', '9']),
            'Y': '1'
        }
        institution_code = department_code[management_code]

        # 行政区划码
        administrative_code = self.random_choice(self.area_codes)

        # 组织机构代码
        org_code = self.generate_org_code()

        # 拼接并计算校验码
        usc_code = management_code + institution_code + administrative_code + org_code.replace("-", "")
        check_digit = self.calculate_check_digit(usc_code)

        return usc_code + check_digit

    def generate_pbc_code(self) -> str:
        """
        生成中征码

        Returns:
            16位中征码
        """
        weight_factor = [1, 3, 5, 7, 11, 2, 13, 1, 1, 17, 19, 97, 23, 29]
        chars = '0123456789'

        # 生成前14位
        id_code = self.random_choices(chars, 14)

        # 计算校验位
        num = 0
        for i in range(14):
            if 'A' <= id_code[i] <= 'Z':
                temp = ord(id_code[i]) - 55
            else:
                temp = ord(id_code[i]) - 48
            num += temp * weight_factor[i]

        residue = num % 97 + 1
        check_code = f"{residue:02d}"

        return id_code + check_code
