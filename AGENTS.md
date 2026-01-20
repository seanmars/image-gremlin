# AGENTS.md - Development Guide for AI Coding Agents

## Project Overview

**image-gremlin** 是一個 Python 3.12+ 專案，使用 `uv` 作為包管理和虛擬環境工具。

## Quick Start

```bash
# 安裝依賴
uv sync

# 執行主程式
uv run python main.py
```

## Build/Lint/Test Commands

### Package Management

```bash
# 安裝依賴
uv sync

# 添加新依賴
uv add <package-name>

# 添加開發依賴
uv add --dev <package-name>

# 移除依賴
uv remove <package-name>

# 更新依賴
uv sync --upgrade
```

### Running Code

```bash
# 執行主程式
uv run python main.py

# 執行任意 Python 腳本
uv run python path/to/script.py
```

### Testing (待設置)

```bash
# 執行所有測試
uv run pytest

# 執行單一測試文件
uv run pytest tests/test_filename.py

# 執行單一測試函數
uv run pytest tests/test_filename.py::test_function_name

# 執行測試並顯示詳細輸出
uv run pytest -v

# 執行測試並顯示覆蓋率
uv run pytest --cov=src --cov-report=term-missing
```

### Linting & Formatting (待設置)

```bash
# 使用 ruff 進行 linting
uv run ruff check .

# 自動修復可修復的問題
uv run ruff check --fix .

# 使用 ruff 進行格式化
uv run ruff format .

# 類型檢查 (如果使用 mypy)
uv run mypy src/
```

## Code Style Guidelines

### File Organization

```
image-gremlin/
├── src/                    # 源代碼目錄
│   └── image_gremlin/      # 主要套件
│       ├── __init__.py
│       └── ...
├── tests/                  # 測試目錄
│   └── test_*.py
├── main.py                 # 入口點
├── pyproject.toml          # 專案配置
└── README.md
```

### Import Style

按照以下順序組織 imports，每組之間空一行：

```python
# 1. 標準庫
import os
import sys
from pathlib import Path

# 2. 第三方套件
import numpy as np
import requests

# 3. 本地套件
from image_gremlin.core import ImageProcessor
from image_gremlin.utils import validate_input
```

**規則**：
- 使用絕對導入而非相對導入
- 每組內按字母順序排列
- 避免使用 `from module import *`

### Naming Conventions

```python
# 模組和套件：小寫字母，使用下劃線
# module_name.py, package_name/

# 類別：PascalCase
class ImageProcessor:
    pass

# 函數和變數：snake_case
def process_image(file_path: str) -> bytes:
    image_data = ...
    return image_data

# 常數：全大寫，使用下劃線
MAX_IMAGE_SIZE = 1024 * 1024
DEFAULT_FORMAT = "png"

# 私有成員：前綴單下劃線
class MyClass:
    def _internal_method(self):
        pass
    
    def __private_method(self):  # Name mangling
        pass
```

### Type Hints

**必須使用** type hints 提高代碼可讀性和維護性：

```python
from typing import Optional, List, Dict, Tuple, Union
from pathlib import Path

def process_images(
    paths: List[Path],
    output_dir: Path,
    quality: int = 85,
    options: Optional[Dict[str, any]] = None
) -> Tuple[int, List[str]]:
    """
    處理多個圖片文件。
    
    Args:
        paths: 圖片文件路徑列表
        output_dir: 輸出目錄
        quality: 圖片質量 (0-100)
        options: 可選配置參數
    
    Returns:
        成功處理的數量和錯誤訊息列表的 tuple
    """
    if options is None:
        options = {}
    
    # Implementation
    return 0, []
```

### Error Handling

```python
# 使用具體的異常類型
try:
    with open(file_path) as f:
        data = f.read()
except FileNotFoundError as e:
    logger.error(f"File not found: {file_path}")
    raise
except PermissionError as e:
    logger.error(f"Permission denied: {file_path}")
    raise
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise

# 創建自定義異常
class ImageProcessingError(Exception):
    """圖片處理相關錯誤的基礎異常類別"""
    pass

class InvalidImageFormat(ImageProcessingError):
    """不支援的圖片格式"""
    pass
```

### Logging

```python
import logging

# 配置 logger
logger = logging.getLogger(__name__)

# 使用適當的 log level
logger.debug("詳細的調試信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("錯誤信息")
logger.exception("例外信息 (自動包含 traceback)")
```

### Code Formatting

- **縮排**：4 個空格（不使用 tabs）
- **行長度**：最大 88 字符（Black 默認）
- **字串**：優先使用雙引號 `"`，除非字串內包含雙引號
- **Docstrings**：使用 Google style 或 NumPy style

```python
def example_function(param1: str, param2: int) -> bool:
    """
    函數的簡短描述。
    
    更詳細的說明可以寫在這裡。
    
    Args:
        param1: 第一個參數的描述
        param2: 第二個參數的描述
    
    Returns:
        返回值的描述
    
    Raises:
        ValueError: 何時拋出此異常
    """
    pass
```

## Development Philosophy (from CLAUDE.md)

### Core Principles

- **漸進式進展**：小步修改，確保每次修改都能編譯和通過測試
- **從現有代碼學習**：在實現新功能前，先研究和規劃
- **務實而非教條**：根據專案實際情況調整
- **清晰意圖勝過巧妙代碼**：選擇顯而易見的解決方案

### Important Reminders

**永遠不要**：
- 使用 `--no-verify` 繞過 commit hooks
- 禁用測試而非修復它們
- 提交無法編譯的代碼
- 做出假設 - 通過現有代碼驗證

**永遠要**：
- 隨時更新計劃文檔
- 從現有實現中學習
- 失敗 3 次後停下來重新評估
- 回應使用正體中文，台灣用語，並保留技術用詞為英文

## Git Workflow

```bash
# 檢查狀態
git status

# 添加修改
git add <files>

# 提交（遵循現有 commit message 風格）
git commit -m "feat: add image processing module"

# 查看最近的 commits 以了解風格
git log --oneline -10
```

### Commit Message Style

遵循 Conventional Commits：
- `feat:` - 新功能
- `fix:` - bug 修復
- `docs:` - 文檔更新
- `test:` - 添加或修改測試
- `refactor:` - 重構代碼
- `chore:` - 構建過程或輔助工具的變動

## Notes for AI Agents

- 這是一個新專案，某些工具配置可能尚未設置
- 在添加新的依賴時，使用 `uv add` 而非手動編輯 `pyproject.toml`
- Python 版本要求：>= 3.12
- 優先使用 Python 標準庫，避免不必要的依賴
- 所有新代碼必須包含 type hints
- 遵循 PEP 8 和 PEP 257 規範
