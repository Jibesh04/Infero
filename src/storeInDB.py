from pymongo import MongoClient
import gridfs
# from PIL import Image
import io
import json
from bson import json_util
# import json

def connect_to_mongodb(uri, db_name):
    """Connect to MongoDB and return the database instance."""
    client = MongoClient(uri)
    return client[db_name]

def upload_image_with_metadata(image, metadata):
    """Upload an image along with metadata to MongoDB."""
    try:
        uri = ""
        db_name = ""
        db = connect_to_mongodb(uri, db_name)

        fs = gridfs.GridFS(db)    
        # Convert the PIL image to a BytesIO object
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        image_data = img_byte_arr.read()
        image_id = fs.put(image_data, filename="processed_image.png", metadata=metadata)
        metadata["_id"] = image_id
        metadata["image_data"] = image_data
        db['Results'].insert_one(metadata)
        return {
            'success': True,
            'body': json.loads(json_util.dumps(image_id))
        }

    except Exception as e:
        return {
            'success': False,
            'body': str(e)
        }

# def convert_to_dict(results):
#     """Convert YOLOv8 results to a dictionary."""
#     detections = []
#     for result in results:
#         detection = {}

#         # Convert bounding boxes
#         if result.boxes:
#             detection['boxes'] = []
#             for box in result.boxes:
#                 detection['boxes'].append({
#                     'class': box.cls.item(),
#                     'confidence': box.conf.item(),
#                     'box': box.xywh.tolist()
#                 })

#         # Convert segmentation masks
#         if result.masks:
#             detection['masks'] = result.masks.cpu().numpy().tolist()

#         # Convert keypoints
#         if result.keypoints:
#             detection['keypoints'] = result.keypoints.cpu().numpy().tolist()

#         # Convert classification probabilities
#         if result.probs:
#             detection['probs'] = result.probs.cpu().numpy().tolist()

#         # Convert oriented bounding boxes
#         if result.obb:
#             detection['obb'] = result.obb.cpu().numpy().tolist()

#         detections.append(detection)
    
#     return detections

# def main():
    
#     bucket = 'imagesdisha2805'
#     key = 'Amazon-S3-Logo.svg.png'
#     metadata = {
#         "image_id": None,
#         "src_img": "image_path",
#         "src_s3_URL": "demo_URL",
#         "inference_model": "YOLOv8x",
#         "inference_result": convert_to_dict(results),
#         "created_at": datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")
#     }
#     upload_image_with_metadata(db, image_path, metadata)
    

# if __name__ == "__main__":
#     main()
