import os

from loguru import logger
from openai import OpenAI

client = OpenAI(
  api_key=os.getenv("ONE_API_KEY"),
  base_url="http://192.168.2.41:3000/v1",
)


def test_oneapi():
  response = client.chat.completions.create(
    model="moonshot-v1-auto",
    messages=[{"role": "user", "content": "Hello, world!"}],
  )
  logger.info(response.choices[0].message.content)

  print(response.choices[0].message.content)
