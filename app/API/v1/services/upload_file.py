import boto3
import datetime
from ....config import config

session = boto3.Session(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
)
# Let's use Amazon DynamoDB with DB resource
S3 = session.resource("s3", region_name=config.AWS_REGION_NAME)


def file_upload(folder, filename, file):
    now = str(datetime.datetime.now())
    response = S3.Bucket(config.AWS_BUCKET_NAME).put_object(
        Key=folder + "/" + now + "_" + filename, Body=file.file
    )
    key = response.key
    url = "https://%s.s3.amazonaws.com/%s" % (config.AWS_BUCKET_NAME, key)
    return url
