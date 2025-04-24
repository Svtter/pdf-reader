from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient


class DB:
  def __init__(self):
    self.client = MongoClient("mongodb://localhost:27017/", username="admin", password="password")

  def save_chat(self, chat: dict):
    chat.update({"created_at": datetime.now()})
    self.client["pdf-reader"]["chats"].insert_one(chat)

  def get_latest_chat(self):
    # 获取最新的一条 chat
    return self.client["pdf-reader"]["chats"].find().sort("created_at", -1)[0]

  def get_chat_by_id(self, chat_id: str):
    return self.client["pdf-reader"]["chats"].find_one({"_id": ObjectId(chat_id)})
