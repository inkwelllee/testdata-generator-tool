"""
日志配置模块
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(enable_file_logging=True, use_pywebview_dir=True):
    """
    配置日志记录
    
    Args:
        enable_file_logging: 打包后是否启用文件日志
        use_pywebview_dir: 是否使用pywebview目录
    
    Returns:
        tuple: (log_file_path, logs_directory)
    """
    # 清除现有处理器
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建格式器
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    
    # 配置根日志器
    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(console_handler)
    
    log_file = None
    logs_dir = None
    
    # 判断是否需要文件日志
    is_frozen = getattr(sys, 'frozen', False)
    # is_frozen = True  # 取消注释测试打包环境
    need_file_log = not is_frozen or enable_file_logging
    
    if need_file_log:
        try:
            if is_frozen and use_pywebview_dir:
                # 打包后使用pywebview目录
                if sys.platform == "win32":
                    logs_dir = os.path.join(os.environ.get('APPDATA', ''), 'pywebview', 'logs')
                else:
                    logs_dir = os.path.join(os.path.expanduser('~'), '.pywebview', 'logs')
                
                log_filename = "app.log"
                max_bytes = 2*1024*1024  # 2MB
                backup_count = 3
            else:
                # 开发环境或应用目录
                if is_frozen:
                    base_dir = os.path.dirname(sys.executable)
                else:
                    # src/utils/logger.py -> src -> project_root
                    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
                logs_dir = os.path.join(base_dir, "logs")
                log_filename = "output.log"
                max_bytes = 5*1024*1024  # 5MB
                backup_count = 5
            
            # 创建日志目录
            os.makedirs(logs_dir, exist_ok=True)
            log_file = os.path.join(logs_dir, log_filename)
            
            # 创建文件处理器
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            
            # 添加文件处理器
            logging.root.addHandler(file_handler)
            
        except Exception as e:
            print(f"创建日志文件失败: {e}")
            log_file = None
            logs_dir = None
    
    return log_file, logs_dir


def log_startup_info(log_file_path, logs_directory, enable_file_logging, use_pywebview_dir):
    """记录程序启动信息"""
    logging.info("=" * 50)
    logging.info("程序启动")
    logging.info(f"运行环境: {'打包环境' if getattr(sys, 'frozen', False) else '开发环境'}")
    logging.info(f"日志配置: 文件日志={'启用' if enable_file_logging else '禁用'}, pywebview目录={'启用' if use_pywebview_dir else '禁用'}")
    
    if logs_directory:
        logging.info(f"日志目录: {logs_directory}")
        logging.info(f"日志文件: {log_file_path}")
    else:
        logging.info("日志文件: 仅控制台输出")
    
    logging.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 50)