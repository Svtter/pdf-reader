import os

from openai import OpenAI


class Kimi(object):
  def __init__(self):
    self.client = OpenAI(
      api_key=os.getenv("MOONSHOT_API_KEY"),
      base_url="https://api.moonshot.cn/v1",
    )


def get_client(name="kimi"):
  kimi = Kimi()
  if name == "kimi":
    return kimi.client
  else:
    raise ValueError(f"Unsupported LLM: {name}")
