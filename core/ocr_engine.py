"""
StS2-Visionary OCR 识别引擎
整合 PaddleOCR 与 DataManager，实现从图片到游戏实体的转化。
"""

import numpy as np
from paddleocr import PaddleOCR
from utils import CFG, logger

# 核心改动：从新的 database 包导入
from database.data_manager import DataManager


class OCREngine:
    """OCR 识别与数据匹配引擎"""

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(OCREngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "ocr"):
            return

        try:
            # 读取配置
            lang = getattr(CFG.ocr_settings, "lang", "ch")
            use_gpu = getattr(CFG.ocr_settings, "use_gpu", False)
            limit_side = getattr(CFG.ocr_settings, "det_limit_side_len", 960)

            logger.info("正在初始化 PaddleOCR (Lang: %s, GPU: %s)...", lang, use_gpu)

            # 初始化模型
            self.ocr = PaddleOCR(
                use_angle_cls=True, lang=lang, use_gpu=use_gpu, det_limit_side_len=limit_side, show_log=False
            )

            # 实例化数据管理器（现在不再有循环引用风险）
            self.data_manager = DataManager()

        except Exception as e:
            logger.critical("OCR 引擎初始化失败: %s", e, exc_info=True)
            raise

    def identify_entities(self, pil_image):
        """
        核心业务流：
        1. 图像转数组 -> 2. OCR 识别 -> 3. 结果过滤 -> 4. 知识库匹配
        """
        if pil_image is None:
            return []

        img_array = np.array(pil_image.convert("RGB"))
        ocr_results = self.ocr.ocr(img_array, cls=True)

        final_outputs = []
        if not ocr_results or not ocr_results[0]:
            return []

        conf_limit = getattr(CFG.ocr_settings, "confidence_threshold", 0.6)

        for res in ocr_results[0]:
            text = res[1][0]
            confidence = res[1][1]

            if confidence < conf_limit:
                continue

            # 调用外部 DataManager 进行匹配
            matches = self.data_manager.global_search(text)

            if matches:
                score, entity = matches[0]
                final_outputs.append({"entity": entity, "score": score, "ocr_text": text, "box": res[0]})

        return final_outputs


if __name__ == "__main__":
    from core.window_capture import capture_window

    engine = OCREngine()
    img = capture_window(CFG.target_app.window_title, CFG.target_app.process_name)

    if img:
        results = engine.identify_entities(img)
        logger.info("=== 识别报告 ===")
        for item in results:
            ent = item["entity"]
            logger.info("发现 [%s]: %s | 匹配得分: %.2f", ent.entity_type.value.upper(), ent.name, item["score"])
