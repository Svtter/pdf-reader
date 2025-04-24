"""
将 chat 的 answer 中的 csv 数据单独读取出来

已知一段文字 text 中有多个 csv 原始文件和数据，通过大模型进行处理，
将该段文字中的 csv 数据单独读取出来，并保存为多个 csv 文件。

csv文件名在 text 中，大模型可以得到该文件名。
"""

import csv
import json
import os
import re
import traceback
import uuid

import jinja2
from loguru import logger
from openai import OpenAI

from .base import PromptReader
from .db import DB


class CsvTool(object):
  def __init__(self, client: OpenAI, output_dir="output"):
    self.client = client
    self.db = DB()
    self.output_dir = output_dir
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

  def read_by_llms(self, text: str):
    # 使用OpenAI模型提取CSV数据和文件名
    prompt = PromptReader.read_prompt("./resources/split-csv.txt")
    prompt = jinja2.Template(prompt).render(text=text)

    messages = [
      {"role": "system", "content": "你是一个专业的CSV数据提取助手，擅长从文本中识别和提取CSV格式的数据。"},
      {"role": "user", "content": prompt},
    ]
    response = self.client.chat.completions.create(
      model="moonshot-v1-auto",  # 或使用其他适合的模型
      messages=messages,
      max_tokens=10000,
      stop=None,
      response_format={"type": "json_object"},
    )

    # 解析模型返回的JSON
    result = json.loads(response.choices[0].message.content)
    self.db.save_chat({"question": messages, "answer": result})
    if result:
      return result
    else:
      return []

  def extract_csv(self, text: str):
    """extract csv data from text

    Args:
        text (str): 包含CSV数据的文本

    Returns:
        list: 保存的CSV文件路径列表
    """
    try:
      # 使用大模型提取CSV数据
      self.csv_data = self.read_by_llms(text)
      self.saved_files = []

      # 处理提取的每个CSV数据
      for i, csv_item in enumerate(self.csv_data):
        content = csv_item.get("content", "")
        if not content:
          continue

        # 获取文件名或生成一个
        filename = csv_item.get("filename")
        if not filename:
          filename = f"csv_{uuid.uuid4().hex[:8]}_{i}.csv"
        elif not filename.endswith(".csv"):
          filename += ".csv"

        filepath = os.path.join(self.output_dir, filename)
        logger.info(f"filepath: {filepath}")

        # 解析并保存CSV内容
        lines = content.strip().split("\n")
        rows = [line.split(",") for line in lines]

        with open(filepath, "w", newline="", encoding="utf-8") as f:
          writer = csv.writer(f)
          writer.writerows(rows)

        self.saved_files.append(filepath)

      # 如果大模型无法提取，使用正则表达式作为备选方案
      if not self.saved_files:
        return self._extract_csv_with_regex(text)

      return self.saved_files

    except Exception as e:
      logger.error(traceback.format_exc())
      logger.error(f"使用大模型提取CSV失败: {str(e)}")
      return self._extract_csv_with_regex(text)

  def _extract_csv_with_regex(self, text: str):
    """使用正则表达式提取CSV数据（备选方法）"""
    csv_pattern = r"(?:^|\n)([^,\n]+(?:,[^,\n]*)+(?:\n[^,\n]+(?:,[^,\n]*)+)+)"
    csv_matches = re.finditer(csv_pattern, text)

    saved_files = []

    for i, match in enumerate(csv_matches):
      csv_content = match.group(1)

      # 生成唯一文件名
      filename = f"csv_{uuid.uuid4().hex[:8]}_{i}.csv"
      filepath = os.path.join(self.output_dir, filename)

      # 解析CSV数据
      lines = csv_content.strip().split("\n")
      rows = [line.split(",") for line in lines]

      # 保存为CSV文件
      with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

      saved_files.append(filepath)

    return saved_files

  def save_csv(self, data, filename=None):
    """将数据保存为CSV文件

    Args:
        data (list): 二维列表数据
        filename (str, optional): 文件名，不提供则自动生成

    Returns:
        str: 保存的文件路径
    """
    if filename is None:
      filename = f"csv_{uuid.uuid4().hex[:8]}.csv"

    filepath = os.path.join(self.output_dir, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerows(data)

    return filepath
