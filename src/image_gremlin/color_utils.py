"""顏色處理工具模組"""

from typing import Tuple


class ColorParseError(Exception):
    """顏色解析錯誤"""
    pass


def parse_rgba_hex(hex_color: str) -> Tuple[int, int, int, int]:
    """
    解析 RGBA hex 顏色字串。
    
    支援格式:
    - #RRGGBBAA (8位數)
    - RRGGBBAA (8位數，無#)
    - #RRGGBB (6位數，alpha默認為255)
    - RRGGBB (6位數，無#，alpha默認為255)
    
    Args:
        hex_color: hex 顏色字串
    
    Returns:
        包含 (R, G, B, A) 的 tuple，每個值範圍 0-255
    
    Raises:
        ColorParseError: 顏色格式錯誤時拋出
    
    Examples:
        >>> parse_rgba_hex("#FF0000FF")
        (255, 0, 0, 255)
        >>> parse_rgba_hex("00FF00")
        (0, 255, 0, 255)
    """
    # 移除 # 符號
    hex_color = hex_color.lstrip("#")
    
    # 檢查長度
    if len(hex_color) not in (6, 8):
        raise ColorParseError(
            f"Invalid hex color format: {hex_color}. "
            f"Expected 6 or 8 characters, got {len(hex_color)}"
        )
    
    # 檢查是否為有效的 hex 字符
    try:
        int(hex_color, 16)
    except ValueError:
        raise ColorParseError(
            f"Invalid hex color format: {hex_color}. "
            f"Contains non-hexadecimal characters"
        )
    
    # 解析 RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # 解析 Alpha (如果有的話，否則默認為 255)
    a = int(hex_color[6:8], 16) if len(hex_color) == 8 else 255
    
    return (r, g, b, a)


def rgba_to_hex(r: int, g: int, b: int, a: int = 255) -> str:
    """
    將 RGBA 值轉換為 hex 字串。
    
    Args:
        r: Red 值 (0-255)
        g: Green 值 (0-255)
        b: Blue 值 (0-255)
        a: Alpha 值 (0-255)，默認為 255
    
    Returns:
        Hex 顏色字串，格式為 #RRGGBBAA
    
    Examples:
        >>> rgba_to_hex(255, 0, 0, 255)
        '#FF0000FF'
    """
    return f"#{r:02X}{g:02X}{b:02X}{a:02X}"


def color_distance(color1: Tuple[int, int, int, int], 
                   color2: Tuple[int, int, int, int]) -> float:
    """
    計算兩個 RGBA 顏色之間的歐幾里得距離。
    
    Args:
        color1: 第一個顏色 (R, G, B, A)
        color2: 第二個顏色 (R, G, B, A)
    
    Returns:
        顏色距離（越小表示越相似）
    """
    r1, g1, b1, a1 = color1
    r2, g2, b2, a2 = color2
    
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + 
            (b1 - b2) ** 2 + (a1 - a2) ** 2) ** 0.5
