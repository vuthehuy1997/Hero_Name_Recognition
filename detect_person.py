import torch
import cv2
import numpy as np

class Person_Detection:
    def __init__(self, device):
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s", device=device)
        # self.model.conf = 0.5
        # self.model.iou = 0.45
        # self.img_size = 640
        print('Person_Detection is loaded')

    def predict(self, img, size=640):
        bboxes = self.model(img)#, size = self.img_size)
        bboxes = bboxes.pandas().xyxy[0].values.tolist()
        
        bboxes = [i for i in bboxes if i[6] == 'person']
        bboxes = [i + [abs(i[0]-i[2])] for i in bboxes]
        print(bboxes)
        return bboxes

# # Model
# model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

# # Images
# img = "test_data/test_images/Ahri_278220660753197_round6_Ahri_06-02-2021.mp4_10_2.jpg"  # or file, Path, PIL, OpenCV, numpy, list
# img = cv2.imread(img)
# img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
# # Inference
# results = model(img)

# # Results
# bboxes = results.pandas().xyxy[0].values.tolist()
# print(bboxes)
# box = [int(i) for i in bboxes[0][:4]]
# print(box)
# img = img[box[1]:box[3],box[0]:box[2]]
# cv2.imwrite('test.jpg', img)