import pytest
from app.src.storeInDB import upload_image_with_metadata, connect_to_mongodb
# from storeInDB import upload_image_with_metadata, connect_to_mongodb
from PIL import Image
import io
from pymongo import MongoClient
import gridfs

@pytest.fixture
def mongodb():
    uri = ""
    db_name = ""
    client = MongoClient(uri)
    db = client[db_name]
    yield db
    # client.drop_database(db_name)

def test_upload_image_with_metadata(mongodb):
    img = Image.new('RGB', (100, 100))
    metadata = {
        "src_img": "",
        "src_s3_URL": "",
        "inference_result": {},
        # "created_at": "2024-06-12T00:00:00"
    }
    response = upload_image_with_metadata(img, metadata)
    assert response['success']
