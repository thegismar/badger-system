import boto3
from brownie import *
from rich.console import Console
from config.env_config import env_config
import os
import requests

console = Console()

# so this is weird, according to AWS Boto3 docs, you shouldn't be able to even **access** objects without having set
# the keys but since boto3 looks in all kinds of places for them, the only explanation i can think of is that you have
# them stored in some other place and it retrieves them from there when you call download.

# also are you using dotenv or decouple? or oth? i'd go with dotenv

# instead of changing the method signature i'd rather check if the presigned url is part of the .env file
PRESIGNED_URL = os.getenv("PRESIGNED_URL") # so this will return None if the env isn't set, whch is fine

def download(fileName):
    """"
    presigned: the URL that was generated by create_presigned_url
    """

    s3 = boto3.client("s3")

    upload_bucket = "badger-json"
    upload_file_key = "rewards/" + fileName

    console.print("Downloading file from s3: " + upload_file_key)

    # i wanna know if i'm here with the aws env variables set or not, case yes i use s3 method, case no the presigned
    # url case neither, exit with None
    # TODO this needs testing since according to the code, the env variables were never passed to the s3 object, yet, it  worked.

    if env_config.aws_access_key_id and env_config.aws_secret_access_key:
        s3_clientobj = s3.get_object(Bucket=upload_bucket, Key=upload_file_key)
    elif PRESIGNED_URL is not None:
        s3_clientobj = requests.get(PRESIGNED_URL).json()
    else:
        return None

    # okay, so i'm just gonna assume that the get_object method also returns a dict-like type, in which case this
    # **should** work.
    # TODO check if s3.get_object returns a dict-like type that can be accessed in a similar way as the get -json

    # console.print(s3_clientobj)
    s3_clientdata = s3_clientobj["Body"].read().decode("utf-8")

    return s3_clientdata


def upload(fileName):
    from config.env_config import env_config

    upload_bucket = "badger-json"
    upload_file_key = "rewards/" + fileName

    console.print("Uploading file to s3: " + upload_file_key)

    s3 = boto3.client(
        "s3",
        aws_access_key_id=env_config.aws_access_key_id,
        aws_secret_access_key=env_config.aws_secret_access_key,
    )
    s3.upload_file(fileName, upload_bucket, upload_file_key)
