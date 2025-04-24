from pdf_reader.db import DB


def test_db():
  db = DB()
  db.save_chat({"question": "What is the capital of France?", "answer": "Paris"})
  get = db.get_latest_chat()

  for unused in ("_id", "created_at"):
    get.pop(unused)
  want = {"question": "What is the capital of France?", "answer": "Paris"}
  assert get == want
