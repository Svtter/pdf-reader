"""read pdf file with rag"""

import pathlib

from pdf_reader.db import DB


class RAGReader(object):
  def __init__(self):
    self.db = DB()

  def load_file(self, file_path: pathlib.Path):
    """load file"""
    pass
