# 📑 [开发规范] StS2-Visionary 代码管理与自动化配置

本文档定义了 **StS2-Visionary** 项目的编码标准、静态检查规则及 VS Code 自动化环境配置，旨在确保项目代码的健壮性与一致性。

---

## 1. 自动格式化配置 (VS Code)

为了消除 `Trailing whitespace` 和 `Missing final newline` 等低级规范错误，项目强制使用 **Black Formatter**。

### 1.1 配置文件 `.vscode/settings.json`
在根目录下创建此文件，内容如下：StS2-Visionary/
├── main.py                # 启动程序
├── config.yaml            # 配置文件
├── core/                  # 核心逻辑
├── ui/                    # 界面逻辑
├── utils/                 # 工具类（新增：日志管理逻辑放在这里）
│   └── logger_init.py     # 日志初始化脚本
├── docs/                  # 技术文档库
├── logs/                  # 日志存储目录（自动生成：保留最近5天）
├── anchors/               # 场景判断用的模板图片
├── data/                  # 提示语 CSV 文件
└── resources/             # 静态资源


```json
{
    "python.defaultInterpreterPath": "./sts2-venv/Scripts/python.exe",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "pylint.args": [
        "--max-line-length=120",
        "--disable=C0114,C0116,R0903"
    ]
}
```

---

## 2. 核心编码规约

### 2.1 命名约定
* **模块/包名**: 小写下划线，如 `core/window_handler.py`。
* **类名**: 大驼峰，如 `SceneDetector`。
* **函数/变量**: 小写下划线，如 `get_screen_shot()`。
* **常量**: 全大写，如 `SCAN_INTERVAL = 0.5`。
* **私有变量**: 内部函数使用 `_` 前缀，如 `_logger`，以避免 `redefined-outer-name` 警告。

### 2.2 日志记录规范
严禁使用 `print()` 调试。所有运行时信息必须通过 `utils.logger_init` 模块输出：
* `logger.debug()`: 详细的中间过程（如特征点匹配数量）。
* `logger.info()`: 关键状态切换（如“检测到商店场景”）。
* `logger.error()`: 捕获的异常，需带上 `exc_info=True` 以记录堆栈。

---

## 3. 静态检查过滤 (Linting Exceptions)

为了平衡开发效率，我们在 Pylint 中屏蔽了以下非核心警告：
* **C0114/C0116**: 缺少模块/函数文档字符串（在内部私有逻辑中可选）。
* **R0903**: 类的公开方法太少（由于模块化设计，部分类仅作为单功能入口）。

---

## 4. 依赖同步流程

每当引入新的库时，请务必执行以下流程以保持环境一致：

1. **安装新包**: `pip install <package_name>`
2. **测试运行**: 确保主程序不报错。
3. **更新快照**: `pip freeze > requirements.txt`
4. **提交文档**: 记录新增包的用途。

---

## 5. 项目结构与导入路径

项目根目录已加入 `PYTHONPATH`。所有导入应使用绝对路径：
```python
# 正确做法
from core.detector import SceneDetector
from utils.logger_init import logger

# 错误做法（相对路径在打包 EXE 时容易出错）
from ..utils.logger_init import logger
```

---

### 💡 接下来：正式进入核心功能开发

现在你的文档库（`docs/`）已经拥有：
1. `README.md` (主页)
2. `DESIGN_VISION.md` (视觉方案)
3. `DEVELOPMENT_STANDARDS.md` (代码管理 - **当前更新**)
