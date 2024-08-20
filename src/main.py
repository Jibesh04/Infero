from parseImage import getImage
from makeInf import predict
from storeInDB import upload_image_with_metadata
from datetime import datetime

def create_metadata(s3_url, key, boxes):
    detection = {}
    if boxes:
        detection['boxes'] = []
        for box in boxes:
            detection['boxes'].append({
                'class': box.cls.item(),
                'confidence': box.conf.item(),
                'box': box.xywh.tolist()
            })
    metadata = {
        "image_data": None,
        "src_img": key,
        "src_s3_URL": s3_url,
        "inference_result": detection,
        "created_at": datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")
    }
    return metadata

# def lambda_probe(bucket, key):
#     url = f"https://{bucket}.s3.amazonaws.com/{key}"
#     img_file = getImage(bucket=bucket, key=key)
#     print(img_file)
#     result_img, res_boxes = predict(img=img_file, key=key)
#     metadata = create_metadata(s3_url=url, key=key, boxes=res_boxes)
#     resp = upload_image_with_metadata(image=result_img, metadata=metadata)
#     print(resp)

# lambda_probe("imagesdisha2805", "JEWgqh6w20240608005241125279.png")
def lambda_handler(event, context):
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
        img_file = getImage(bucket=bucket_name, key=object_key)
        result_img, res_boxes = predict(img=img_file, key=object_key)
        metadata = create_metadata(s3_url=url, key=object_key, boxes=res_boxes)
        resp = upload_image_with_metadata(image=result_img, metadata=metadata)
        return {
            'statusCode': 200,
            'body': {'message': 'Inference successful', 'db_status': resp}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'message': 'Server Error', 'error': str(e)}
        }
# event = {
#         'Records': [
#             {
#                 's3': {
#                     'bucket': {'name': 'imagesdisha2805'},
#                     'object': {'key': '7PJXQPxf20240608111650578769.png'}
#                 }
#             }
#         ]
#     }
# context = {}
# response = lambda_handler(event, context)