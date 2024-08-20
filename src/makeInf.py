from ultralytics import YOLO
from PIL import Image
# import io

model = YOLO("yolov8x.pt")

def result_to_image(result):
    temp = result.plot()
    if temp.shape[2] == 3:
        temp = temp[:, :, ::-1] 
    return Image.fromarray(temp.astype('uint8'))

def predict(img, key):
    results = model(img)
    print(type(results))
    result = results[0]
    # print(result.boxes)
    boxes = result.boxes  # Boxes object for bounding box outputs
    image = result_to_image(result)
    return image, boxes