import boto3
import os
AWS_ACCESS_KEY_ID = 'AKIA5MI27BRQRTCB2QCV'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'forstatic'
AWS_REGION='ap-northeast-2'

s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
region_name=AWS_REGION)

namelist = list()
obj = s3.list_objects(Bucket=AWS_STORAGE_BUCKET_NAME)
for content in obj['Contents']:
    if('static/img'in content['Key']):
        namelist.append(content['Key'])
for name in namelist:
    print(name)
