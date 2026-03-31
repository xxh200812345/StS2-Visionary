"""
StS2-Visionary 测试资源生成器
修正了 resource_dir 字符串类型无法直接调用 mkdir 的问题。
"""

import csv
from pathlib import Path
from utils import CFG
from utils.logger_init import logger


def generate_test_resources():
    """
    根据 CFG 配置自动生成测试用 CSV 文件。
    确保 resource_dir 转换为 Path 对象后再操作。
    """
    # 1. 获取配置中的目录字符串并转换为 Path 对象
    # 假设 CFG.paths.database_csv_dir 的值是 "./resources/data"
    raw_dir = CFG.paths.database_csv_dir

    # 核心修正：强制转换为 Path 对象，这样才能用 .mkdir() 和 / 运算符
    resource_dir = Path(raw_dir) if isinstance(raw_dir, str) else raw_dir

    # 执行目录创建
    resource_dir.mkdir(parents=True, exist_ok=True)

    # 2. 定义测试数据内容
    test_data = {
        "cards.csv": [
            ["name", "type", "cost", "rarity", "desc"],
            ["打击", "攻击", "1", "初始", "造成6点伤害。"],
            ["防御", "技能", "1", "初始", "获得5点护甲。"],
            ["闪电击", "攻击", "1", "普通", "造成8点伤害。生成1个闪电球。"],
        ],
        "relics.csv": [
            ["name", "rarity", "desc"],
            ["开信刀", "罕见", "打出3张技能牌造成5点AOE伤害。"],
            ["手里剑", "罕见", "打出3张攻击牌获得1点力量。"],
        ],
        "events.csv": [
            ["name", "type", "desc"],
            ["活体墙", "事件", "你在高塔中遇到了一面长满脸的墙..."],
            ["黄金神像", "事件", "拿走它会获得诅咒。"],
        ],
    }

    # 3. 写入文件
    logger.info("开始生成测试资源至: %s", resource_dir.absolute())

    for filename, rows in test_data.items():
        # 现在 resource_dir 是 Path 对象，可以直接使用 / 拼接
        file_path = resource_dir / filename
        try:
            with open(file_path, mode="w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            logger.info("-> [成功] 创建文件: %s", filename)
        except Exception as e:
            logger.error("-> [失败] 写入 %s 时发生错误: %s", filename, e)


if __name__ == "__main__":
    generate_test_resources()
