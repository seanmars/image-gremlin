"""圖片處理器基礎類別"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from PIL import Image

logger = logging.getLogger(__name__)


class ImageProcessingError(Exception):
    """圖片處理相關錯誤的基礎異常類別"""
    pass


class InvalidImageFormat(ImageProcessingError):
    """不支援的圖片格式"""
    pass


class ImageProcessor(ABC):
    """
    圖片處理器抽象基礎類別。
    
    所有圖片處理功能都應該繼承此類別並實作 process 方法。
    """
    
    def __init__(self) -> None:
        """初始化處理器"""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def process(
        self, 
        input_path: Path, 
        output_path: Path, 
        **kwargs: Any
    ) -> None:
        """
        處理圖片的主要方法。
        
        Args:
            input_path: 輸入圖片路徑
            output_path: 輸出圖片路徑
            **kwargs: 其他處理參數
        
        Raises:
            ImageProcessingError: 處理過程中發生錯誤
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        取得處理器名稱（用於 CLI 命令）。
        
        Returns:
            處理器名稱
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        取得處理器描述。
        
        Returns:
            處理器描述
        """
        pass
    
    def _load_image(self, path: Path) -> Image.Image:
        """
        載入圖片檔案。
        
        Args:
            path: 圖片路徑
        
        Returns:
            PIL Image 物件
        
        Raises:
            FileNotFoundError: 檔案不存在
            InvalidImageFormat: 無法開啟圖片
        """
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        
        try:
            return Image.open(path)
        except Exception as e:
            raise InvalidImageFormat(f"Failed to open image: {e}")
    
    def _save_image(self, image: Image.Image, path: Path) -> None:
        """
        儲存圖片檔案。
        
        Args:
            image: PIL Image 物件
            path: 輸出路徑
        
        Raises:
            ImageProcessingError: 無法儲存圖片
        """
        # 確保輸出目錄存在
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            image.save(path)
            self.logger.info(f"Image saved to: {path}")
        except Exception as e:
            raise ImageProcessingError(f"Failed to save image: {e}")
