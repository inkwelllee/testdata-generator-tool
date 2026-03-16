"""
银行卡生成器
"""
import random
from typing import Dict, List
from .data_generator import DataGenerator


class BankGenerator(DataGenerator):
    """银行卡号生成器"""

    # 银行类型常量
    BOC = "BOC"      # 中国银行
    CCB = "CCB"      # 建设银行
    ABC = "ABC"      # 农业银行
    ICBC = "ICBC"    # 工商银行
    PSBC = "PSBC"    # 邮储银行

    def __init__(self, bank_prefixes: Dict[str, List[str]]):
        """
        初始化银行卡生成器

        Args:
            bank_prefixes: 银行卡前缀配置 {银行类型: [前缀列表]}
        """
        self.bank_prefixes = bank_prefixes

    def generate(self, bank_type: str) -> str:
        """
        生成银行卡号

        Args:
            bank_type: 银行类型 (BOC, CCB, ABC, ICBC, PSBC)

        Returns:
            19位银行卡号
        """
        prefixes = self.bank_prefixes.get(bank_type, ['666666'])
        prefix = random.choice(prefixes)
        suffix = self.random_choices("0123456789", 13)
        return prefix + suffix

    def generate_boc(self) -> str:
        """生成中国银行银行卡号"""
        return self.generate(self.BOC)

    def generate_ccb(self) -> str:
        """生成建设银行银行卡号"""
        return self.generate(self.CCB)

    def generate_abc(self) -> str:
        """生成农业银行银行卡号"""
        return self.generate(self.ABC)

    def generate_icbc(self) -> str:
        """生成工商银行银行卡号"""
        return self.generate(self.ICBC)

    def generate_psbc(self) -> str:
        """生成邮储银行银行卡号"""
        return self.generate(self.PSBC)

    def generate_all_banks(self) -> Dict[str, str]:
        """
        生成所有银行的银行卡号

        Returns:
            {银行类型: 卡号} 字典
        """
        return {
            self.BOC: self.generate_boc(),
            self.CCB: self.generate_ccb(),
            self.ABC: self.generate_abc(),
            self.ICBC: self.generate_icbc(),
            self.PSBC: self.generate_psbc(),
        }
