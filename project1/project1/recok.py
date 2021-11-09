import boto3
import os

def detect_labels():   
    photo='static/img/ㅁㄴ.PNG'
    bucket='forstatic'
    client=boto3.client('rekognition',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                        region_name='ap-northeast-2')
    response = client.detect_labels(Image={'S3Object':
    {'Bucket':bucket,'Name':photo}},
             MaxLabels=10)

    flag=0
    for label in response['Labels']:           
        if(label['Name']=='Motorcycle' and label['Confidence']>80):
            print('오토바이 감지')
            flag=1

    helmet_flag=0
    flag2=0
    if(flag==1):
        for label in response['Labels']:
            if(label['Name']=='Helmet' and label['Confidence']>80):
                print('헬맷 착용')
                flag2=1
            else:
                helmet_flag=1

        if(flag2==0 and helmet_flag == 1):
            print("헬맷 미착용")
            print("이제 번호판 인식 시작")


detect_labels() 

