from pdf_reader.filebucket import remove_file, save_file


def test_save_and_remove_file():
  assert save_file(file_path="./resources/test.txt", bucket_name="test", object_name="test2.txt")
  assert remove_file(bucket_name="test", object_name="test2.txt")


def test_file_object_id():
  file_object = save_file(file_path="./resources/test.txt", bucket_name="test", object_name="test2.txt")
  assert file_object.bucket_name == "test"
  assert file_object.key == "test2.txt"
