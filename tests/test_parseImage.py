import pytest
from PIL import Image
from app.src.parseImage import getImage, im_resize, returnImage
# from parseImage import getImage, im_resize, returnImage
import boto3
from moto import mock_aws
import io

@mock_aws
def test_getImage():
    s3 = boto3.client('s3', region_name='us-east-1')
    bucket = ""
    key = ""
    
    s3.create_bucket(Bucket=bucket)
    img = Image.new('RGB', (100, 100))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    s3.put_object(Bucket=bucket, Key=key, Body=img_byte_arr.getvalue())
    
    image = getImage(bucket, key)
    assert image is not None
    assert isinstance(image, Image.Image)

def test_im_resize():
    img = Image.new('RGB', (800, 600))
    resized_img = im_resize(img)
    assert resized_img.size[0] <= 640
    assert resized_img.size[1] <= 640
