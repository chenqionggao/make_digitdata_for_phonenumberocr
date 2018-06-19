#-*- coding: utf-8 -*-

## change chinese word and edge constraints
import os
import cv2
import glob
import math
import random
import numpy as np
import os.path as osp
import multiprocessing as mp
import logging
from PIL import Image,ImageDraw,ImageFont 
import io
import sys
from scipy import misc

reload(sys)
sys.setdefaultencoding('utf-8')



resultImgsDir = resultpath

bgiDir = bgipath
bigbgiDir = bgipath2

gTtf= ttfpath


ttfSize = [25,30]


index = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9};

chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

def r(val):
    return int(np.random.random() * val)

def genTextString(counter):
    textStr = "";
    for idx in xrange(counter):
        textStr += chars[r(len(chars))]

    return textStr;

def make_paste_single(counter):
    bgis = glob.glob( osp.join(bgiDir,'*') )
    big_bgis = glob.glob( osp.join(bigbgiDir,'*') )
    
    base=random.randint(20,50)
    curcol=random.randint(10,30)
    
    curBgi = random.randint(0,len(bgis)-1)
    curbigBgi = random.randint(0,len(big_bgis)-1)
    bgi = bgis[curBgi]
    big_bgi = big_bgis[curbigBgi]
    
    num=""
    ##for certain size
    #data_shape1,data_shape2,channel=np.array(Image.open(bgi).convert('RGB')).shape
    ## for random size
    data_shape1 =random.randint(10,50)
    data_shape2 =random.randint(10,30)
    img=np.array(Image.open(big_bgi).convert('RGB').resize((260,60)))
    for i in range(counter):
        curBgi = random.randint(0,len(bgis)-1)
        bgi = bgis[curBgi]
        if data_shape1+curcol > 60 or base + data_shape2 > 260:
            return
        img[curcol: (data_shape1+curcol), base : (base + data_shape2),:]= np.array(Image.open(bgi).convert('RGB').resize((data_shape2,data_shape1)))
        #img[0: data_shape1, base : (base + data_shape2),:]= np.array(Image.open(bgi).convert('RGB').resize((data_shape2,data_shape1)))
        #img[(30-np.floor(data_shape1/2)): (30+np.floor(data_shape1/2)), base : base + data_shape2,:]= np.array(Image.open(bgi).convert('RGB'))
        base += data_shape2
        num = num+str((bgi.split("/")[6]).split("_")[0])
    print str(num)
    misc.imsave((resultImgsDir+str(num)+".jpg"),img)



if __name__ == '__main__':

    #the directory of text,which will be paste on the background images
    inter=40000 
    counter=11
    for i in range(inter):
        make_paste_single(counter)
