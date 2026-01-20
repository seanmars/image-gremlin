"""CLI 介面模組"""

import logging
from pathlib import Path

import click

from .color_utils import parse_rgba_hex, ColorParseError
from .models import ColorReplacer
from .models.base import ImageProcessingError

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="0.1.0", prog_name="image-gremlin")
def cli():
    """
    Image Gremlin - 圖片處理工具
    
    提供多種圖片處理功能，使用子命令來選擇不同的處理方式。
    """
    pass


@cli.command(name="replace-color")
@click.option(
    "-i", "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="輸入圖片路徑"
)
@click.option(
    "-o", "--output",
    "output_path",
    required=True,
    type=click.Path(path_type=Path),
    help="輸出圖片路徑"
)
@click.option(
    "-s", "--source-color",
    "source_color",
    required=True,
    help="要替換的來源顏色 (RGBA hex格式, 例如: FF0000FF 或 #FF0000)"
)
@click.option(
    "-t", "--target-color",
    "target_color",
    required=True,
    help="目標顏色 (RGBA hex格式, 例如: 00FF00FF 或 #00FF00)"
)
@click.option(
    "--tolerance",
    default=0,
    type=click.IntRange(0, 255),
    help="顏色容差值 (0-255)，用於匹配相似顏色。0表示精確匹配，數值越大匹配範圍越廣"
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="顯示詳細日誌"
)
def replace_color_command(
    input_path: Path,
    output_path: Path,
    source_color: str,
    target_color: str,
    tolerance: int,
    verbose: bool
) -> None:
    """
    替換圖片中指定的顏色。
    
    顏色格式支援:
      - #RRGGBBAA (8位數，包含alpha)
      - #RRGGBB (6位數，alpha默認為FF)
      - RRGGBBAA (無#前綴)
      - RRGGBB (無#前綴)
    
    範例:
      image-gremlin replace-color -i input.png -o output.png -s FF0000 -t 00FF00
      
      image-gremlin replace-color -i input.png -o output.png -s "#FF0000FF" -t "#00FF00FF" --tolerance 10
    """
    # 設定 verbose 模式
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    try:
        # 解析顏色
        logger.info(f"Parsing source color: {source_color}")
        source_rgba = parse_rgba_hex(source_color)
        logger.info(f"Source RGBA: {source_rgba}")
        
        logger.info(f"Parsing target color: {target_color}")
        target_rgba = parse_rgba_hex(target_color)
        logger.info(f"Target RGBA: {target_rgba}")
        
        # 建立處理器並執行
        logger.info(f"Processing image: {input_path}")
        logger.info(f"Output path: {output_path}")
        logger.info(f"Tolerance: {tolerance}")
        
        processor = ColorReplacer()
        processor.process(
            input_path=input_path,
            output_path=output_path,
            source_color=source_rgba,
            target_color=target_rgba,
            tolerance=tolerance
        )
        
        click.echo(click.style("✓ Success!", fg="green"))
        click.echo(f"Replaced color {source_color} with {target_color}")
        click.echo(f"Output saved to: {output_path}")
        
    except ColorParseError as e:
        logger.error(f"Color parsing error: {e}")
        click.echo(click.style(f"✗ Error: {e}", fg="red"), err=True)
        raise click.Abort()
    
    except ImageProcessingError as e:
        logger.error(f"Image processing error: {e}")
        click.echo(click.style(f"✗ Error: {e}", fg="red"), err=True)
        raise click.Abort()
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        click.echo(click.style(f"✗ Unexpected error: {e}", fg="red"), err=True)
        raise click.Abort()


# 為了向後相容，保留原本的 main 函數
def main():
    """CLI 入口點"""
    cli()


if __name__ == "__main__":
    main()
