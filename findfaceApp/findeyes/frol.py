
import datetime
from sys import argv
import tensorflow as tf
import os
import glob
from skimage import io
import matplotlib.pyplot as plt 
from multiprocessing import Process
from PIL import Image, ImageDraw
from pathlib import Path
 
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
 
import numpy as np
from keras.layers import  Input,Conv2D,BatchNormalization,Activation,Subtract
from keras.models import Model, load_model
from keras.callbacks import CSVLogger, ModelCheckpoint, LearningRateScheduler
from tensorflow.keras.optimizers import Adam
import keras.backend as K


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


 
def forl(path, pass_dir, fail_dir):
    model = load_model('FCN_baseline.h5')
    
    # img = io.imread(r'C:\\Users\\cn-wilsonshi\\Downloads\\checkfrol\\frol\\GlassCol00128.jpg')
    print(path)
    img = io.imread(path)
    img = img.astype('float') / 255.0
    img = np.expand_dims(img, axis=0)
    
    specular_mask = model.predict(img)

    th = 0.4
    specular_mask[specular_mask > th] = 1.0
    specular_mask[specular_mask <= th] = 0

    totalpex = len(specular_mask[specular_mask >= 0])
    hilightpex = len(specular_mask[specular_mask == 1.0])
    rate = round(hilightpex/totalpex, 2)*100

    # return rate

    print("++"*50)
    print(f"{hilightpex} / {totalpex} : {rate} %")

    if rate >= 6:
        if not os.path.exists(pass_dir): os.makedirs(pass_dir)
        Image.open(path).convert('RGB').save(f"{pass_dir}{readfile().last_path(path)}")
    else:
        if not os.path.exists(fail_dir): os.makedirs(fail_dir)
        Image.open(path).convert('RGB').save(f"{fail_dir}{readfile().last_path(path)}")
    
    # plt.subplot(1,2,1)
    # plt.imshow(img[0, :,:,:])
    # plt.subplot(1,2,2)
    # plt.imshow(specular_mask[0, :,:,0], cmap='gray')
    # plt.show()

def multforl(path, pass_dir, fail_dir):
    for i in path:
        forl(i, pass_dir, fail_dir)


if __name__ == "__main__":
    start = datetime.datetime.now()

    paths = readfile().listfiles(argv[1])

    print("find file: ", len(paths))

    length = len(paths)
    fail_dir = '{}/Downloads/fail/'.format(str(Path.home()))
    pass_dir_cv = '{}/Downloads/pass/'.format(str(Path.home()))

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
        p = Process(target=multforl,args=(i,pass_dir_cv,fail_dir,))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()


    end = datetime.datetime.now()
    print(f"总图片：{length} 张 {'*'*10} 用时：{(end - start).seconds} 秒 {'*'*10} 每秒：{round(length/int((end - start).seconds))} 张")



