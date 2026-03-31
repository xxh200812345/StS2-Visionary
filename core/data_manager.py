"""
StS2-Visionary 数据管理模块
负责从 CSV/JSON 加载游戏数据，并提供模糊搜索功能。
"""

import pandas as pd
from fuzzywuzzy import process
from utils import CFG
from utils.logger_init import logger
from models.game_entity import GameEntity, DataType


class DataManager:
    """全能知识库：负责数据加载与检索"""

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return

        # 模拟数据存储（实际应用中这里应该是从 CSV 加载）
        self.entities = []
        self._load_data()
        self.initialized = True
        logger.info("DataManager 初始化完成，已加载 %d 条实体数据。", len(self.entities))

    def _load_data(self):
        """从本地文件加载数据（此处为示例逻辑）"""
        # 实际开发时，你会在这里用 pandas 读取 CSV
        # 示例：self.entities.append(GameEntity(name="打击", entity_type=DataType.CARD))
        pass

    def global_search(self, text, threshold=80):
        """
        在所有实体中进行模糊匹配
        返回格式: [(score, GameEntity), ...]
        """
        if not text:
            return []

        # 这里的逻辑根据你的匹配算法实现
        # 示例：使用 fuzzywuzzy 进行名称匹配
        choices = {e.name: e for e in self.entities}
        results = process.extract(text, choices.keys(), limit=3)

        matches = []
        for name, score in results:
            if score >= threshold:
                matches.append((score, choices[name]))

        return sorted(matches, key=lambda x: x[0], reverse=True)
