"""
StS2-Visionary 静态常量
定义文件系统路径、日志保留规则等底层基础设施参数。
"""

from pathlib import Path

PROJECT_NAME = "sts2_visionary"

# 项目根目录自动推导
ROOT_DIR = Path(__file__).resolve().parent.parent

# 配置文件名
CONFIG_FILENAME = "config.yaml"
CONFIG_PATH = ROOT_DIR / CONFIG_FILENAME

# 日志基础设施定义
LOG_DIR_NAME = "logs"
LOG_FILE_NAME = "app_info.log"
LOG_BACKUP_COUNT = 5  # 保留 5 天
LOG_ROTATION_WHEN = "D"  # 按天轮转
