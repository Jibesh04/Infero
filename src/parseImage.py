# import json
import boto3
# import urllib.parse
# from pprint import pprint


from PIL import Image
import io


s3 = boto3.client('s3',
                aws_access_key_id='',
                aws_secret_access_key='',
                region_name='')

def im_resize(img):
    try:
        width, height = img.size
        M = max(width, height)
        if M > 640:
            newsize = ((640, height * 640//width) if width == M else (width * 640//height, 640))
            img = img.resize(newsize, Image.LANCZOS)
    except Exception as e:
        print(e)
    return img

def returnImage(response):
    image_content = response['Body'].read()
    image = Image.open(io.BytesIO(image_content))
    # image.show()
    return im_resize(image)

def getImage(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        # pprint(response)
        return returnImage(response)
    
    except Exception as e:
        # pprint(e)
        return str(e)