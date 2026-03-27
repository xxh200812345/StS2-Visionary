"""
StS2-Visionary 日志管理模块
负责初始化日志系统，实现每日轮转并保留最近 5 天的日志文件。
"""

import logging
from logging.handlers import TimedRotatingFileHandler
import os


def setup_logger():
    """
    配置并初始化日志处理器。
    设置 TimedRotatingFileHandler 以实现日志的自动轮转和清理。
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "sts2_visionary.log")

    # 创建全局 logger 实例，内部命名避免与外部变量冲突
    _logger = logging.getLogger("StS2_Visionary")
    _logger.setLevel(logging.DEBUG)

    # 防止重复添加 Handler
    if not _logger.handlers:
        # 核心配置：按天轮转 (D)，间隔 1 天，保留 5 个备份
        file_handler = TimedRotatingFileHandler(
            log_file, when='D', interval=1, backupCount=5, encoding='utf-8'
        )

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(module)s] - %(message)s'
        )
        file_handler.setFormatter(formatter)

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        _logger.addHandler(file_handler)
        _logger.addHandler(console_handler)

    return _logger


# 初始化全局单例 logger
logger = setup_logger()
