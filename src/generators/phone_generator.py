"""
手机号和邮箱生成器
"""
from datetime import datetime
from .data_generator import DataGenerator


class PhoneGenerator(DataGenerator):
    """手机号和邮箱生成器"""

    def __init__(self, phone_prefixes: list):
        """
        初始化手机号生成器

        Args:
            phone_prefixes: 手机号前缀列表
        """
        self.phone_prefixes = phone_prefixes

    def generate_phone(self) -> str:
        """
        生成手机号

        Returns:
            11位手机号
        """
        prefix = self.random_choice(self.phone_prefixes)
        remaining_digits = self.random_choices("0123456789", 9)
        return prefix + remaining_digits

    def generate_email(self) -> str:
        """
        生成邮箱地址

        Returns:
            邮箱地址
        """
        timestamp = int(datetime.now().timestamp())
        return f"{timestamp}@qq.com"
