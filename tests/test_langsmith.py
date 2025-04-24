import openai
from langsmith import traceable
from langsmith.wrappers import wrap_openai

# Auto-trace LLM calls in-context
client = wrap_openai(openai.Client())


@traceable  # Auto-trace this function
def pipeline(user_input: str):
  result = client.chat.completions.create(messages=[{"role": "user", "content": user_input}], model="moonshot-v1-auto")
  return result.choices[0].message.content


def test_langsmith():
  pipeline("Hello, world!")
  # Out:  Hello there! How can I assist you today?
