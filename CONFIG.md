# 程序配置说明

## 主要配置选项

在 `main.py` 文件顶部的 `CONFIG` 字典中可以配置程序行为：

```python
CONFIG = {
    # 日志配置
    'enable_file_logging_in_production': True,   # 打包后是否启用文件日志
    'use_pywebview_directory': True,             # 是否使用pywebview目录
    
    # 缓存配置
    'clear_cache_on_startup': False,             # 启动时是否清除缓存
}
```

## 配置项详解

### 日志配置

#### `enable_file_logging_in_production`
- **类型**: Boolean
- **默认值**: `True`
- **说明**: 控制打包后的程序是否生成日志文件
- **选项**:
  - `True`: 打包后生成日志文件
  - `False`: 打包后仅控制台输出，不生成日志文件

#### `use_pywebview_directory`
- **类型**: Boolean  
- **默认值**: `True`
- **说明**: 控制日志文件的存放位置
- **选项**:
  - `True`: 使用pywebview目录 (`%APPDATA%/pywebview/logs/`)
  - `False`: 使用应用目录 (`应用目录/logs/`)

### 缓存配置

#### `clear_cache_on_startup`
- **类型**: Boolean
- **默认值**: `False`
- **说明**: 控制程序启动时是否自动清除webview缓存
- **选项**:
  - `True`: 启动时自动清除缓存（开发调试时推荐）
  - `False`: 启动时不清除缓存（正常使用推荐）

## 使用场景

### 开发调试
```python
CONFIG = {
    'enable_file_logging_in_production': True,
    'use_pywebview_directory': True,
    'clear_cache_on_startup': True,  # 确保每次启动都使用最新页面
}
```

### 生产发布
```python
CONFIG = {
    'enable_file_logging_in_production': True,
    'use_pywebview_directory': True,
    'clear_cache_on_startup': False,  # 保持缓存，提高启动速度
}
```

### 最小化版本
```python
CONFIG = {
    'enable_file_logging_in_production': False,  # 不生成日志文件
    'use_pywebview_directory': False,
    'clear_cache_on_startup': False,
}
```

## API方法

程序还提供了以下API方法供前端调用：

- `clearCache()`: 清除浏览器缓存并刷新页面
- `clearSystemCache()`: 清除系统webview缓存目录
- `getCacheInfo()`: 获取缓存目录信息和大小

## 注意事项

1. **缓存清理**: 启用 `clear_cache_on_startup` 会在每次启动时删除webview缓存，确保使用最新的页面文件，但会稍微增加启动时间。

2. **日志位置**: 使用pywebview目录可以避免在应用目录产生文件，保持应用目录整洁。

3. **权限问题**: pywebview目录通常有更好的写入权限，减少权限相关的问题。