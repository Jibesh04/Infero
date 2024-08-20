import pytest
from app.src.main import create_metadata, lambda_handler
# from main import create_metadata, lambda_handler
from unittest.mock import patch
from datetime import datetime
from PIL import Image

def test_create_metadata():
    s3_url = "https://example.com/test-key"
    key = "test-key"
    boxes = []
    metadata = create_metadata(s3_url, key, boxes)
    assert metadata['src_img'] == key
    assert metadata['src_s3_URL'] == s3_url

@patch('app.src.main.getImage')
@patch('app.src.main.predict')
@patch('app.src.main.upload_image_with_metadata')
def test_lambda_handler(mock_upload_image_with_metadata, mock_predict, mock_getImage):
    mock_getImage.return_value = Image.new('RGB', (100, 100))
    mock_predict.return_value = (Image.new('RGB', (100, 100)), [])
    mock_upload_image_with_metadata.return_value = {'success': True}

    event = {
        'Records': [
            {
                's3': {
                    'bucket': {'name': ''},
                    'object': {'key': ''}
                }
            }
        ]
    }
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
