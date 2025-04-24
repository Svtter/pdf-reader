# PDF Reader

1. 如果我想从 pdf 中读取数据，我应该如何编写 prompt？
2. 我想提供特定 csv 结构的表头给用户，我应该如何编写 prompt？


## 主流程

- DONE 将多个 prompt 混合成一个，向大模型提问。
- DONE 提问完成后，得到一个混合的 csv text
- DONE 向大模型请求，获取多个 csv 文件。
- DONE 合并这些 excel 文件

根据提供的 template，将不同的 csv 文件放在不同的 sheet，并且与之前的文件进行合并。

## Thinking

现在的技术基于 openai sdk 以及没有使用 agent 或者 ai 框架。
我在想，是不是应该应用一下 agent 框架来组成相关的逻辑。

## Developer

1. 查看 mongodb 数据：`open localhost:8081`
2. 查看 minio 数据：`open localhost:9091`

### Support framework

1. Tracing

- langsmith
- langfuse

2. API

- Kimi
- Zhipu
- Silicon (not work)
- OpenAI (no api key)
