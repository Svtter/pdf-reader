import os

from langfuse.decorators import observe
from langfuse.openai import openai


@observe()
def story():
  return (
    openai.chat.completions.create(
      model="moonshot-v1-auto",
      max_tokens=100,
      messages=[
        {"role": "system", "content": "You are a great storyteller."},
        {"role": "user", "content": "Once upon a time in a galaxy far, far away..."},
      ],
    )
    .choices[0]
    .message.content
  )


@observe()
def main():
  return story()


def test_langfuse():
  assert os.getenv("OPENAI_BASE_URL") is not None
  assert os.getenv("OPENAI_API_KEY") is not None
  main()
