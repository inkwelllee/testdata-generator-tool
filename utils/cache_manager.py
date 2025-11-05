"""
缓存管理模块
"""
import os
import sys
import shutil
import tempfile
import logging


def clear_webview_cache():
    """
    程序启动时清除webview缓存
    
    Returns:
        bool: 是否成功清除缓存
    """
    try:
        cache_dirs = []
        
        # Windows系统的webview缓存目录
        if sys.platform == "win32":
            cache_dirs.extend([
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'pywebview'),
                os.path.join(os.environ.get('APPDATA', ''), 'pywebview'),
                os.path.join(tempfile.gettempdir(), 'pywebview')
            ])
        else:
            # Linux/Mac系统
            cache_dirs.extend([
                os.path.join(os.path.expanduser('~'), '.pywebview'),
                os.path.join(tempfile.gettempdir(), 'pywebview')
            ])
        
        cleared_dirs = []
        
        # 清除缓存目录
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                try:
                    shutil.rmtree(cache_dir)
                    cleared_dirs.append(cache_dir)
                    logging.info(f"已清除缓存目录: {cache_dir}")
                except Exception as e:
                    logging.warning(f"无法清除缓存目录 {cache_dir}: {e}")
        
        if cleared_dirs:
            logging.info(f"缓存清理完成，共清除 {len(cleared_dirs)} 个目录")
            return True
        else:
            logging.info("未找到需要清除的缓存目录")
            return False
                    
    except Exception as e:
        logging.error(f"清除缓存时出错: {e}")
        return False


def get_cache_info():
    """
    获取缓存目录信息
    
    Returns:
        dict: 缓存目录信息
    """
    cache_info = {
        'directories': [],
        'total_size': 0,
        'total_files': 0
    }
    
    try:
        cache_dirs = []
        
        if sys.platform == "win32":
            cache_dirs.extend([
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'pywebview'),
                os.path.join(os.environ.get('APPDATA', ''), 'pywebview'),
                os.path.join(tempfile.gettempdir(), 'pywebview')
            ])
        else:
            cache_dirs.extend([
                os.path.join(os.path.expanduser('~'), '.pywebview'),
                os.path.join(tempfile.gettempdir(), 'pywebview')
            ])
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                dir_info = {
                    'path': cache_dir,
                    'size': 0,
                    'files': 0,
                    'exists': True
                }
                
                try:
                    for root, dirs, files in os.walk(cache_dir):
                        dir_info['files'] += len(files)
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                dir_info['size'] += os.path.getsize(file_path)
                            except (OSError, IOError):
                                pass
                except Exception as e:
                    logging.warning(f"无法获取目录信息 {cache_dir}: {e}")
                
                cache_info['directories'].append(dir_info)
                cache_info['total_size'] += dir_info['size']
                cache_info['total_files'] += dir_info['files']
            else:
                cache_info['directories'].append({
                    'path': cache_dir,
                    'size': 0,
                    'files': 0,
                    'exists': False
                })
    
    except Exception as e:
        logging.error(f"获取缓存信息时出错: {e}")
    
    return cache_info


def format_size(size_bytes):
    """
    格式化文件大小显示
    
    Args:
        size_bytes (int): 字节数
        
    Returns:
        str: 格式化后的大小字符串
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"