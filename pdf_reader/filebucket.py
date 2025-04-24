import os

import boto3


def get_bucket(bucket_name):
  s3 = boto3.resource(
    "s3",
    endpoint_url="http://127.0.0.1:9090",
    config=boto3.session.Config(signature_version="s3v4"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY", "minio"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY", "password"),
  )
  return s3.Bucket(bucket_name)


def remove_file(bucket_name, object_name):
  """删除文件"""
  bucket = get_bucket(bucket_name)
  return bucket.delete_objects(Delete={"Objects": [{"Key": object_name}]})


def save_file(file_path, bucket_name, object_name):
  """保存文件"""
  bucket = get_bucket(bucket_name)

  if not bucket.creation_date:
    bucket.create(
      ACL="private",
      CreateBucketConfiguration={"LocationConstraint": os.getenv("MINIO_REGION", "us-east-1")},
    )

  return bucket.put_object(Key=object_name, Body=file_path)
