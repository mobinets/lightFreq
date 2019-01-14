#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2,os
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal, io
from PIL import Image
import xlrd
import xlwt
from xlutils.copy import copy

def threshold(img,type = 0,*thd):#0: otsu, 1: manu, 2: adaptive
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #转为灰度图
    if type == 1:
        img_thd = cv2.threshold(img_gray,thd,255,cv2.THRESH_BINARY)
    elif type == 2:
        img_thd = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    else :
        ret, img_thd = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return img_thd

def morphologyEx(img,type):#形态学
    kernel = np.ones((5, 5), np.uint8)
    if type == 'open':
        img_mor = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif type == 'close':
        img_mor = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    elif type == 'close+open' or 'open+close':
        img_c = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img_mor = cv2.morphologyEx(img_c, cv2.MORPH_OPEN, kernel)
    return img_mor

def findLightShape(img_original,img,type = 'rect'):
    img_cont = img.copy()
    img_cont, contours, hier1 = cv2.findContours(img_cont, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_mask = np.zeros(img_cont.shape, np.uint8)
    area = np.zeros(len(contours))
    for i, cnt in enumerate(contours):
        area[i] = cv2.contourArea(cnt)
    maxcnt = np.max(area)
    maxindex = np.where(area == maxcnt)
    if type == 'rect':
        x, y, w, h = cv2.boundingRect(contours[maxindex[0][0]])
        img_mask = cv2.rectangle(img_mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
        #plt.imshow(img_mask)
        #plt.show()
    elif type == 'irregular':
        img_mask = cv2.drawContours(img_mask, contours, maxindex[0][0], (255, 255, 255), -1, hierarchy=hier1,maxLevel=2)

    img_roi = cv2.bitwise_and(img_original,img_original, mask=img_mask)
    img_roi_gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
    #plt.imshow(img_roi_gray)
    #plt.show()
    return img_roi_gray

def extraction(img_shape, cal_type = 0):
    if img_shape.shape[0] < img_shape.shape[1]:
        rowsum = np.sum(img_shape, axis=1)
    else:
        rowsum = np.sum(img_shape, axis=0)
    pixel = img_shape
    pixel[pixel > 0] = 1
    pixelnum = np.sum(pixel, axis=1)
    rowsum = rowsum[rowsum > 0]
    pixelnum = pixelnum[pixelnum > 0]
    if cal_type == 0:
        lightsignal = rowsum.astype(float)
    elif cal_type ==1:
        lightsignal = rowsum / pixelnum
        lightsignal = lightsignal.astype(float)
    # 这里是用来截取照片中有效部分的,头和尾的干扰有时候比较大,去掉前1/8和后1/8再进行统计
    lightsignal = lightsignal[int(len(lightsignal) / 8):int(len(lightsignal) * 7/8)]
    lightsignal_odd = lightsignal[0:len(lightsignal):2]
    lightsignal_even = lightsignal[1:len(lightsignal):2]
    gain_odd = np.mean(lightsignal_odd)
    gain_even = np.mean(lightsignal_even)

    print("Odd:%s,Even:%s" % (gain_odd, gain_even))


    lightsignal[0:len(lightsignal):2] = lightsignal[0:len(lightsignal):2] / gain_odd
    lightsignal[1:len(lightsignal):2] = lightsignal[1:len(lightsignal):2] / gain_even


    print("lightsignal:%s" % lightsignal)



    xx = np.arange(1, len(lightsignal) + 1)
    p = np.polyfit(xx, lightsignal, 6)
    func = np.poly1d(p)
    lightsignal = lightsignal / func(xx)
    temp = lightsignal
    #lightsignal = temp[::-1]
    return lightsignal

def signalPro(lightsignal,CFs,dirname,j,sh):
    N = len(lightsignal)
    print(N)
    fs = 3024 * 34.97

    f, Pxx = signal.periodogram(lightsignal, fs, window=signal.get_window('blackman', N), nfft=N)
    amp = 20 * np.log10(np.clip(np.abs(Pxx), 1e-20, 1e100))
    sav = signal.savgol_filter(amp, 5, 2)
    sav_n = sav[200:len(sav) - 1000]

    maxF = f[np.where(sav_n == np.max(sav_n))[0][0] + 200]

    for i in range(len(f)):
        sh.write(i,(j-1)*2,f[i])
        sh.write(i,(j-1)*2+1, sav[i])

    plt.figure('lightsignal %d' % j)
    plt.plot(lightsignal)
    plt.xlabel('rows')
    plt.ylabel('mean value of each row')
    plt.savefig(dirname + '%d.png' % j)

    plt.figure('fft %d' % j)
    plt.plot(f, sav, 'r')
    plt.xlabel('frequency [Hz]')
    plt.ylabel('SNR')
    plt.text(30000, -120, 'CF = %f' % maxF, va='top', ha='center')
    plt.savefig(dirname + '%d.png' % j)
    # plt.show()
    plt.close()
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    CFs.append(maxF)
    return CFs
def main():

    lightsignal = np.array([])
    wbk = xlwt.Workbook()
    sh = wbk.add_sheet('sheet_1',cell_overwrite_ok=True)
    #待处理图片所在的文件名
    filename = 'C-40'
    #图片文件保存路径的上一级
    dirname = os.path.join('C:/Users/NGMI-08/Desktop/work/xin/', filename + '/')
   # excelFile = 'D:/work/'
    #li = ['0','15'.]
    #dirname = '/Users/carol/Desktop/work/vlc/hello714_30/'
    CFs = []
    for j in range(1,11):#十组数据
        lightsignal = np.array([])
        for i in range((j-1)*5,(j-1)*5+5):#每组5张照片
            #img = cv2.imread('1.tiff')
            imgname = str(i + 1) + '.tiff'
            imgPath = os.path.join(dirname, imgname)
            print(imgPath)
            #img = Image.open(imgPath)
            #img = img.rotate(-90,expand=tr)
            img = cv2.imread(imgPath)
            print(img.shape)
            img_thd = threshold(img)
            img_mor = morphologyEx(img_thd,'close')
            img_shape = findLightShape(img, img_mor, type='rect')
            lightsignal = np.append(lightsignal,extraction(img_shape))

        CFs = signalPro(lightsignal,CFs,dirname,j,sh)

    print(CFs)

    wbk.save(os.path.join(dirname,filename+'.xls'))

    io.savemat(dirname+filename+'CF.mat', {'CFs_A_ir':CFs})

if __name__ == '__main__':
    main()
