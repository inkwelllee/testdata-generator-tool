"""
数据生成器基类
"""
import random
from datetime import datetime, timedelta
from typing import List, Optional


class DataGenerator:
    """数据生成器基类，提供通用工具方法"""

    @staticmethod
    def random_choice(items: List[str]) -> str:
        """从列表中随机选择一个元素"""
        return random.choice(items)

    @staticmethod
    def random_choices(chars: str, k: int) -> str:
        """从字符集中随机选择k个字符"""
        return ''.join(random.choices(chars, k=k))

    @staticmethod
    def random_int(min_val: int, max_val: int) -> int:
        """生成指定范围的随机整数"""
        return random.randint(min_val, max_val)

    @staticmethod
    def generate_random_date(start_year: int = 1960, end_year: int = 2020) -> str:
        """生成随机日期（YYYYMMDD格式）"""
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%Y%m%d")

    @staticmethod
    def validate_date(date_string: str) -> bool:
        """验证日期字符串格式是否正确"""
        try:
            datetime.strptime(date_string, "%Y%m%d")
            return True
        except ValueError:
            return False
