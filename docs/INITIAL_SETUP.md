### 标题：[开发规范] 环境搭建与依赖管理

**1. 虚拟环境**
```bash
python -m venv sts2-venv
source venv/bin/scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. 配置文件结构 (`config.yaml`)**
```yaml
app_settings:
  target_name: "Slay the Spire 2"  # 目标窗口标题关键字
  update_interval: 0.5            # 检测频率 (秒)
  
paths:
  anchors: "./anchors"
  database: "./data/main_db.csv"
  
ocr_engine:
  use_gpu: false
  lang: "ch"
  det_db_thresh: 0.3              # 目标检测灵敏度
```

