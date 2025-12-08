import pyperclip as cp
import random
import tkinter as tk
import os
import sys
import PIL.Image as PImage
import threading
import cv2
import numpy

from datetime import datetime, timedelta
from tkinter.messagebox import *
from PIL import ImageFont, ImageDraw

from backend.config.config_manager import ConfigManager

if getattr(sys, 'frozen', None):
    base_dir = os.path.join(sys._MEIPASS, 'asserts')
else:
    base_dir = os.path.join(os.path.abspath("."), 'asserts')

def set_entry_value(entry, value):
    entry.delete(0, tk.END)
    entry.insert(0, value)

def read_file(file_path):
    with open(base_dir + file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def generate_random_date(start_year=1960, end_year=2020):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    
    return random_date.strftime("%Y%m%d")

def calculate_checksum(id_number):
    factorArr = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
    parityBit = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
    
    intweightSum = sum(int(id_number[i]) * factorArr[i] for i in range(17))
    intCheckDigit = parityBit[intweightSum % 11]

    return intCheckDigit

# 定义校验码计算函数
def calculate_check_digit(code):
    # 权重系数
    ws = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
    # 字符映射
    str_chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    
    # 验证代码长度
    if len(code) != 17:
        raise ValueError("Input code must be 17 characters long")
    
    # 确保所有字符在映射表中
    for char in code:
        if char not in str_chars:
            raise ValueError(f"Character '{char}' not found in mapping table")

    # 计算加权和
    sum_val = sum(str_chars.index(char) * ws[i] for i, char in enumerate(code))

    # 计算校验码
    check_digit_num = 31 - (sum_val % 31)
    if check_digit_num > 30:
        check_digit = '0'
    else:
        check_digit = str_chars[check_digit_num]
    
    return check_digit

def calculate_org_code_check_digit(org_code):
    # 权重系数
    ws = [3, 7, 9, 10, 5, 8, 4, 2]
    # 字符映射
    str_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # 计算加权和
    sum_val = sum(str_chars.index(char) * ws[i] for i, char in enumerate(org_code[:8]))
    
    # 计算校验码
    check_digit_num = 11 - (sum_val % 11)
    if check_digit_num == 11:
        check_digit = '0'
    elif check_digit_num == 10:
        check_digit = 'X'
    else:
        check_digit = str(check_digit_num)
    
    return check_digit
    
def generate_org_code():
    chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    org_code = ''.join(random.choice(chars) for _ in range(8))
    check_digit = calculate_org_code_check_digit(org_code)

    return org_code + '-' + check_digit

def generate_bank_card(self, bank_type):
    prefix = random.choice(self.config.bank_prefixes.get(bank_type, ['666666']))
    suffix = ''.join(random.choices("0123456789", k=13))
    
    # 拼接为19位银行卡号
    bank_card_number = prefix + suffix
    
    return bank_card_number

# 根据性别随机生成三位顺序码
def generate_sequence_code(gender):
    while True:
        sequence_code = random.randint(100, 999)
        
        if gender == 1:
            if sequence_code % 2 != 0:
                break
        else:
            if sequence_code % 2 == 0:
                break
    
    return str(sequence_code)

# 验证输入的日期字符串格式是否正确
def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y%m%d")
        return True
    except ValueError:
        return False

def is_empty(value):
    return not value

def change_background(img, img_back, zoom_size, center):
    # 缩放
    img = cv2.resize(img, zoom_size)
    rows, cols, channels = img.shape

    # 转换hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取mask
    # lower_blue = np.array([78, 43, 46])
    # upper_blue = np.array([110, 255, 255])
    diff = [5, 30, 30]
    gb = hsv[0, 0]
    lower_blue = numpy.array(gb - diff)
    upper_blue = numpy.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('Mask', mask)

    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 粘贴
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 0:  # 0代表黑色的点
                img_back[center[0] + i, center[1] + j] = img[i, j]  # 此处替换颜色，为BGR通道

    return img_back

class numberGen:
    def __init__(self):
        self.config = ConfigManager()

    # 姓名
    def random_name(self, sex):
        # 随机生成姓氏
        name_xing = random.choice(self.config.name_data['SURNAMES'])

        if sex == 0:
            # 女性
            name_ming = random.choice(self.config.name_data['FEMALE_NAMES'])
        else:
            # 男性
            name_ming = random.choice(self.config.name_data['MALE_NAMES'])

        return name_xing + name_ming

    # 手机号
    def random_phone_number(self):
        prefix = random.choice(self.config.phone_prefixes)
        remaining_digits = ''.join(random.choices("0123456789", k=9))
        phone_number = prefix + remaining_digits
        
        return phone_number
    
    def random_email(self):
        timestamp = int(datetime.now().timestamp())
        email = f"{timestamp}@qq.com"
        return email

    # 身份证号码
    def random_id_card(self, gender, birth_date):
        # 随机选择一个省级地区码
        lines = read_file("/areaCode.txt")
        region_code = random.choice(lines)
        
        birth_date = birth_date.replace("-", "")
        
        # 随机生成后三位顺序码
        sequence_code = generate_sequence_code(gender)
        
        # 拼接前17位
        id_number_17 = region_code + birth_date + sequence_code
        
        # 计算校验码
        checksum = calculate_checksum(id_number_17)
        
        # 生成完整的身份证号
        id_number = id_number_17 + checksum
        
        return id_number

    # 公司名称
    def random_company_name(self):
        first_word = random.choice(self.config.company_name_data['POSITIVE_WORDS'])
        second_part = random.choice(self.config.company_name_data['DESCRIPTIVE_WORDS'])
        industry_word = random.choice(self.config.company_name_data['INDUSTRY_WORDS'])
        
        return f"{first_word}{second_part}{industry_word}公司"

    # 统一社会信用代码
    def random_credit_code(self):
        # 随机选择登记管理部门代码
        management_code = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'N', 'Y'])
        
        # 随机选择机构类别代码
        department_code = {
            '1': '1',
            '2': random.choice(['1', '9']),
            '3': random.choice(['1', '2', '3', '4', '5', '9']),
            '4': random.choice(['1', '9']),
            '5': random.choice(['1', '2', '3', '9']),
            '6': random.choice(['1', '2', '9']),
            '7': random.choice(['1', '2', '9']),
            '8': random.choice(['1', '9']),
            '9': random.choice(['1', '2', '3']),
            'A': random.choice(['1', '9']),
            'N': random.choice(['1', '2', '3', '9']),
            'Y': '1'
        }
        institution_code = department_code[management_code]
        
        # 读取行政区划码，这里假设我们已经有了行政区划码列表
        lines = read_file("/areaCode.txt")
        administrative_code = random.choice(lines)
        
        # 生成组织机构代码
        self.organization_code = generate_org_code()
        
        # 生成校验码
        usc_code = management_code + institution_code + administrative_code + self.organization_code.replace("-", "")

        check_digit = calculate_check_digit(usc_code)
        
        # 返回完整的统一社会信用代码
        return usc_code + check_digit

    # 组织机构代码
    def random_organ_code(self):
        # 生成组织机构代码
        self.organization_code = generate_org_code()
        
        return self.organization_code

    # 中征码
    def random_pbc_code(self):
        # 加权因子
        weight_factor = [1, 3, 5, 7, 11, 2, 13, 1, 1, 17, 19, 97, 23, 29]
        # 生成前14位的随机字符（包括数字和大写字母）
        chars = '0123456789'
        id_code = ''.join(random.choices(chars, k=14))

        # 计算校验位
        num = 0
        for i in range(14):
            if 'A' <= id_code[i] <= 'Z':
                temp = ord(id_code[i]) - 55  # 字母转数字
            else:
                temp = ord(id_code[i]) - 48  # 数字直接转
            num += temp * weight_factor[i]

        # 取余+1
        residue = num % 97 + 1

        # 将校验位拼接到前14位生成完整的中征码
        code = f"{residue:02d}"  # 校验位确保两位
        
        return id_code + code

    def random_bank_account(self, type):
        return generate_bank_card(self, type)

    def random_boc_code(self): 
        bank_card_no = generate_bank_card(self, 'BOC')

        set_entry_value(self.boccode, bank_card_no)

    def random_ccb_code(self): 
        bank_card_no = generate_bank_card(self, 'CCB')

        set_entry_value(self.ccbcode, bank_card_no)

    def random_abc_code(self): 
        bank_card_no = generate_bank_card(self, 'ABC')

        set_entry_value(self.abccode, bank_card_no)
    
    def random_icbc_code(self): 
        bank_card_no = generate_bank_card(self, 'ICBC')

        set_entry_value(self.icbccode, bank_card_no)

    def random_psbc_code(self):
        bank_card_no = generate_bank_card(self, 'PSBC')

        set_entry_value(self.psbccode, bank_card_no)
        self.random_boc_code()
        self.random_ccb_code()
        self.random_abc_code()
        self.random_icbc_code()
        self.random_psbc_code()

    # 车牌号
    def random_license_plate(self):
        provinces = ["京", "津", "沪", "渝", "冀", "豫", "云", "辽", "黑", "湘", "皖", "鲁", "新", "苏", "浙", "赣", "鄂", "桂", "甘", "晋", "蒙", "陕", "吉", "闽", "贵", "粤", "青", "藏", "川", "宁", "琼"]
        province = random.choice(provinces)
        alpha = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        suffix = "".join(random.choice(alphanumeric) for _ in range(5))
        return province + alpha + suffix

    # 车架号 (VIN)
    def random_vin(self):
        # 简单生成17位VIN
        chars = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
        vin = "".join(random.choice(chars) for _ in range(17))
        return vin

    # 发动机号
    def random_engine_no(self):
        # 简单生成发动机号
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        engine_no = "".join(random.choice(chars) for _ in range(random.randint(6, 10)))
        return engine_no

    # 地址
    def random_address(self):
        # 随机选择一个地址
        address = random.choice(list(self.config.area_info.values()))
        # 增加详细地址
        road_names = ["人民路", "建设路", "解放路", "和平路", "文化路", "中山路", "北京路", "上海路"]
        road = random.choice(road_names)
        number = random.randint(1, 999)
        return f"{address}{road}{number}号"

    def resetAll(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def copy_to_clipboard(self, text):
        cp.copy(text)
        showinfo('成功', '复制成功')

    def generateIdCardImage(self):
        if is_empty(self.ename.get()) and is_empty(self.gender.get()) and is_empty(self.birth_date_entry.get()) and is_empty(self.eidn.get()) :
            showinfo('错误', '请先生成数据')
            return
        
        # self.loading_bar = loading_alert.LoadingBar(title="提示", content="图片正在生成...")
        # self.loading_bar.show(self.root)

        # 开启新线程保持滚动条显示
        wait_thread = threading.Thread(target=self.handle_image)
        wait_thread.setDaemon(True)
        wait_thread.start()

    def handle_image(self, name, sex, birth_date, idCard, path):
        birth_date = birth_date.replace("-", "")
        if sex == 1 :
            avatar = PImage.open(os.path.join(base_dir, 'images/pengyy.jpeg'))
        else :
            avatar = PImage.open(os.path.join(base_dir, 'images/liuyf.jpg')) 

        empty_image = PImage.open(os.path.join(base_dir, 'images/empty.png'))
        empty_image = empty_image.convert("RGB")

        name_font = ImageFont.truetype(os.path.join(base_dir, self.config.image_config['FONTS']['DEFAULT']), 24)
        other_font = ImageFont.truetype(os.path.join(base_dir, self.config.image_config['FONTS']['DEFAULT']), 24)
        birth_date_font = ImageFont.truetype(os.path.join(base_dir, self.config.image_config['FONTS']['BIRTH_DATE']), 24)
        id_font = ImageFont.truetype(os.path.join(base_dir, self.config.image_config['FONTS']['ID_CARD']), 24)

        draw = ImageDraw.Draw(empty_image)
        draw.text((260, 290), name, fill=(0, 0, 0), font=name_font)
        draw.text((260, 345), '男' if sex == 1 else '女', fill=(0, 0, 0), font=other_font)
        draw.text((420, 345), '汉', fill=(0, 0, 0), font=other_font)
        draw.text((260, 400), birth_date[:4], fill=(0, 0, 0), font=birth_date_font)
        draw.text((390, 400), birth_date[4:6], fill=(0, 0, 0), font=birth_date_font)
        draw.text((470, 400), birth_date[6:], fill=(0, 0, 0), font=birth_date_font)

        # 住址
        try:
            region_key = self.config.area_info[int(idCard[0:4] + '00')]
            addr = self.config.area_info[int(idCard[0:6])]
        except KeyError:
            addr = '北京市朝阳区'
            region_key = '朝阳区'
        
        start = 0
        addr_loc_y = 460
        while start < len(addr):
            draw.text((260, addr_loc_y), addr[start:start + 11], fill=(0, 0, 0), font=other_font)
            start += 11
            addr_loc_y += 50

        # 身份证号
        draw.text((350, 610), idCard, fill=(0, 0, 0), font=id_font)

        # 背面
        draw.text((440, 1130), addr.replace(region_key, '') + '公安局', fill=(0, 0, 0), font=other_font)
        draw.text((440, 1190), '2020.10.01-2030.10.01', fill=(0, 0, 0), font=other_font)

        avatar = avatar.resize((180, 250))
        avatar = avatar.convert('RGBA')
        empty_image.paste(avatar, (620, 290), mask=avatar)

        filename = f'{name}.png'

        # 指定图像的保存路径和文件名
        image_path = os.path.join(path, filename)
        print(image_path)
        empty_image.save(image_path)

        # self.loading_bar.close()
        # showinfo('成功', f'文件已生成: {filename}')
        return '文件已生成：' + image_path

    def generateBusinessLicenseImage(self):
        if is_empty(self.ecreditcode.get()) and is_empty(self.ecompanyname.get()) and is_empty(self.ename.get()) :
            showinfo('错误', '请先生成数据')
            return

        # self.loading_bar = loading_alert.LoadingBar(title="提示", content="图片正在生成...")
        # self.loading_bar.show(self.root)

        # 开启新线程保持滚动条显示
        wait_thread = threading.Thread(target=self.handle_business_image)
        wait_thread.setDaemon(True)
        wait_thread.start()

    def handle_business_image(self, company_name, credit_code, name, path):
        empty_image = PImage.open(os.path.join(base_dir, 'images/business_license.png'))
        empty_image = empty_image.convert("RGB")

        name_font = ImageFont.truetype(os.path.join(base_dir, self.config.image_config['FONTS']['DEFAULT']), 24)

        draw = ImageDraw.Draw(empty_image)
        draw.text((180, 310), credit_code, fill=(0, 0, 0), font=name_font)
        draw.text((313, 468), company_name, fill=(0, 0, 0), font=name_font)
        draw.text((315, 552), name, fill=(0, 0, 0), font=name_font)

        filename = f'{company_name}.png'

        # 指定图像的保存路径和文件名
        image_path = os.path.join(path, filename)
        empty_image.save(image_path)

        # self.loading_bar.close()
        # showinfo('成功', f'文件已生成: {filename}')
        return '文件已生成：' + image_path
    
    def change_directory(self, directoryType):
        if directoryType == 'desktop':
            directory = os.path.join(os.path.expanduser("~"), "Desktop")
        elif directoryType == 'follow':
            directory = os.getcwd()
        else:
            directory = ''
        
        return directory
        # if not os.path.exists(directory):
        #     os.makedirs(directory)
        #     showinfo('成功','目录创建成功')

    def check_path(self, directoryPath):
        if not os.path.exists(directoryPath):
            return False
        else:
            return True