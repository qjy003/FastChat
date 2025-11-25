# 配置文件：保存线上线下环境需要的各种配置信息

import os

# OpenAI相关配置
# Azure OpenAI API密钥
AZURE_OPENAI_API_KEY = ""
# 服务运行的端口
PORT = 18866
# Azure OpenAI API基础URL，默认值从环境变量获取，或使用提供的代理地址
AZURE_OPENAI_API_BASE = os.environ.get("AZURE_OPENAI_API_BASE", "http://gpt-proxy.jd.com/gateway/azure")
# 是否使用提示模板，默认值从环境变量获取，并转换为布尔值
USE_PROMPT_TEMPLATE = os.environ.get("USE_PROMPT_TEMPLATE", "True") == "True"
# GPT模型名称
GPT_MODEL = "gpt-35-turbo-1106"
# 嵌入模型名称
EMBEDDING_MODEL_NAME = "text-embedding-ada-002-2"
# 嵌入模型类型
EMBEDDING_MODEL_TYPE = "OpenAIEmbeddings"

# Vearch配置：连接知识库的默认配置
VEARCH_CONFIG = {
    "master_url": "",  # 主节点URL
    "router_url": "",  # 路由节点URL
    "db_name": "",  # 数据库名称
    "space_name": "",  # 空间名称
    "embedding_deminsion": 1536,  # 嵌入维度
}

# 对话格式配置（此处未具体配置，仅作为注释标题）

# 线上部署相关配置
# 主路径，默认值从环境变量获取
MAIN_PATH = os.environ.get("JD_ONLINE_MAIN_PATH", "")
# 不良案例JSON目录，默认值从环境变量获取
BAD_CASES_JSON_DIR = os.environ.get("JD_ONLINE_BAD_CASE_DIR", "data/json")
# 日志目录，默认值从环境变量获取
LOGGING_DIR = os.environ.get("JD_ONLINE_LOGGING_DIR", "data/log")
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

# 设置环境变量
# 将Azure OpenAI API密钥和基础URL设置到环境变量中，以便后续代码使用
os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
os.environ["OPENAI_API_BASE"] = AZURE_OPENAI_API_BASE

# ES日志记录服务配置信息
Elasticsearch_Params = {
    "hosts": [{"host": "",
               "port": 9200,
               "scheme": "http"}],
    "http_auth": ('', ''),
    "timeout": 500
}
Elasticsearch_Table = ""