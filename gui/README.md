# 开心果前端

基于 Vue 3 + Quasar 的测试数据生成器前端界面。

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Quasar** - 跨平台 Vue 组件库
- **Pinia** - Vue 状态管理
- **Vite** - 下一代前端构建工具
- **Vue Router** - 官方路由管理器

## 目录结构

```
gui/
├── src/
│   ├── api/                    # API 封装层
│   │   └── index.js            # 后端接口封装
│   ├── assets/                 # 静态资源
│   │   └── icons/
│   │       └── logo.svg        # 应用图标
│   ├── components/             # 公共组件
│   │   ├── BasicInfoGenerator.vue    # 基础信息生成器
│   │   ├── VehicleInfoGenerator.vue  # 车辆信息生成器
│   │   └── SettingsDrawer.vue        # 设置抽屉
│   ├── composables/            # 组合式函数
│   │   ├── useClipboard.js     # 剪贴板操作
│   │   ├── useGenerator.js     # 数据生成逻辑
│   │   └── useWindow.js        # 窗口控制
│   ├── router/                 # 路由配置
│   │   └── index.js
│   ├── stores/                 # Pinia 状态管理
│   │   ├── index.js
│   │   ├── app.js              # 应用状态
│   │   └── generator.js        # 生成器状态
│   ├── views/
│   │   └── generator.vue       # 主页面
│   ├── App.vue                 # 根组件
│   ├── main.js                 # 入口文件
│   └── quasar-variables.scss   # Quasar 变量覆盖
├── index.html
├── package.json
├── vite.config.js
└── vite-plugin-copy-to-ui.js   # 构建后复制插件
```

## 功能特性

- **基础信息生成**: 姓名、身份证、手机号、邮箱、地址
- **企业信息生成**: 公司名称、统一社会信用代码、组织机构代码
- **账号信息生成**: 银行卡号
- **车辆信息生成**: 车牌号、车架号、发动机号
- **图片生成**: 身份证图片、营业执照图片
- **深色模式**: 支持明暗主题切换
- **窗口控制**: 置顶、缩放、最小化、最大化

## 开发

### 安装依赖
```bash
npm install
```

### 开发模式
```bash
npm run dev
```

### 构建
```bash
npm run build
```

### 预览构建结果
```bash
npm run preview
```

## 与后端通信

前端通过 `window.pywebview.api` 与 Python 后端通信，API 封装在 `src/api/index.js`:

```javascript
// 数据生成
generatorApi.randomName(sex)
generatorApi.randomIdCard(sex, birthDate)
generatorApi.randomPhoneNumber()
// ...

// 窗口控制
windowApi.minimize()
windowApi.maximize()
windowApi.toggleAlwaysOnTop()
// ...

// 图片生成
imageApi.generateIdCardImage(name, sex, birthday, idCard, directory)
imageApi.generateBusinessImage(companyName, creditCode, name, directory)
```

## 状态管理

使用 Pinia 进行状态管理:

- **app store**: 窗口状态、目录配置、加载状态
- **generator store**: 表单数据、字段配置、API映射

## 样式

- 使用 Quasar 内置组件和样式系统
- 深色模式通过 `Dark` 插件控制
- 自定义样式在组件内使用 scoped CSS
