"""
StS2-Visionary 游戏实体定义模块
包含所有游戏对象（卡牌、遗物等）的基础数据结构。
"""

from dataclasses import dataclass, field
from enum import Enum


class DataType(Enum):
    """
    游戏数据类型枚举。
    用于区分识别到的对象属于卡牌、遗物还是事件。
    """

    CARD = "card"
    RELIC = "relic"
    EVENT = "event"
    POTION = "potion"
    UNKNOWN = "unknown"


@dataclass
class GameEntity:
    """
    所有游戏实体的基类。
    封装了从 CSV 加载的基础属性及原始数据。
    """

    name: str
    entity_type: DataType
    description: str = ""
    raw_data: dict = field(default_factory=dict)

    # 预留常用字段
    rarity: str = "普通"
    cost: str = "0"
