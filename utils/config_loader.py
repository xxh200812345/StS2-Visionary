"""
StS2-Visionary 配置加载模块
提供全局统一的对象化配置访问入口。
"""

from pathlib import Path
from types import SimpleNamespace
import yaml
from utils.logger_init import logger


class ConfigManager:
    """配置管理类，实现单例加载并转换为对象格式"""

    _config = None
    ROOT_DIR = Path(__file__).resolve().parent.parent
    CONFIG_PATH = ROOT_DIR / "config.yaml"

    @staticmethod
    def _dict_to_obj(data):
        """递归将字典转换为 SimpleNamespace 对象"""
        if isinstance(data, dict):
            # 将字典内部所有的值也进行递归转换
            return SimpleNamespace(**{k: ConfigManager._dict_to_obj(v) for k, v in data.items()})
        if isinstance(data, list):
            # 如果是列表，对其内部元素进行处理
            return [ConfigManager._dict_to_obj(i) for i in data]
        return data

    @classmethod
    def get_config(cls):
        """获取全局配置单例"""
        if cls._config is None:
            cls.load_config()
        return cls._config

    @classmethod
    def load_config(cls):
        """执行 YAML 加载并格式化为对象"""
        try:
            if not cls.CONFIG_PATH.exists():
                logger.error("配置文件未找到: %s，使用内置默认值", cls.CONFIG_PATH)
                raw_config = {
                    "target_app": {"window_title": "Slay the Spire 2", "process_name": "StS2.exe"},
                    "ocr_settings": {"lang": "ch"},
                }
            else:
                with open(cls.CONFIG_PATH, "r", encoding="utf-8") as f:
                    raw_config = yaml.safe_load(f) or {}
                    logger.info("成功加载全局配置: %s", cls.CONFIG_PATH)

            # 关键步骤：将原生字典转换为支持 . 访问的对象
            cls._config = cls._dict_to_obj(raw_config)

        except Exception as e:
            logger.error("解析配置文件失败: %s", e)
            raise


# 导出函数，注意现在的返回类型不再是 dict，而是 SimpleNamespace (Any)
def get_config():
    """获取配置对象，支持点语法访问，如 cfg.target_app.window_title"""
    return ConfigManager.get_config()
