"""merge multiple csv data into one excel file"""

import os
import traceback

import pandas as pd
from loguru import logger


def merge_csv_to_excel(
  csv_files: list[str],
  output_file_path: str,
  sheet_name_list: list[str] = None,
):
  """merge multiple csv data into one excel file, in different sheets"""
  # 创建 ExcelWriter 对象
  try:
    with pd.ExcelWriter(output_file_path, engine="openpyxl") as writer:
      # 遍历所有 csv 文件
      for file in csv_files:
        # 读取 csv 文件，添加参数以处理不一致的数据格式
        try:
          # 首先尝试正常读取
          df = pd.read_csv(file)
        except pd.errors.ParserError:
          # 如果解析错误，使用更宽松的参数重试
          logger.warning(f"CSV格式不一致，使用宽松模式读取: {file}")
          df = pd.read_csv(file, on_bad_lines="skip", sep=None, engine="python")

        # 获取文件名（不带路径和扩展名）作为 sheet 名
        sheet_name = os.path.splitext(os.path.basename(file))[0]
        # 将数据写入对应的 sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)
  except Exception as e:
    logger.error(traceback.format_exc())
    logger.error(f"merge csv to excel failed: {e}")
    return False
  return True
