import os

from langfuse.openai import OpenAI
from loguru import logger


def test_langfuse():
  client = OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url="https://api.moonshot.cn/v1",
  )
  assert client is not None
  response = client.chat.completions.create(
    model="moonshot-v1-auto",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, world!"},
    ],
  )
  logger.info(response.choices[0].message.content)
  assert response.choices[0].message.content is not None
