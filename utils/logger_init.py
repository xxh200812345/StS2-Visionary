"""
StS2-Visionary 日志管理模块
负责初始化日志系统，实现每日轮转并保留最近 5 天的日志文件。
"""

import logging
from logging.handlers import TimedRotatingFileHandler
from utils.constants import ROOT_DIR, LOG_DIR_NAME, LOG_FILE_NAME, LOG_BACKUP_COUNT, LOG_ROTATION_WHEN, PROJECT_NAME


def setup_logger():
    # 路径语义化拼接
    log_dir = ROOT_DIR / LOG_DIR_NAME
    log_file = log_dir / LOG_FILE_NAME

    # 自动创建目录
    log_dir.mkdir(parents=True, exist_ok=True)

    _logger = logging.getLogger(PROJECT_NAME)
    _logger.setLevel(logging.INFO)

    if not _logger.handlers:
        file_handler = TimedRotatingFileHandler(
            str(log_file), when=LOG_ROTATION_WHEN, interval=1, backupCount=LOG_BACKUP_COUNT, encoding="utf-8"
        )
        # ... 后续 formatter 设置 ...
        _logger.addHandler(file_handler)
        _logger.addHandler(logging.StreamHandler())

    return _logger


# 初始化全局单例 logger
logger = setup_logger()
