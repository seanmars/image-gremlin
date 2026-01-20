"""顏色替換處理器"""

from pathlib import Path
from typing import Tuple

from PIL import Image

from .base import ImageProcessor
from ..color_utils import color_distance


class ColorReplacer(ImageProcessor):
    """
    顏色替換處理器。
    
    將圖片中指定的顏色替換為另一個顏色。
    """
    
    def get_name(self) -> str:
        """取得處理器名稱"""
        return "replace-color"
    
    def get_description(self) -> str:
        """取得處理器描述"""
        return "Replace a specific color in the image with another color"
    
    def process(
        self,
        input_path: Path,
        output_path: Path,
        **kwargs
    ) -> None:
        """
        替換圖片中指定的顏色。
        
        Args:
            input_path: 輸入圖片路徑
            output_path: 輸出圖片路徑
            **kwargs: 
                - source_color: Tuple[int, int, int, int] - 要替換的來源顏色 (R, G, B, A)
                - target_color: Tuple[int, int, int, int] - 目標顏色 (R, G, B, A)
                - tolerance: int - 顏色容差值 (預設: 0)
        
        Raises:
            ValueError: 缺少必要參數
            ImageProcessingError: 處理過程中發生錯誤
        """
        # 驗證必要參數
        if "source_color" not in kwargs:
            raise ValueError("Missing required parameter: source_color")
        if "target_color" not in kwargs:
            raise ValueError("Missing required parameter: target_color")
        
        source_color: Tuple[int, int, int, int] = kwargs["source_color"]
        target_color: Tuple[int, int, int, int] = kwargs["target_color"]
        tolerance: int = kwargs.get("tolerance", 0)
        
        # 載入圖片
        image = self._load_image(input_path)
        
        # 轉換為 RGBA 模式（確保支援透明度）
        if image.mode != "RGBA":
            self.logger.info(f"Converting image from {image.mode} to RGBA")
            image = image.convert("RGBA")
        
        # 替換顏色
        replaced_count = self._replace_color(
            image, source_color, target_color, tolerance
        )
        
        self.logger.info(f"Replaced {replaced_count} pixels")
        
        # 儲存圖片
        self._save_image(image, output_path)
    
    def _replace_color(
        self,
        image: Image.Image,
        source_color: Tuple[int, int, int, int],
        target_color: Tuple[int, int, int, int],
        tolerance: int
    ) -> int:
        """
        替換圖片中的顏色。
        
        Args:
            image: PIL Image 物件
            source_color: 來源顏色
            target_color: 目標顏色
            tolerance: 容差值
        
        Returns:
            替換的像素數量
        """
        pixels = image.load()
        width, height = image.size
        replaced_count = 0
        
        if pixels is None:
                return replaced_count
        
        for y in range(height):
            for x in range(width):
                current_pixel = pixels[x, y]
                
                if self._is_color_match(current_pixel, source_color, tolerance):
                    pixels[x, y] = target_color
                    replaced_count += 1
        
        return replaced_count
    
    def _is_color_match(
        self,
        color1: Tuple[int, int, int, int],
        color2: Tuple[int, int, int, int],
        tolerance: int
    ) -> bool:
        """
        檢查兩個顏色是否匹配（考慮容差值）。
        
        Args:
            color1: 第一個顏色
            color2: 第二個顏色
            tolerance: 容差值
        
        Returns:
            如果顏色匹配則為 True
        """
        if tolerance == 0:
            # 精確匹配
            return color1 == color2
        else:
            # 使用歐幾里得距離計算相似度
            distance = color_distance(color1, color2)
            return distance <= tolerance
