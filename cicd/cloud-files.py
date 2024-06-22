import os
import boto3
from botocore.exceptions import NoCredentialsError
from tqdm import tqdm
import cicd.mdxutils as mdxutils

"""
Thrid Part Libs
- boto3
- tqdm
"""

bucket = str(input("Bucket Name: "))
base_path = str(input("Basedir: "))
folder = str(input("Folder: "))
is_public = input("Is Public (y/n): ")
extra_args = {}

if str(is_public).lower().strip() == "y":
    extra_args = {"ACL": "public-read"}



class ProgressPercentage:
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = tqdm.get_lock()
        self._tqdm = tqdm(total=self._size, unit='B', unit_scale=True, desc=filename)

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            self._tqdm.update(bytes_amount)

def upload_file (abspath, filename, **kwargs):
    KeyName = (
        filename
        .replace(' ', '-')
        .replace('---', '-')
    )
    KeyName = f"{folder}/{KeyName}"
    s3 = boto3.client('s3')

    try:
        s3.upload_file(
            Filename=abspath,
            Bucket=bucket,
            Key=KeyName,
            ExtraArgs=extra_args,
            Callback=ProgressPercentage(abspath)
        )
        print(f"File {bucket}/{KeyName} uploaded successful")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials missing")
    except Exception as e:
        print("unknown error ", e)

mdxutils.get_dir_files(base_path, upload_file)