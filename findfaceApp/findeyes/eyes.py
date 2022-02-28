
# import paddlehub as hub
# module = hub.Module(name="pyramidbox_lite_mobile_mask", version="1.1.0")
# results = module.face_detection(data={"image": ["face_mask_2_386.jpg"]}) 

import paddlehub as hub
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
 
# 1.待预测图片
test_img_path = ["./face_mask_2_386.jpg"]
 
# 2.载入模型
module = hub.Module(name="pyramidbox_lite_mobile_mask", version="1.1.0")
 
# 3.预测
input_dict = {"image": test_img_path}
results = module.face_detection(data=input_dict)
 
# # 4.结果展示
# img = mpimg.imread("detection_result/face_mask_2_386.jpg")
# plt.figure(figsize=(10, 10))
# plt.imshow(img)
# plt.axis('off')
# plt.show()


# import cv2
# import os
# from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget,
#     QMessageBox, QHBoxLayout, QVBoxLayout, QSlider, QListWidget,
#     QPushButton, QLabel, QComboBox, QFileDialog, QLineEdit, QTextEdit, 
#     QTextBrowser, QInputDialog)
# from pathlib import Path


# class Findeyes():
#     def __init__(self):
#         self.haar = cv2.data.haarcascades + "haarcascade_eye.xml"


#     def find_face_cv2(self, img_path):

#         # 读取原始图像
#         img = cv2.imread(img_path)

#         # 调用熟悉的人脸分类器 检测特征类型
#         # 人脸 - haarcascade_frontalface_default.xml
#         # 人眼 - haarcascade_eye.xm
#         # 微笑 - haarcascade_smile.xml
#         face_detect = cv2.CascadeClassifier(self.haar)

#         # 灰度处理
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         # 检查人脸 按照1.1倍放到 周围最小像素为5
#         face_zone = face_detect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
#         print ('识别人脸的信息：',face_zone)

#         # if type(face_zone) != tuple:

#         #     print(f"{img_path} {'='*10} pass")
#         #     return True
            
#         #     if not os.path.exists(pass_dir): os.makedirs(pass_dir)
#         #     Image.open(img_path).convert('RGB').save(f"{pass_dir}{random.randint(1, 10000000000)}.jpg")

#         if type(face_zone) != tuple:
#             # 绘制矩形和圆形检测人脸
#             for x, y, w, h in face_zone:
#                 # 绘制矩形人脸区域 thickness表示线的粗细
#                 cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h),color=[0,0,255], thickness=2)
#                 # 绘制圆形人脸区域 radius表示半径
#                 cv2.circle(img, center=(x+w//2, y+h//2), radius=w//2, color=[0,255,0], thickness=2)

#             # 设置图片可以手动调节大小
#             cv2.namedWindow("Easmount-CSDN", 0)

#             # 显示图片
#             cv2.imshow("Easmount-CSDN", img)

#             # 等待显示 设置任意键退出程序
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()


# if __name__ == "__main__":
#     # a = QApplication([])
#     # path = QFileDialog.getOpenFileName(QWidget(), "选取文件路径", "/Users/wilson/Downloads/Mask/Image")[0]
#     # if path:
#     #     print(path)
#     #     Findeyes().find_face_cv2(path)

#     Findeyes().find_face_cv2(r"/Users/wilson/Downloads/Mask/Image/mask_test_movie__434.jpg")
