import boto3
s3resource=boto3.resource('s3')
bucket=s3resource.Bucket(name='forstatic')
bucket.Object('123123.png').get()