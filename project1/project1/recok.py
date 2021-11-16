import boto3
import os
import io
import os
import cv2
import boto3
from django.shortcuts import get_object_or_404
import numpy as np

from google.cloud import vision
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

'''
- config_env
: 이미지를 자르고 버킷에 저장/ 번호판 대상으로 다시 Google Vision API 호출하기 위해 필요한 설정값들을 설정해줌
=> 총 4가지의 값을 설정하여 ,List 로 묶어 반환
   =>> Google Vision API 사용을 위한 Client 객체 
   =>> google vision api 가 인식할 수 있도록 변환된 image (원본 이미지) 
   =>> OpenCV 가 인식할 수 있도록 변환된 image (원본 이미지)
   =>> 번호판 사진을 저장할 Bucket 의 정보 (해당 목적지 Bucket 객체, 저장될 파일의 이름)
=> 매개변수
   =>> srcBucket 
       : 불러올 이미지가 저장된 버킷의 이름
   =>> file_name
       : 불러올 이미지 파일의 이름 (경로, .jpg 제외)
   =>> dstBucket    
       : 번호판 사진을 저장할 버킷의 이름
'''

def config_env(srcBucket, file_name, dstBucket):
    configs=[]

    os. environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\kang4\\privateKey\\temporal-parser-329211-ce27c0f3eb53.json'
    client = vision.ImageAnnotatorClient()

    s3= boto3.resource('s3', 
                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                    region_name='ap-northeast-2'
    )
    
    src_bucket = s3.Bucket(srcBucket) 
    img = src_bucket.Object('static/img/{}'.format(file_name)).get().get('Body').read()
    img_complete = cv2.imdecode(np.asarray(bytearray(img)),cv2.IMREAD_COLOR)
    
    dst_bucket = s3.Bucket(dstBucket)

    configs.append(client)                            ## Google Vision API 사용을 위한 Client 객체
    configs.append(CVToVision(img_complete,os.path.splitext(file_name)[1]))   ## google vision api 가 인식할 수 있도록 변환된 image (원본 이미지)
    configs.append(img_complete)                      ## OpenCV 가 인식할 수 있도록 변환된 image (원본 이미지)
    configs.append(list((dst_bucket,file_name)))      ## 번호판 사진을 저장할 Bucket 의 정보 (해당 목적지 Bucket 객체, 저장될 파일의 이름)

    return configs                                 

'''
- getImgSize
  => OpenCV 가 인식할 수 있도록 변환된 이미지 를 인자로 받아, 그 이미지의 가로 세로 픽셀 길이를 반환
  => 매개변수
     =>> cv_img
         : OpenCV 가 인식할 수 있도록 변환된 이미지
'''

def getImgSize(cv_img):   
    h,w,c= cv_img.shape
    return h,w

'''
- getPlateCoords
  : 주어진 이미지에서, 번호판의 4개의 꼭짓점 좌표를 list로 반환, 만약, 인식이 불가하다면, -1 반환
  => 매개변수
     =>> gpc_image
         : Google Vision API 가 인식할 수 있는 이미지 타입으로, Google VisionAPI 를 통해, 번호판 인식을 시킬 이미지
     =>> client
         : Google Vision API 사용을 위해 필요한 Client 객체
     =>> img_size
         : 해당 인식시킬 이미지 크기 정보    
'''


def getPlateCoords(gpc_image,client,img_size):                        ## get Absolute Coords of plate if it exists, if failed 0 returned
    objects = client.object_localization(image=gpc_image).localized_object_annotations
    norm_coords = []

    for object_ in objects:
        if(object_.name == 'License plate'):   
            for vertex in object_.bounding_poly.normalized_vertices:
                norm_coords.append(tuple((vertex.x, vertex.y)))
    
    if not norm_coords:
        return -1

    Abs = []

    for coord in norm_coords:
        Abs.append(list([int(coord[0]*img_size[1]), int (coord[1]*img_size[0])]))
    return Abs

'''
- getTextsCoords
  => 이미지 상에 인식된 모든 텍스트들의 좌표들을 List로 묶어 반환
  => 매개변수
     =>> gpc_image
         : Google Vision API 가 인식할 수 있는 이미지 타입으로, Google VisionAPI 를 통해, 번호판 인식을 시킬 이미지(잘려진 번호판 사진)
     =>> client
         : Google Vision API 사용을 위해 필요한 Client 객체


'''

def getTextsCoords(gpc_image, client):
    response = client.text_detection(image=gpc_image)
    texts = response.text_annotations

    textCoords= []

    for text in texts:
        textCoords.append(tuple((text.description,[(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices])))
    
    return textCoords

'''
- uploadS3
 : 인자로 주어진 이미지를, 인자로 주어진 목적지 버킷에다가 저장
=> 매개변수
   =>> cv_img
       : 저장할 이미지 (CV image 타입)
   =>> dst_info   
       : 목적지 버킷에 대한 정보 (목적지 버킷 객체와, 저장될 파일의 이름)들을 담고 있는 리스트
'''
def uploadS3(cv_img,dst_info):            
    dstBucket, file_name =dst_info
    image_string = cv2.imencode('.jpg', cv_img)[1].tobytes() 
    dstBucket.put_object(Key = 'static/img/cropped_{}'.format(file_name), Body=image_string)

'''
- CVToVision
  : OpenCV가 인식하는 이미지 타입을, Google Vision API가 인식할 수 있는 이미지 타입으로 변경하여 반환
  => OpenCV 가 인식하는 이미지 타입은 numpy array 타입, Google Vision APi가 인식할 수 있는 이미지 타입은 ByteArray 타입
  => 매개변수  
      =>> cv_img
         : 변환할 이미지 (CV image 타입)

'''
def CVToVision(cv_img,img_format):
    image = cv_img
    success, encoded_image = cv2.imencode(img_format, image)
    content2 = encoded_image.tobytes()
    image_cv2 = vision.Image(content=content2)
    return image_cv2



    
'''
- Crop_Image
  : 본격적으로 주어진 설정값들을 토대호, 선 번호판 검출 후 해당 번호판 자르기 시작함. 최종적으로 번호판 인식이 불가하여,
    자르지 못한 경우, 빈 List 를, 인식에 성공한 경우, 잘려진 이미지(CV 가 인식 가능한 이미지 타입)값을 반환
  => 매개변수
     =>> configs
         : config_env 함수에서 설정한 값들의 List 

'''
def Crop_Image(configs):
    client,gpc_image,cv_img,dst_info = configs
    img_prop= getImgSize(cv_img)
    
    Abs = getPlateCoords(gpc_image,client,img_prop)
    if(Abs == -1):
        print('No Plate Detected')
        return []

    print('Plate Detected Cropping Now')
    pts = np.array(Abs)
    
    ## (1) Crop the bounding rect
    poly_4 = cv2.boundingRect(pts)  
    x,y,w,h = poly_4
    croped = cv_img[y:y+h, x:x+w].copy()
    
    ## (2) make mask
    pts = pts - pts.min(axis=0)
    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
    
    ## (3) do bit-op
    dst = cv2.bitwise_and(croped, croped, mask=mask)
    
    ## (4) add the white background
    bg = np.ones_like(croped, np.uint8)*255
    cv2.bitwise_not(bg,bg, mask=mask)
    dst2 = bg+ dst


    ## author BY Baek Geon Woo From KAU
    return dst2
def delete_s3Image(Photo):
    s3 = boto3.client('s3')
    s3.delete_object(Bucket="forstatic",Key=Photo)
    return
def detect_labels():   
    photo='static/img/No9.png'
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
            img_format = os.path.splitext("No9.png")[1]
            configs = config_env("forstatic","No9.png","forstatic")     ## [api_client 객체, google vision image 객체, cv_image 객체,[목적지 Bucket, 파일 이름]]
            crop_res = Crop_Image(configs)                     
            if not len(crop_res):
                print('No Plate Detected... Terminating Process...')
                quit()
            text = [text[0] for text in getTextsCoords(CVToVision(crop_res,img_format), configs[0])][1:]
            print(text)
            delete_s3Image(photo)
            # s3=boto3.client('s3')
            # s3.delete_object(Bucket=bucket,Key='static/img/No9.png')


detect_labels() 



