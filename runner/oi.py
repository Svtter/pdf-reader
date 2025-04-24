"""直接测试 openai file 接口"""

# 等待助手处理完成
import time

import openai

# 设置您的 OpenAI API 密钥
openai.api_key = "your-api-key"

# 上传文件
file = openai.File.create(file=open("your_file.txt", "rb"), purpose="assistants")

# 创建助手
assistant = openai.Assistant.create(
  name="File QA Assistant",
  instructions="你是一个可以根据上传文件内容回答问题的助手。",
  tools=[{"type": "file_search"}],
  model="gpt-4-1106-preview",
)

# 创建会话线程
thread = openai.Thread.create()

# 向助手发送消息
message = openai.ThreadMessage.create(
  thread_id=thread.id, role="user", content="请根据上传的文件内容回答以下问题：...", file_ids=[file.id]
)

# 运行助手
run = openai.ThreadRun.create(thread_id=thread.id, assistant_id=assistant.id)


while True:
  run_status = openai.ThreadRun.retrieve(run.id)
  if run_status.status == "completed":
    break
  time.sleep(1)

# 获取助手的回复
messages = openai.ThreadMessage.list(thread_id=thread.id)
for msg in messages.data:
  print(f"{msg.role}: {msg.content}")
