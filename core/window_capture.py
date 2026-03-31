"""
StS2-Visionary 窗口捕获模块
负责通过模糊标题和进程名锁定窗口，并进行后台截图。
"""

import ctypes
import time
import win32con
import win32gui
import win32process
import win32ui
import psutil
from PIL import Image
from utils.logger_init import logger
from utils import CFG


# 解决高分屏截图错位或尺寸不对的问题
ctypes.windll.user32.SetProcessDPIAware()

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
    try:
        hwnd = find_window_fuzzy(title_keyword, process_name)
        if not hwnd:
            logger.warning("未找到匹配窗口: [%s]", title_keyword)
            return None

        # 如果窗口被最小化，尝试恢复它（可选，如果不希望干扰用户可去掉）
        if win32gui.IsIconic(hwnd):
            logger.info("窗口处于最小化状态，尝试恢复...")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.1)  # 等待窗口重绘

        # 获取窗口精确坐标
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        # 核心修正：改用 PrintWindow 方式
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bit_map)

        # 修正点：使用 PrintWindow
        # 参数 2 表示捕获整个窗口（包括非客户区）
        # 如果依然空白，尝试将 2 改为 0 或 3
        result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

        if not result:
            logger.error("PrintWindow 捕获失败，尝试 BitBlt 兜底...")
            save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

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

        # 资源清理
        win32gui.DeleteObject(save_bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        return img

    except Exception as e:
        logger.error("截图失败: %s", e)
        return None


if __name__ == "__main__":

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
