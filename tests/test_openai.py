import os

from loguru import logger
from openai import OpenAI


def test_openai_2():
  client = OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
  )
  response = client.chat.completions.create(
    model="moonshot-v1-auto",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, world!"},
    ],
  )
  logger.info(response.choices[0].message.content)
  assert response.choices[0].message.content is not None


def test_openai():
  client = OpenAI()
  response = client.chat.completions.create(
    model="moonshot-v1-auto",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello, world!"},
    ],
  )
  logger.info(response.choices[0].message.content)
  assert response.choices[0].message.content is not None
