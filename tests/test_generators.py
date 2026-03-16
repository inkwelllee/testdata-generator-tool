"""
数据生成器测试
"""
import pytest
from src.generators import (
    IDGenerator,
    PhoneGenerator,
    BankGenerator,
    VehicleGenerator,
    PersonalGenerator,
)
from src.configs import ConfigManager


class TestIDGenerator:
    """身份证生成器测试"""

    def setup_method(self):
        config = ConfigManager()
        self.generator = IDGenerator(config.area_codes)

    def test_generate_male_id(self):
        """测试生成男性身份证"""
        id_card = self.generator.generate(1, "1990-01-15")
        assert len(id_card) == 18
        assert id_card[-2] in '13579X'  # 男性顺序码为奇数

    def test_generate_female_id(self):
        """测试生成女性身份证"""
        id_card = self.generator.generate(0, "1995-06-20")
        assert len(id_card) == 18
        assert id_card[-2] in '02468'  # 女性顺序码为偶数

    def test_checksum_valid(self):
        """测试校验码计算"""
        id_card = self.generator.generate(1, "1985-03-10")
        # 校验码应为最后一位
        assert IDGenerator.calculate_checksum(id_card[:17]) == id_card[17]


class TestPhoneGenerator:
    """手机号生成器测试"""

    def setup_method(self):
        config = ConfigManager()
        self.generator = PhoneGenerator(config.phone_prefixes)

    def test_generate_phone(self):
        """测试生成手机号"""
        phone = self.generator.generate_phone()
        assert len(phone) == 11
        assert phone.startswith(('13', '14', '15', '16', '17', '18', '19'))

    def test_generate_email(self):
        """测试生成邮箱"""
        email = self.generator.generate_email()
        assert '@' in email
        assert email.endswith('@qq.com')


class TestBankGenerator:
    """银行卡生成器测试"""

    def setup_method(self):
        config = ConfigManager()
        self.generator = BankGenerator(config.bank_prefixes)

    def test_generate_boc_card(self):
        """测试生成中国银行卡"""
        card = self.generator.generate('BOC')
        assert len(card) == 19

    def test_generate_all_banks(self):
        """测试生成所有银行"""
        all_cards = self.generator.generate_all_banks()
        assert len(all_cards) == 5
        for bank_type, card in all_cards.items():
            assert len(card) == 19


class TestVehicleGenerator:
    """车辆信息生成器测试"""

    def setup_method(self):
        self.generator = VehicleGenerator()

    def test_generate_license_plate(self):
        """测试生成车牌号"""
        plate = self.generator.generate_license_plate()
        # 格式：省份(1) + 字母(1) + 字母数字(5) = 7位
        assert len(plate) == 7

    def test_generate_vin(self):
        """测试生成车架号"""
        vin = self.generator.generate_vin()
        assert len(vin) == 17
        # VIN 不包含 I, O, Q
        assert 'I' not in vin
        assert 'O' not in vin
        assert 'Q' not in vin

    def test_generate_engine_no(self):
        """测试生成发动机号"""
        engine_no = self.generator.generate_engine_no()
        assert 6 <= len(engine_no) <= 10
