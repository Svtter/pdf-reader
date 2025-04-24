import os

import pytest
from loguru import logger
from openai import OpenAI

from pdf_reader.csvtool import CsvTool


@pytest.fixture
def client():
  return OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url="https://api.moonshot.cn/v1",
  )


def test_read_by_llms(client):
  csv_tool = CsvTool(client=client)
  with open("./resources/test.txt", "r") as f:
    text = f.read()
  csv_data = csv_tool.read_by_llms(text)
  assert csv_data, "csv_data is empty"


def test_extract_csv(client):
  csv_tool = CsvTool(client=client)
  with open("./resources/test.txt", "r") as f:
    text = f.read()
  csv_data = csv_tool.extract_csv(text)
  assert csv_data, "csv_data is empty"
