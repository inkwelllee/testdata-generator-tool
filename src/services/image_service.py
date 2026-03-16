"""
图片生成服务
"""
import os
import logging
import threading
from typing import Optional, Tuple
import PIL.Image as PImage
from PIL import ImageFont, ImageDraw

from src.configs import ConfigManager
from .path_service import PathService


class ImageService:
    """图片生成服务"""

    def __init__(self, config_manager: ConfigManager):
        """
        初始化图片服务

        Args:
            config_manager: 配置管理器
        """
        self.config = config_manager
        self.path_service = PathService()

    def _get_font(self, font_name: str, size: int = 24) -> ImageFont.FreeTypeFont:
        """
        获取字体

        Args:
            font_name: 字体配置名称
            size: 字体大小

        Returns:
            字体对象
        """
        font_config = self.config.image_config.get('FONTS', {})
        font_file = font_config.get(font_name, font_config.get('DEFAULT', 'fonts/hei.ttf'))
        # font_file 已经包含 fonts/ 前缀
        font_path = os.path.join(self.path_service.base_dir, font_file)
        return ImageFont.truetype(font_path, size)

    def generate_id_card_image(
        self,
        name: str,
        sex: int,
        birth_date: str,
        id_card: str,
        save_path: str
    ) -> str:
        """
        生成身份证图片

        Args:
            name: 姓名
            sex: 性别 (1=男, 0=女)
            birth_date: 出生日期 (YYYY-MM-DD)
            id_card: 身份证号
            save_path: 保存路径

        Returns:
            生成的图片路径
        """
        birth_date_clean = birth_date.replace("-", "")

        # 选择头像
        if sex == 1:
            avatar_path = self.path_service.get_image_path('pengyy.jpeg')
        else:
            avatar_path = self.path_service.get_image_path('liuyf.jpg')

        avatar = PImage.open(avatar_path)

        # 加载模板
        empty_image_path = self.path_service.get_image_path('empty.png')
        empty_image = PImage.open(empty_image_path)
        empty_image = empty_image.convert("RGB")

        # 加载字体
        name_font = self._get_font('DEFAULT', 24)
        other_font = self._get_font('DEFAULT', 24)
        birth_date_font = self._get_font('BIRTH_DATE', 24)
        id_font = self._get_font('ID_CARD', 24)

        draw = ImageDraw.Draw(empty_image)

        # 绘制姓名
        draw.text((260, 290), name, fill=(0, 0, 0), font=name_font)

        # 绘制性别和民族
        draw.text((260, 345), '男' if sex == 1 else '女', fill=(0, 0, 0), font=other_font)
        draw.text((420, 345), '汉', fill=(0, 0, 0), font=other_font)

        # 绘制出生日期
        draw.text((260, 400), birth_date_clean[:4], fill=(0, 0, 0), font=birth_date_font)
        draw.text((390, 400), birth_date_clean[4:6], fill=(0, 0, 0), font=birth_date_font)
        draw.text((470, 400), birth_date_clean[6:], fill=(0, 0, 0), font=birth_date_font)

        # 绘制住址
        try:
            region_key = self.config.area_info[int(id_card[0:4] + '00')]
            addr = self.config.area_info[int(id_card[0:6])]
        except KeyError:
            addr = '北京市朝阳区'
            region_key = '朝阳区'

        start = 0
        addr_loc_y = 460
        while start < len(addr):
            draw.text((260, addr_loc_y), addr[start:start + 11], fill=(0, 0, 0), font=other_font)
            start += 11
            addr_loc_y += 50

        # 绘制身份证号
        draw.text((350, 610), id_card, fill=(0, 0, 0), font=id_font)

        # 绘制背面信息
        draw.text((440, 1130), addr.replace(region_key, '') + '公安局', fill=(0, 0, 0), font=other_font)
        draw.text((440, 1190), '2020.10.01-2030.10.01', fill=(0, 0, 0), font=other_font)

        # 粘贴头像
        avatar = avatar.resize((180, 250))
        avatar = avatar.convert('RGBA')
        empty_image.paste(avatar, (620, 290), mask=avatar)

        # 保存图片
        filename = f'{name}.png'
        image_path = os.path.join(save_path, filename)
        empty_image.save(image_path)

        logging.info(f"身份证图片已生成: {image_path}")
        return f'文件已生成：{image_path}'

    def generate_business_license_image(
        self,
        company_name: str,
        credit_code: str,
        name: str,
        save_path: str
    ) -> str:
        """
        生成营业执照图片

        Args:
            company_name: 公司名称
            credit_code: 统一社会信用代码
            name: 法人姓名
            save_path: 保存路径

        Returns:
            生成的图片路径
        """
        # 加载模板
        template_path = self.path_service.get_image_path('business_license.png')
        empty_image = PImage.open(template_path)
        empty_image = empty_image.convert("RGB")

        # 加载字体
        name_font = self._get_font('DEFAULT', 24)

        draw = ImageDraw.Draw(empty_image)

        # 绘制信息
        draw.text((180, 310), credit_code, fill=(0, 0, 0), font=name_font)
        draw.text((313, 468), company_name, fill=(0, 0, 0), font=name_font)
        draw.text((315, 552), name, fill=(0, 0, 0), font=name_font)

        # 保存图片
        filename = f'{company_name}.png'
        image_path = os.path.join(save_path, filename)
        empty_image.save(image_path)

        logging.info(f"营业执照图片已生成: {image_path}")
        return f'文件已生成：{image_path}'
