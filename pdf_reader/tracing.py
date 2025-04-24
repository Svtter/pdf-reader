"""通过编写装饰器来实现动态 tracing framework, 避免单一的 tracing framework 限制"""

import os

"""dynamic tracing framework"""
tracing_framework = os.getenv("TRACING_FRAMEWORK", "langfuse")


def tracable(*args, **kwargs):
  """wrapper langsmith traceable"""
  if tracing_framework == "langsmith":
    from langsmith import traceable

    return traceable(*args, **kwargs)
  else:
    return lambda x: x


def get_openai_client_cls():
  """获取 OpenAI 客户端"""
  if tracing_framework == "langfuse":
    from langfuse.openai import OpenAI

    return OpenAI
  elif tracing_framework == "langsmith":
    from langsmith.wrappers import wrap_openai
    from openai import OpenAI

    def fn(*args, **kwargs):
      return wrap_openai(OpenAI(*args, **kwargs))

    return fn
  else:
    raise ValueError(f"Unsupported tracing framework: {tracing_framework}")
