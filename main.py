"""test kimi/silicon/qwen/hunyuan based on openai api"""

import envenv  # noqa
import base64
import os
import pathlib

import httpx

from pdf_reader.base import Chat
from pdf_reader.tracing import get_openai_client_cls

OpenAI = get_openai_client_cls()


class Kimi(Chat):
  def __init__(self):
    super().__init__()
    self.client = OpenAI(
      api_key=os.getenv("MOONSHOT_API_KEY"),
      base_url="https://api.moonshot.cn/v1",
    )
    self.support_file_id = False
    self.model = "moonshot-v1-auto"

  def estimate_token_count(self, input_messages) -> int:
    """
    在这里实现你的 Tokens 计算逻辑，或是直接调用我们的 Tokens 计算接口计算 Tokens

    https://api.moonshot.cn/v1/tokenizers/estimate-token-count
    """
    header = {
      "Authorization": f"Bearer {os.environ['MOONSHOT_API_KEY']}",
    }
    data = {
      "model": "moonshot-v1-128k",
      "messages": input_messages,
    }
    r = httpx.post("https://api.moonshot.cn/v1/tokenizers/estimate-token-count", headers=header, json=data)
    r.raise_for_status()
    return r.json()["data"]["total_tokens"]

  def open_image(self, image_path: pathlib.Path) -> str:
    """image_path 为 Kimi 识别的图片的地址"""
    with image_path.open("rb") as f:
      image_data = f.read()
    # 我们使用标准库 base64.b64encode 函数将图片编码成 base64 格式的 image_url
    image_url = f"data:image/{os.path.splitext(image_path)[1]};base64,{base64.b64encode(image_data).decode('utf-8')}"
    return image_url


class Hunyuan(Chat):
  def __init__(self):
    super().__init__()
    self.client = OpenAI(
      api_key=os.getenv("HUNYUAN_API_KEY"),
      base_url="https://api.hunyuan.cloud.tencent.com/v1",
    )
    self.support_file_id = False
    self.model = "hunyuan-TurboS"


class Qwen(Chat):
  def __init__(self):
    super().__init__()
    self.client = OpenAI(
      api_key=os.getenv("QIANWEN_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    self.support_file_id = True
    self.file_purpose = "file-extract"
    self.model = "qwen/qwen2.5-coder-32b-instruct"


class Silicon(Chat):
  def __init__(self):
    super().__init__()
    self.client = OpenAI(
      api_key=os.getenv("SILICON_API_KEY"),
      base_url="https://api.siliconflow.cn/v1",
    )
    self.support_file_id = True
    self.file_purpose = "batch"
    self.model = "Qwen/QVQ-72B-Preview"


class Zhipu(Chat):
  def __init__(self):
    super().__init__()
    self.client = OpenAI(
      api_key=os.getenv("ZHIPU_API_KEY"),
      base_url="https://open.bigmodel.cn/api/paas/v4",
    )
    self.support_file_id = True
    self.file_purpose = "file-extract"
    self.model = "glm-4v-plus-0111"


class OneAPI(Chat):
  def __init__(self):
    super().__init__()
    self.client = OpenAI(
      api_key=os.getenv("ONE_API_KEY"),
      base_url="http://192.168.2.41:3000/v1",
    )


def parse_args():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("--chat", type=str, default="kimi", help="chat model")
  parser.add_argument("--file", type=str, default="./resources/test.pdf", help="file path")
  parser.add_argument("--estimate", type=bool, default=False, help="estimate token count")
  parser.add_argument("--chat-id", type=str, default=None, help="get chat by id")
  return parser.parse_args()


if __name__ == "__main__":
  args = parse_args()

  chat_models = {
    "kimi": Kimi,
    "hunyuan": Hunyuan,
    "qwen": Qwen,
    "silicon": Silicon,
    "zhipu": Zhipu,
    "oneapi": OneAPI,
  }

  chat: Chat = chat_models[args.chat]()
  file_path = pathlib.Path(args.file)
  if args.estimate:
    chat.load_file(file_path)
    print(chat.estimate_token_count(chat.get_messages()))
  elif args.chat_id:
    print(chat.get_chat_by_id(args.chat_id))
  else:
    print(chat.ask(file_path))
