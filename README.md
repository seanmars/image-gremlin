# Image Gremlin

一個強大且易於擴充的 Python 圖片處理工具，提供命令列介面進行各種圖片操作。

## 功能特色

- **顏色替換** - 將圖片中指定的顏色替換為另一個顏色
- **RGBA 支援** - 完整支援透明度處理
- **容差匹配** - 可設定容差值來匹配相似顏色
- **模組化設計** - 易於擴充新功能
- **友善的 CLI** - 清晰的命令列介面和錯誤提示

## 系統需求

- Python >= 3.12
- uv (套件管理工具)

## 安裝

```bash
# Clone 專案
git clone <repository-url>
cd image-gremlin

# 安裝依賴
uv sync
```

## 使用方式

### 查看可用命令

```bash
uv run python main.py --help
```

### 顏色替換 (replace-color)

將圖片中指定的顏色替換為另一個顏色。

#### 基本用法

```bash
# 將紅色替換為綠色
uv run python main.py replace-color -i input.png -o output.png -s FF0000 -t 00FF00

# 使用 # 前綴和完整 RGBA
uv run python main.py replace-color -i input.png -o output.png -s "#FF0000FF" -t "#00FF00FF"

# 將綠色替換為透明（Alpha=0）
uv run python main.py replace-color -i icon.png -o output.png -s 00ff00 -t 00000000
```

#### 使用容差匹配相似顏色

```bash
# 容差值 10，會匹配接近紅色的顏色
uv run python main.py replace-color -i input.png -o output.png -s FF0000 -t 00FF00 --tolerance 10
```

#### Verbose 模式

```bash
# 顯示詳細處理資訊
uv run python main.py replace-color -i input.png -o output.png -s FF0000 -t 00FF00 -v
```

### 顏色格式說明

支援以下 RGBA hex 格式：
- `#RRGGBBAA` - 8位數，包含 alpha 通道
- `#RRGGBB` - 6位數，alpha 默認為 FF (不透明)
- `RRGGBBAA` - 無 # 前綴
- `RRGGBB` - 無 # 前綴

範例：
- `FF0000` 或 `#FF0000` - 紅色 (不透明)
- `FF0000FF` 或 `#FF0000FF` - 紅色 (不透明)
- `00000000` - 完全透明
- `FF000080` - 半透明紅色

## 專案架構

```
image-gremlin/
├── src/
│   └── image_gremlin/
│       ├── models/              # 圖片處理器 Models
│       │   ├── __init__.py
│       │   ├── base.py          # ImageProcessor 抽象基礎類別
│       │   └── color_replacer.py # 顏色替換處理器
│       ├── __init__.py
│       ├── cli.py               # CLI 介面
│       └── color_utils.py       # 顏色處理工具
├── main.py                      # 程式入口點
├── pyproject.toml               # 專案配置
└── README.md
```

## 擴充新功能

專案採用模組化設計，可輕鬆新增功能：

### 1. 建立新的 Model

在 `src/image_gremlin/models/` 建立新檔案，繼承 `ImageProcessor`：

```python
# src/image_gremlin/models/my_feature.py
from pathlib import Path
from .base import ImageProcessor

class MyFeature(ImageProcessor):
    def get_name(self) -> str:
        return "my-feature"
    
    def get_description(self) -> str:
        return "Description of my feature"
    
    def process(self, input_path: Path, output_path: Path, **kwargs) -> None:
        # 載入圖片
        image = self._load_image(input_path)
        
        # 處理邏輯
        # ...
        
        # 儲存圖片
        self._save_image(image, output_path)
```

### 2. 在 CLI 新增子命令

在 `src/image_gremlin/cli.py` 新增命令：

```python
from .models import MyFeature

@cli.command(name="my-feature")
@click.option("-i", "--input", ...)
@click.option("-o", "--output", ...)
def my_feature_command(input_path, output_path):
    processor = MyFeature()
    processor.process(input_path=input_path, output_path=output_path)
```

### 3. 匯出新 Model

在 `src/image_gremlin/models/__init__.py` 新增：

```python
from .my_feature import MyFeature
__all__ = [..., "MyFeature"]
```

## 開發指南

詳細的開發指南請參考 [AGENTS.md](AGENTS.md)。

### 執行測試

```bash
# 執行所有測試（待設置）
uv run pytest

# 執行特定測試
uv run pytest tests/test_color_utils.py
```

### Code Style

專案遵循：
- PEP 8 編碼規範
- Type hints 必須使用
- Google/NumPy style docstrings

## 依賴套件

- [Pillow](https://python-pillow.org/) - 圖片處理
- [Click](https://click.palletsprojects.com/) - CLI 框架

## License

MIT

## 貢獻

歡迎提交 Issue 和 Pull Request！
