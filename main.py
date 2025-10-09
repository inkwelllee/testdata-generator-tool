import mimetypes
import os
import sys
import webview
import logging

# 配置日志记录
logging.basicConfig(
    filename="output.log",  # 日志文件名
    level=logging.INFO,      # 记录日志的级别
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 在终端和日志文件同时输出
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# 示例日志
logging.info("程序开始执行")

 
from backend.gen import numberGen

# 配置关闭提示
chinese = {
    'global.quitConfirmation': '暂别勿思念，转瞬与亲见',
}

if getattr(sys, 'frozen', None):
    web_dir = os.path.join(sys._MEIPASS, 'gui')
else:
    web_dir = os.path.join(os.path.abspath("."), 'gui')

class Api:
    def __init__(self) -> None:
        numberGen.__init__(self)
        self._window = None

    def set_window(self, window):
        self._window = window

    def quit(self):
        self._window.destroy()

    def randomName(self, sex):
        return numberGen.random_name(self, sex)
    
    def randomIdCard(self, sex, birth_date):
        return numberGen.random_id_card(self, sex, birth_date)
    
    def randomPhoneNumber(self):
        return numberGen.random_phone_number(self)
    
    def randomEmail(self):
        return numberGen.random_email(self)
    
    def randomCompanyName(self):
        return numberGen.random_company_name(self)
    
    def randomSocialCreditCode(self):
        return numberGen.random_credit_code(self)
    
    def randomOrganizationCode(self):
        return numberGen.random_organ_code(self)
    
    def randomZhongzhengCode(self):
        return numberGen.random_pbc_code(self)
    
    def randomBankAccount(self, bankType):
        return numberGen.random_bank_account(self, bankType)
    
    def generateIdCardImage(self, name, sex, birth_date, idCard, directoryPath):
        return numberGen.handle_image(self, name, sex, birth_date, idCard, directoryPath)
    
    def generateBusinessImage(self, companyName, creditCode, name, directoryPath):
        return numberGen.handle_business_image(self, companyName, creditCode, name, directoryPath)
    
    def changeDirectory(self, directoryType):
        return numberGen.change_directory(self, directoryType)
    
    def checkPath(self, directoryPath):
        return numberGen.check_path(self, directoryPath)

    # 关闭窗口
    def destroyApp(self):
        self._window.destroy()

    # 最小化窗口
    def minimizeApp(self):
        self._window.minimize()

    # 最大化窗口
    def maximizeApp(self):
        self._window.maximize()

    # 还原窗口
    def restoreApp(self):
        self._window.restore()

    # 调整窗口大小
    def resizeApp(self, width, height):
        self._window.resize(width, height)

    def test(self):
        self._window.resize(1420, 720)

def main():
    logging.info("程序开始执行 => main")
    # 实例化Api类
    api = Api()
    logging.info("程序开始执行 => api")
    # 系统分辨率
    screens = webview.screens
    screens = screens[0]
    width = screens.width
    # height = screens.height
    logging.info("程序开始执行 => width")
    # 窗口大小
    initWidth = 1200
    initHeight = 660
    # initHeight = int(height * 2 / 3)
    logging.info("程序开始执行 => initHeight")
    # template = os.path.join(web_dir, "dist/index.html") 
    mimetypes.add_type('application/javascript', '.js')
    logging.info("程序开始执行 => mimetypes")
    #window = webview.create_window(title='BlingBling', url='http://localhost:8098', width=initWidth, height=initHeight, js_api=api, resizable=True, text_select=False, confirm_close=False, frameless=True, easy_drag=False)
    #window = webview.create_window(title='BlingBling', url='http://inkwell.top/gen_ui', width=initWidth, height=initHeight, js_api=api, resizable=True, text_select=False, confirm_close=False, frameless=True, easy_drag=False)
    window = webview.create_window('BlingBling', 'asserts/ui/index.html', width=initWidth, height=initHeight, js_api=api, resizable=True, text_select=False, confirm_close=False, frameless=True, easy_drag=False)        
    logging.info("程序开始执行 => window")
    api.set_window(window)
    logging.info("程序开始执行 => api.set_window(window)")
    webview.start(localization=chinese, 
                  http_server=True, 
                  private_mode=False, 
                  gui=None,
                  # debug=True
                  )
    logging.info("程序开始执行 => webview.start")

if __name__ == '__main__':
    main()