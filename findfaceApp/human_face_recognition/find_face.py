#coding:utf-8
import datetime
from itertools import count
import os
import re
import shutil
import time
import face_recognition
import cv2
import matplotlib.pyplot as plt
import sys
from PIL import Image, ImageDraw
from pathlib import Path
import random
import dlib
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import qdarkstyle

import numpy as np

class readfile():

    def __init__(self) -> None:
        self.files = []

    def allfile(self, path) -> None:
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                new_file = path+'/'+file
                if os.path.isdir(new_file):
                    self.allfile(new_file)
                else:
                    self.files.append(new_file)
        else:
            self.files.append(path)

    def listfiles(self, path) -> list:
        path = self.format_path(path)
        self.allfile(path)
        return self.files

    def format_path(self, path) -> str:
        path = os.path.abspath(path)
        path = path.replace('\\', '/')
        path = path.replace('//', '/')
        path = path[:-1] if path[-1] == '/' else path
        return path

    def last_path(self, path) -> str:
        path = path[path.rfind('/')+1:]
        return path

    def sub_path(self, path, rootpath) -> str:
        path = path[path.find(rootpath)+len(rootpath):]
        path = path[1:] if path[0] == '/' else path
        return path



# face_recognition 文档：https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md

class Findface():
    def find_face_cv2(self, img_path, pass_dir, fail_dir):

        # 读取原始图像
        img = cv2.imread(img_path)

        # 调用熟悉的人脸分类器 检测特征类型
        # 人脸 - haarcascade_frontalface_default.xml
        # 人眼 - haarcascade_eye.xm
        # 微笑 - haarcascade_smile.xml
        face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # 检查人脸 按照1.1倍放到 周围最小像素为5
        face_zone = face_detect.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
        # print ('识别人脸的信息：',face_zone)

        if type(face_zone) != tuple:

            print(f"{img_path} {'='*10} pass")
            return True
            
            if not os.path.exists(pass_dir): os.makedirs(pass_dir)
            Image.open(img_path).convert('RGB').save(f"{pass_dir}{random.randint(1, 10000000000)}.jpg")

            # # 绘制矩形和圆形检测人脸
            # for x, y, w, h in face_zone:
            #     # 绘制矩形人脸区域 thickness表示线的粗细
            #     cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h),color=[0,0,255], thickness=2)
            #     # 绘制圆形人脸区域 radius表示半径
            #     cv2.circle(img, center=(x+w//2, y+h//2), radius=w//2, color=[0,255,0], thickness=2)

            # # 设置图片可以手动调节大小
            # cv2.namedWindow("Easmount-CSDN", 0)

            # # 显示图片
            # cv2.imshow("Easmount-CSDN", img)

            # # 等待显示 设置任意键退出程序
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        else:

            print(f"{img_path} {'='*10} fail")
            return False
            
            if not os.path.exists(fail_dir): os.makedirs(fail_dir)
            Image.open(img_path).convert('RGB').save(f"{fail_dir}{random.randint(1, 10000000000)}.jpg")


    def find_face_fr(self, img_path, pass_dir, fail_dir):

        image=face_recognition.load_image_file(img_path)

        face_locations=face_recognition.face_locations(image)

        face_num2=len(face_locations)
        # print(face_num2)

        if face_num2:
            print(f"{img_path} {'='*10} pass")
            return True
            
            if not os.path.exists(pass_dir): os.makedirs(pass_dir)
            Image.open(img_path).convert('RGB').save(f"{pass_dir}{random.randint(1, 10000000000)}.jpg")

            # org=cv2.imread(img_path)
            # for i in range(0,face_num2):
            #     top=face_locations[i][0]
            #     right=face_locations[i][1]
            #     bottom=face_locations[i][2]
            #     left=face_locations[i][3]
                
            #     start=(left,top)
            #     end=(right,bottom)
                
            #     color=(0,255,0)
            #     thickness=5
            #     img=cv2.rectangle(org,start,end,color,thickness)
                
            # plt.imshow(img)
            # plt.axis("off")
            # plt.show()

        if face_num2 == 0:
            print(f"{img_path} {'='*10} fail")
            return False
            
            if not os.path.exists(fail_dir): os.makedirs(fail_dir)
            Image.open(img_path).convert('RGB').save(f"{fail_dir}{random.randint(1, 10000000000)}.jpg")

            # cv2.imshow("Easmount-CSDN", image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()


    def mkdir(self, path):
        path = re.findall("(.*/)", path)[0]
        print("当前路径：", path)
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print("#"*50)
            print("建立新的文件路径于: {}".format(path))
            print("#"*50)


    def writeFile(self, path, file):
        self.mkdir(path)
        with open(path, 'w', encoding='UTF-8') as f:
            f.write(file)
        f.close
        print("成功写入文件至: {}".format(path))
        return path


    def mark_face_detail(self, path):

        try:
            image = face_recognition.load_image_file(path)
            #查找图像中所有面部的所有面部特征
            face_landmarks_list = face_recognition.face_landmarks(image)
            face_landmarks = face_landmarks_list[0]
        except Exception as error:
            print("无法识别到人脸！！！！")
            return False


        allx = 0
        ally = 0
        for i in face_landmarks['right_eye']:
            allx += i[0]
            ally += i[1]

        lex = round(allx/len(face_landmarks['right_eye']))
        ley = round(ally/len(face_landmarks['right_eye']))

        # print("left eye:", lex, ley, '\n', "**"*40)

        allx = 0
        ally = 0
        for i in face_landmarks['left_eye']:
            allx += i[0]
            ally += i[1]

        rex = round(allx/len(face_landmarks['right_eye']))
        rey = round(ally/len(face_landmarks['right_eye']))

        # print("right eye:", rex, rey, '\n', "**"*40)

        nsx = face_landmarks['nose_bridge'][-1][0]
        nsy = face_landmarks['nose_bridge'][-1][1]

        # print("nose:", nsx, nsy, '\n', "**"*40)

        maxt = max(face_landmarks['top_lip'])
        maxb = max(face_landmarks['bottom_lip'])
        lm = maxt if maxt == maxb else max([maxt, maxb])
        lmx = lm[0]
        lmy = lm[1]

        # print("left lip:", lmx, lmy, '\n', "**"*40)

        mint = min(face_landmarks['top_lip'])
        minb = min(face_landmarks['bottom_lip'])
        rm = mint if mint == minb else min([mint, minb])
        rmx = rm[0]
        rmy = rm[1]

        # print("right lip:", rmx, rmy, '\n', "**"*40)


        ffpfile = f"LEX {lex}\nLEY {ley}\nREX {rex}\nREY {rey}\nNSX {nsx}\nNSY {nsy}\nLMX {lmx}\nLMY {lmy}\nRMX {rmx}\nRMY {rmy}"

        # print(ffpfile)

        filename = readfile().last_path(path)
        filename = filename.replace('jpg', 'ffp')

        dir = '{}/Downloads/FFP/{}'.format(str(Path.home()), filename)

        self.writeFile(dir, ffpfile)


    def show_face_mark(self, path):
        path = readfile().format_path(path)
        image = face_recognition.load_image_file(path)

        #查找图像中所有面部的所有面部特征
        face_landmarks_list = face_recognition.face_landmarks(image)

        # print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

        if not face_landmarks_list:
            print("无法识别到人脸！！！！")
            return False

        face_landmarks = face_landmarks_list[0]

        #打印此图像中每个面部特征的位置
        facial_features = [
            'chin',
            'nose_bridge',
            'left_eye',
            'right_eye',
            'top_lip',
            'bottom_lip'
        ]

        for facial_feature in facial_features:
            print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))
        
        # 获取面部标记点
        print("**"*40)

        # 在图像中描绘出每个人脸特征！
        pil_image = Image.fromarray(image)
        d = ImageDraw.Draw(pil_image)

        for facial_feature in facial_features:
            d.line(face_landmarks[facial_feature], width=1)
        pil_image.show()



    def unit_mark_face_detail(self, paths):
        for path in paths:
            self.mark_face_detail(path)


    def multprocess(self, path):
        path = readfile().format_path(path)
        paths = readfile().listfiles(path)

        start = datetime.datetime.now()

        length = len(paths)
        p1 = []
        p2 = []
        p3 = []
        p4 = []
        p5 = []

        for i in range(length):
            if i < round(length/5):
                p1.append(paths[i])
            elif i >= round(length/5) and i <(2*round(length/5)):
                p2.append(paths[i])
            elif i >= (2*round(length/5)) and i < (3*round(length/5)):
                p3.append(paths[i])
            elif i >= (3*round(length/5)) and i < (4*round(length/5)):
                p4.append(paths[i])
            else:
                p5.append(paths[i])

        multp = [p1,p2,p3,p4,p5]
        
        # q = Queue()
        process_list = []
        for i in multp:
            print("开始运行")
            p = Process(target=self.unit_mark_face_detail,args=(i,))
            p.start()
            process_list.append(p)

        for p in process_list:
            p.join()


        end = datetime.datetime.now()
        print(f"总图片：{length} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(length/int((end - start).seconds))} 张")
        app = QApplication([])
        self.Tips("人脸图片标注已结束\n文件保存在下载文件夹中")



    def unit_find_face(self, pathlist, pass_dir, fail_dir, mode):
        ps = []
        fl = []
        coun = 1

        if mode == 'fr':
            for path in pathlist:
                if self.find_face_fr(path, pass_dir, fail_dir):
                    ps.append(path)
                else:
                    fl.append(path)
                print(f"识别进度：{coun} / {len(pathlist)}")
                coun += 1
        if mode == 'cv2':
            for path in pathlist:
                if self.find_face_cv2(path, pass_dir, fail_dir):
                    ps.append(path)
                else:
                    fl.append(path)
                print(f"识别进度：{coun} / {len(pathlist)}")
                coun += 1

        for i in ps:
            if not os.path.exists(pass_dir): os.makedirs(pass_dir)
            Image.open(i).convert('RGB').save(f"{pass_dir}{random.randint(1, 10000000000)}.jpg")


        for i in fl:
            if not os.path.exists(fail_dir): os.makedirs(fail_dir)
            Image.open(i).convert('RGB').save(f"{fail_dir}{random.randint(1, 10000000000)}.jpg")


    def multp_find_face(self, path, tmpfile):
        start = datetime.datetime.now()

        # use fr to check the face

        path = readfile().format_path(path)
        paths = readfile().listfiles(path)

        fail_dir = '{}/Downloads/finish_fail/'.format(str(Path.home()))
        # pass_dir_fr = 'fr_pass/'
        pass_dir_fr = tmpfile

        length = len(paths)

        p1 = []
        p2 = []
        p3 = []
        p4 = []
        p5 = []
        p6 = []

        for i in range(length):
            if i < round(length/6):
                p1.append(paths[i])
            elif i >= round(length/6) and i <(2*round(length/6)):
                p2.append(paths[i])
            elif i >= (2*round(length/6)) and i < (3*round(length/6)):
                p3.append(paths[i])
            elif i >= (3*round(length/6)) and i < (4*round(length/6)):
                p4.append(paths[i])
            elif i >= (4*round(length/6)) and i < (5*round(length/6)):
                p5.append(paths[i])
            else:
                p6.append(paths[i])

        multp = [p1,p2,p3,p4,p5,p6]

        process_list = []
        for i in multp:
            print("开始运行")
            p = Process(target=self.unit_find_face,args=(i,pass_dir_fr,fail_dir,'fr',))
            p.start()
            process_list.append(p)

        for p in process_list:
            p.join()


        # use cv2 to check face

        paths = readfile().listfiles(pass_dir_fr)

        fail_dir = '{}/Downloads/finish_fail/'.format(str(Path.home()))
        pass_dir_cv = '{}/Downloads/final_pass/'.format(str(Path.home()))

        length = len(paths)

        p1 = []
        p2 = []
        p3 = []
        p4 = []
        p5 = []
        p6 = []

        for i in range(length):
            if i < round(length/6):
                p1.append(paths[i])
            elif i >= round(length/6) and i <(2*round(length/6)):
                p2.append(paths[i])
            elif i >= (2*round(length/6)) and i < (3*round(length/6)):
                p3.append(paths[i])
            elif i >= (3*round(length/6)) and i < (4*round(length/6)):
                p4.append(paths[i])
            elif i >= (4*round(length/6)) and i < (5*round(length/6)):
                p5.append(paths[i])
            else:
                p6.append(paths[i])

        multp = [p1,p2,p3,p4,p5,p6]

        process_list = []
        for i in multp:
            print("开始运行")
            p = Process(target=self.unit_find_face,args=(i,pass_dir_cv,fail_dir,'fr',))
            p.start()
            process_list.append(p)

        for p in process_list:
            p.join()


        end = datetime.datetime.now()
        print(f"总图片：{length} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(length/int((end - start).seconds))} 张")


    def deletefile(self, path):
        if os.path.isdir(path):
            # os.remove(path)
            subfiles = readfile().listfiles(path)
            pool = ThreadPoolExecutor(max_workers=10)
            for file in subfiles:
                pool.submit(self.deletefile, file)
            pool.shutdown()

            shutil.rmtree(path)
            print(f"删除文件夹：{path}")
            
        else:
            os.remove(path)
            # print(f"删除文件：{path}")


    def face(self, path):
        tmpfile = str(random.randint(1, 100000000))+'/'
        p = Process(target=self.multp_find_face, args=(path,tmpfile,))
        p.start()
        p.join()
        
        p = Process(target=self.deletefile, args=(tmpfile,))
        p.start()
        p.join()

        app = QApplication([])
        self.Tips("人脸图片清洗已结束\n文件保存在下载文件夹中")


    # 提示
    def Tips(self, message):
        window = QWidget()
        window.setWindowOpacity(0.9) # 设置窗口透明度
        window.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # 美化风格
        QMessageBox.about(window, "提示", message)



if __name__ == "__main__":

    if sys.argv[1] == 'face':
        Findface().face(sys.argv[2])
        

    if sys.argv[1] == 'mark':
        path = readfile().format_path(sys.argv[2])
        paths = readfile().listfiles(path)

        start = datetime.datetime.now()
        notfind = []
        for i in paths:
            # print(i)
            if Findface().mark_face_detail(i) == False:
                notfind.append(i)

        print(f"{len(notfind)} 张图片无法找到，需人工检查！！！！")
        for i in notfind:
            print(i)

        end = datetime.datetime.now()
        print(f"总图片：{len(paths)} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(len(paths)/int((end - start).seconds))} 张")


    if sys.argv[1] == 'show':
        Findface().show_face_mark(sys.argv[2])

    if sys.argv[1] == 'multmark':
        Findface().multprocess(sys.argv[2])

    if sys.argv[1] == 'delete':
        start = datetime.datetime.now()
        Findface().deletefile(sys.argv[2])
        end = datetime.datetime.now()
        print(f"删除文件用时：{(end-start).seconds} 秒")

    if sys.argv[1] == 'test':
        # pool = ThreadPoolExecutor(max_workers=2)

        # path = readfile().format_path(sys.argv[2])
        # paths = readfile().listfiles(path)

        # for i in paths:
        #     t = pool.submit(mark_face_detail, i)
        #     # if not t.running():
        #     #     time.sleep(5)
        #     # print(i)

        # pool.shutdown()

        # test(sys.argv[2])
        # find_face_cv2(r"C:/Users/cn-wilsonshi/Downloads/finish_fail/3480549624.jpg", '.', '.')
        Findface().deletefile(sys.argv[2])

    # face_detail(r"C:/Users/cn-wilsonshi/Downloads/old_version/glasses/20.jpg")

    

