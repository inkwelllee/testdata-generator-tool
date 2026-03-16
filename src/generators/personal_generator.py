"""
个人信息生成器
"""
import random
from typing import Dict, List
from .data_generator import DataGenerator


class PersonalGenerator(DataGenerator):
    """个人信息生成器（姓名、地址等）"""

    def __init__(
        self,
        name_data: Dict[str, List[str]],
        area_info: Dict[int, str]
    ):
        """
        初始化个人信息生成器

        Args:
            name_data: 姓名数据 {SURNAMES: [...], MALE_NAMES: [...], FEMALE_NAMES: [...]}
            area_info: 地区信息 {区号: 地区名}
        """
        self.name_data = name_data
        self.area_info = area_info

    def generate_name(self, gender: int) -> str:
        """
        生成姓名

        Args:
            gender: 性别 (1=男, 0=女)

        Returns:
            姓名
        """
        surname = self.random_choice(self.name_data['SURNAMES'])

        if gender == 0:
            # 女性
            given_name = self.random_choice(self.name_data['FEMALE_NAMES'])
        else:
            # 男性
            given_name = self.random_choice(self.name_data['MALE_NAMES'])

        return surname + given_name

    def generate_address(self) -> str:
        """
        生成地址

        Returns:
            地址字符串
        """
        # 随机选择一个地区
        address = self.random_choice(list(self.area_info.values()))

        # 添加详细地址
        road_names = ["人民路", "建设路", "解放路", "和平路", "文化路", "中山路", "北京路", "上海路"]
        road = self.random_choice(road_names)
        number = self.random_int(1, 999)

        return f"{address}{road}{number}号"

    def get_area_by_code(self, code: str) -> str:
        """
        根据身份证前6位获取地区名称

        Args:
            code: 身份证前6位

        Returns:
            地区名称
        """
        try:
            # 先尝试精确匹配
            if int(code) in self.area_info:
                return self.area_info[int(code)]
            # 尝试前4位+00
            region_code = int(code[:4] + "00")
            if region_code in self.area_info:
                return self.area_info[region_code]
        except (ValueError, KeyError):
            pass
        return "北京市朝阳区"
