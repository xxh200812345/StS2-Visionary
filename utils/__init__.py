from .config_loader import get_config

# 预先实例化全局配置对象
# 这样 VS Code 扫描索引时能直接发现 utils.cfg
CFG = get_config()
