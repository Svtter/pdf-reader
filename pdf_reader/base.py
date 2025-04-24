import pathlib

from .db import DB
from .tracing import tracable


class PromptReader:
  """read prompt from file"""

  @classmethod
  def read_prompt(cls, path) -> str:
    with open(path, "r") as f:
      return f.read()

  @classmethod
  def read_system_prompt(cls) -> str:
    """read system prompt"""
    return cls.read_prompt(path="./resources/prompt-init.txt")

  @classmethod
  def read_table_format(cls) -> str:
    """read table format"""
    return cls.read_prompt(path="./resources/table-format.txt")

  @classmethod
  def read_question(cls) -> str:
    """read user question"""
    return cls.read_prompt(path="./resources/question.txt")


class Chat(object):
  def __init__(self):
    self.db = DB()
    self.file = None
    self.file_purpose = "file-extract"
    self.messages = []

  def get_latest_chat(self):
    """get latest chat"""
    return self.db.get_latest_chat()

  def get_chat_by_id(self, chat_id: str):
    """get chat by id"""
    return self.db.get_chat_by_id(chat_id)

  def load_file(self, file_path: pathlib.Path) -> dict:
    """file_path 为 LLM 识别的文件的地址"""
    file_object = self.client.files.create(
      file=file_path,
      purpose=self.file_purpose,
    )

    # moonshot.pdf 是一个示例文件, 我们支持文本文件和图片文件，对于图片文件，我们提供了 OCR 的能力
    # 上传文件时，我们可以直接使用 openai 库的文件上传 API，使用标准库 pathlib 中的 Path 构造文件
    # 对象，并将其传入 file 参数即可，同时将 purpose 参数设置为 file-extract；注意，目前文件上传
    # 接口仅支持 file-extract 一种 purpose 值。
    self.file = {
      "file_id": file_object.id,
      "file_object": file_object,
    }

    # 获取结果
    # file_content = client.files.retrieve_content(file_id=file_object.id)
    # 注意，某些旧版本示例中的 retrieve_content API 在最新版本标记了 warning, 可以用下面这行代替
    # （如果使用旧版本的 SDK，可以继续延用 retrieve_content API）
    file_content = self.client.files.content(file_object.id).text
    self.file["file_content"] = file_content
    return self.file

  def add_file(self):
    if self.support_file_id:
      return self.file["file_id"]
    else:
      return self.file["file_content"]

  def get_messages(self, user_input: str):
    self.messages = [
      {"role": "system", "content": PromptReader.read_system_prompt()},
      {"role": "system", "content": self.add_file()},
      {"role": "system", "content": PromptReader.read_table_format()},
      {"role": "user", "content": user_input},
    ]
    return self.messages

  @tracable
  def make_request(self, user_input: str):
    response = self.client.chat.completions.create(
      model=self.model,
      messages=self.get_messages(user_input),
      temperature=0.3,
      max_tokens=4000,
      stop=None,
    )
    answer = response.choices[0].message.content
    return answer

  def ask(self, file_path: pathlib.Path) -> str:
    """ask kimi"""
    self.file = self.load_file(file_path)

    # 调用 LLM 生成回答
    answer = self.make_request(user_input=PromptReader.read_question())

    # 保存聊天记录
    self.db.save_chat({"question": self.messages, "answer": answer})
    return answer
