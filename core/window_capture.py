"""
StS2-Visionary 窗口捕获模块
负责通过模糊标题和进程名锁定窗口，并进行后台截图。
"""

import win32con
import win32gui
import win32process
import win32ui
import pywintypes
import psutil
from PIL import Image
from utils.logger_init import logger
from utils.config_loader import get_config

# pylint: disable=no-member


def find_window_fuzzy(title_keyword: str, process_name: str):
    """
    通过标题关键字和进程名双重过滤寻找窗口句柄。
    """
    target_hwnd = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            # 1. 检查标题是否包含关键字 (忽略大小写)
            if title_keyword.lower() in title.lower():
                try:
                    # 2. 检查该句柄所属的进程名
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    proc = psutil.Process(pid)
                    if proc.name().lower() == process_name.lower():
                        target_hwnd.append(hwnd)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        return True

    win32gui.EnumWindows(callback, None)
    return target_hwnd[0] if target_hwnd else None


def capture_window(title_keyword: str, process_name: str):
    """
    捕获指定条件的窗口并返回 PIL Image 对象。

    Args:
        title_keyword: 窗口标题包含的关键字。
        process_name: 进程名（如 Notepad--.exe）。
    """
    try:
        # 1. 寻找匹配的窗口句柄
        hwnd = find_window_fuzzy(title_keyword, process_name)

        if not hwnd:
            logger.warning("未找到匹配标题关键字 [%s] 且进程名为 [%s] 的窗口", title_keyword, process_name)
            return None

        # 2. 获取窗口尺寸
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        if width <= 0 or height <= 0:
            logger.error("窗口尺寸异常，窗口可能已被最小化")
            return None

        # 3. Win32 截图核心逻辑
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bit_map)

        # 执行拷贝
        result = save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        if result == 0:
            logger.error("BitBlt 拷贝操作失败")
            return None

        # 4. 转换为 PIL Image
        bmp_info = save_bit_map.GetInfo()
        bmp_str = save_bit_map.GetBitmapBits(True)
        img = Image.frombuffer(
            "RGB",
            (bmp_info["bmWidth"], bmp_info["bmHeight"]),
            bmp_str,
            "raw",
            "BGRX",
            0,
            1,
        )

        # 5. 资源释放
        win32gui.DeleteObject(save_bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        return img

    except pywintypes.error as e:
        logger.error("Win32 API 调用失败: %s", e)
        return None
    except Exception as e:
        # pylint: disable=broad-exception-caught
        logger.critical("窗口捕获发生未预期异常: %s", e, exc_info=True)
        return None


if __name__ == "__main__":
    # 使用对象化访问的配置
    CFG = get_config()

    # 从配置中提取两个参数
    t_title = CFG.target_app.window_title
    t_process = CFG.target_app.process_name

    logger.info("开始测试双重锁定捕获 | 标题关键字: %s | 进程名: %s", t_title, t_process)
    image = capture_window(t_title, t_process)

    if image:
        image.save("debug_capture.png")
        logger.info("截图成功，尺寸: %s", image.size)
    else:
        logger.error("截图失败")
