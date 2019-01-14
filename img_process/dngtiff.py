#! usr/bin/env python
# -*- coding: utf-8 -*-
import os.path,sys
# 待转换图片的保存路径
dirname = 'C:/Users/NGMI-08/Desktop/work/xin/C-40/'

for jpg in os.listdir(dirname):
    if os.path.splitext(jpg)[-1] == '.jpg':
   # if os.path.splitext(jpg)[-1] == '.dng':
        os.remove(os.path.join(dirname,jpg))
def dngToTif():
    i = 1
    for f in os.listdir(dirname):
        src = os.path.join(dirname,f)
        if os.path.isdir(src):
            continue
        dst = os.path.join(dirname,str(i)+'.dng')
        os.rename(src,dst)
        i += 1
        os.system("C:/Users/NGMI-08/Desktop/dcraw.exe -v -4 -H 0 -W -w -D -j -T "+dst)#命令行调用 dcraw(windows 下才可用)
def delJPG():
    for jpg in os.listdir(dirname):
        #if os.path.splitext(jpg)[1] == '.jpg':
       if os.path.splitext(jpg)[-1] == '.dng':
            os.remove(os.path.join(dirname,jpg))

def renameFiles():
    list = [x for x in os.listdir(dirname) if os.path.splitext(x)[-1]=='.tiff']
    index = 0
    print(list)
    for file in list:
        name = 'IMG_'+str(index) + '.tiff'
        os.rename(os.path.join(dirname,file),os.path.join(dirname,name))
        index = index + 1


dngToTif()
delJPG()
#renameFiles()