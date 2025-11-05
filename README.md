# testdata-generator-tool

一个用于生成各类号码的工具。

## 项目结构

```
testdata-generator-tool/
├── asserts/                          # 资源文件目录
│   ├── fonts/                        # 字体文件目录
│   │   ├── hei.ttf                   # 黑体字体
│   │   ├── ocrb10bt.ttf              # OCR-B字体
│   │   └── fzhei.ttf                 # 仿宋字体
│   ├── images/                       # 图片资源目录
│   │   ├── business_license.png      # 营业执照模板
│   │   ├── empty.png                 # 空白身份证模板
│   │   ├── liuyf.jpg                 # 女神刘亦菲
│   │   └── pengyy.jpeg               # 男神彭于晏
│   ├── ui/                           # 前端构建产物目录 (自动生成)
│   │   ├── assets/                   # 前端资源文件
│   │   ├── festival/                 # 节日动画文件
│   │   └── index.html                # 主页面文件
│   ├── areaCode.txt                  # 地区编码数据
│   ├── ico.icns                      # Mac应用图标
│   └── ico.ico                       # Windows应用图标
├── backend/                          # 后端Python目录
│   ├── config/                       # 配置文件目录
│   │   ├── __init__.py               # 包初始化文件
│   │   ├── config_manager.py         # 配置管理器
│   │   └── constants.py              # 常量配置
│   ├── __init__.py                   # 包初始化文件
│   └── gen.py                        # 数据生成工具类
├── gui/                              # 前端Vue项目目录
│   ├── src/                          # Vue源码目录
│   │   ├── components/               # Vue组件目录
│   │   │   └── FestivalAnimation.vue # 节日动画组件
│   │   ├── views/                    # 页面组件目录
│   │   │   ├── generator.vue         # 主生成器页面
│   │   │   └── index.vue             # 首页
│   │   ├── assets/                   # 前端资源文件
│   │   ├── router/                   # 路由配置
│   │   ├── utils/                    # 前端工具函数
│   │   ├── App.vue                   # 根组件
│   │   └── main.js                   # 入口文件
│   ├── scripts/                      # 构建脚本目录
│   │   ├── copy-to-ui.js             # Node.js复制脚本
│   │   ├── copy-to-ui.bat            # Windows批处理脚本
│   │   └── copy-to-ui.sh             # Unix/Linux脚本
│   ├── dist/                         # 构建输出目录 (自动生成)
│   ├── package.json                  # 前端依赖配置
│   ├── vite.config.js                # Vite构建配置
│   └── vite-plugin-copy-to-ui.js     # 自动复制插件
├── utils/                            # 工具模块目录
│   ├── __init__.py                   # 包初始化文件
│   ├── api.py                        # API类模块
│   ├── cache_manager.py              # 缓存管理模块
│   └── logger.py                     # 日志配置模块
├── logs/                             # 日志文件目录 (自动生成)
│   └── output.log                    # 应用日志文件
├── images/                           # 效果图目录
├── main.py                           # 主程序入口文件
├── CONFIG.md                         # 配置说明文档
├── .gitignore                        # Git忽略文件配置
└── README.md                         # 项目说明文档
```

## 架构特性

### 🏗️ 模块化设计
- **前后端分离**: Vue.js前端 + Python后端
- **模块化架构**: 日志、API、缓存管理等功能独立模块
- **自动化构建**: 前端构建完成后自动复制到运行目录

### 🔧 核心功能
- **数据生成**: 身份证、手机号、邮箱、公司名称等各类测试数据
- **图片生成**: 身份证、营业执照等证件图片生成
- **缓存管理**: 智能缓存清理和管理
- **日志系统**: 完善的日志记录和轮转机制
- **节日动画**: 特定日期显示节日祝福动画

### ⚙️ 配置管理
程序支持灵活的配置选项，详见 [CONFIG.md](CONFIG.md)：
- 日志文件位置配置
- 缓存清理策略配置
- 开发/生产环境适配

## 效果图展示
### vue版(pywebview)
![浅色](./images/example.jpg)
---
![深色](./images/example-dark.jpg)

## 环境依赖

### Python 依赖
```bash
# 剪切板操作
pip install pyperclip

# 图像处理
pip install opencv-python
pip install Pillow

# 数组计算
pip install numpy

# WebView支持
pip install pywebview
```

### 前端依赖 (可选，仅开发时需要)
```bash
# 进入前端目录
cd gui

# 安装Node.js依赖
npm install

# 或使用yarn
yarn install
```

### 前端主要依赖包
- **Vue 3**: 前端框架
- **Element Plus**: UI组件库
- **Vite**: 构建工具
- **Axios**: HTTP客户端
- **Moment.js**: 日期处理

## 运行程序

### 直接运行
```bash
# 直接运行主程序
python main.py
```

### 开发模式
```bash
# 1. 安装前端依赖
cd gui
npm install

# 2. 开发模式运行前端 (可选)
npm run dev

# 3. 构建前端并自动复制到运行目录
npm run build

# 4. 返回根目录运行主程序
cd ..
python main.py
```

### 配置选项
在 `main.py` 中可以配置程序行为：
```python
CONFIG = {
    'enable_file_logging_in_production': True,   # 打包后是否启用文件日志
    'use_pywebview_directory': True,             # 是否使用pywebview目录
    'clear_cache_on_startup': False,             # 启动时是否清除缓存
}
```

## 打包程序

### 准备工作
1. **构建前端**
   ```bash
   cd gui
   npm run build
   cd ..
   ```

2. **安装打包工具**
   ```bash
   pip install pyinstaller
   ```

### 打包命令

#### Windows 打包
```bash
pyinstaller -i asserts/ico.ico --name 测试数据生成器 --windowed --clean --noconfirm --onefile --add-data "asserts;asserts" main.py
```

#### Mac 打包
```bash
pyinstaller -i asserts/ico.icns --name 测试数据生成器 --windowed --clean --noconfirm --onefile --add-data ./asserts:./asserts main.py
```

#### Linux 打包
```bash
pyinstaller --name 测试数据生成器 --windowed --clean --noconfirm --onefile --add-data "./asserts:./asserts" main.py
```

### 打包说明
- 打包前确保已运行 `npm run build` 构建前端
- 打包后的程序包含完整的前端界面和后端逻辑
- 程序会自动在用户目录创建日志文件（可配置）
- 支持自动缓存管理和清理功能

## 开发说明

### 前端开发
- 前端使用Vue 3 + Element Plus开发
- 支持热重载开发模式
- 构建完成后自动复制到 `asserts/ui/` 目录
- 节日动画组件支持特定日期显示

### 后端开发  
- 模块化设计，功能分离
- 完善的日志系统和错误处理
- 支持跨平台缓存管理
- API接口支持前端调用

### 配置管理
- 集中配置管理，支持开发/生产环境切换
- 详细配置说明见 [CONFIG.md](CONFIG.md)
- 支持日志级别和位置配置

