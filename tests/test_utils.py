import glob

from pdf_reader.utils import merge_csv_to_excel


def get_csv_list():
  return glob.glob("./output/*.csv")


def test_merge_csv_to_excel():
  csv_list = get_csv_list()
  assert merge_csv_to_excel(csv_list, "./output/merged.xlsx")
