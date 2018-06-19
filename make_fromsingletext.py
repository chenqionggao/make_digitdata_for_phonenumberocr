#-*- coding: utf-8 -*-

## change chinese word and edge constraints
import os
import cv2
import glob
import math
import random
import numpy as np
import os.path as osp
from xml.dom.minidom import Document
import multiprocessing as mp
import logging
from PIL import Image,ImageDraw,ImageFont 
import io
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#resultImgsDir: the directory of resulting images
resultImgsDir = resultpath



#bgiDIr: the directory of background images
bgiDir = bgipath

#gTtf:the global variable of ttf files path
gTtf= ttfpath


#ttfSize: the set of sizes of font, which will be used to create the text

ttfSize = [28,30,35]

index = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9};

#with alpha data
#chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X","Y", "Z"];
#without alpha data
chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

def r(val):
    return int(np.random.random() * val)

def genTextString(counter):
    textStr = "";
    for idx in xrange(counter):
        textStr += chars[r(len(chars))]

    return textStr;

def _paste(bgi,draw,ttf,size,curRow,curCol,curText,cols):

    ttfont = ImageFont.truetype(ttf,size) 
    #curText = curText.split(':')
    #print curText.decode("UTF-8").split()
    #curText = curText[random.randint(0,len(curText.decode("UTF-8"))-1 )]
    maxNumText = int(math.floor((cols-curCol)/size))
    #string = curText[:maxNumText].strip()
    string = curText.decode("UTF-8")
    numAscii = sum([1 for i in string if 0<ord(i)<255])
    numText=1
    stringsize =ttfont.getsize(string) 
    print string,stringsize,curRow,curCol,curRow+stringsize[0],curCol+stringsize[1]
    if string!="" and numText >= 1 and curCol+stringsize[0] < 200 and curRow+stringsize[1] < 60:
        #random the RGB values
        bgr = [random.randint(0,50) for i in range(3)]
        draw.text((curCol,curRow),string, tuple(bgr), font=ttfont) 
    else:
        
        string = ''
        
    '''width height '''
    width,height = ttfont.getsize(string)
    
     #=====   
#    bgi = np.array(bgi,dtype = np.uint8)
#    cv2.rectangle(bgi,(curCol,curRow),(curCol+width,curRow+height),(0,0,0),1)
#    bgi = Image.fromarray(bgi)

    return bgi,string,width,height



def paste(imgname,bgi,text,ttf,ttfRandom):

    #bgi = cv2.imread(bgi)
    bgi = np.array(Image.open(bgi).resize((200,60)))

    if(len(bgi.shape)==2):
        depth=1
        rows,cols = bgi.shape
    else:
        rows,cols,depth = bgi.shape
    
    bgi = Image.fromarray(bgi)
    draw = ImageDraw.Draw(bgi)

    #certain position for certain size of pic 
    curRow = random.randint(10,30)
    #curRow += curRowInter
    curTtfSize = random.randint(0,len(ttfRandom)-1)

   #certain position for certain size of pic
    curCol = random.randint(10,50)
    
    bgi,string,width,height = _paste(bgi,draw,ttf,ttfRandom[curTtfSize],curRow,curCol,curText,cols)
    if string != '' :           
        #cur intervel
        curRowInter = random.randint(2,7)
        #cur ttf size
        curTtfSize = random.randint(0,len(ttfRandom)-1)
        
        return np.array(bgi)
    else:
        return np.zeros((np.array(bgi).shape))
def handle(text):
    
    ind, text = text
    #pid
    pid = os.getpid()
    #background image
    bgis = glob.glob( osp.join(bgiDir,'*') )
    #select one background image
    curBgi = random.randint(0,len(bgis)-1)
    bgi = bgis[curBgi]

    #ttf
    ttfs = glob.glob(osp.join(gTtf,'*.ttf'))
    curTtf = random.randint(0,len(ttfs)-1)    
    ttf = ttfs[curTtf]
   
    #ttf size random
    ttfRandom = [1]+[ random.randint(0,1) for i in range(len(ttfSize)-1)] 
    ttfRandom = [ran*size for ran,size in zip(ttfRandom, ttfSize)] 
    ttfRandom = [i for i in ttfRandom if i != 0] 
    imgname = '{}_{}_{}.jpg'.format(ind,pid,curTtf)
    bgi =  paste(imgname,bgi,text,ttf,ttfRandom)
   
    if text != "" and np.sum(np.array(bgi)) != 0:
        Image.fromarray(bgi).save(osp.join('data',text+".jpg"))
    
    return

if __name__ == '__main__':

    #the directory of text,which will be paste on the background images
    inter=20000
    for i in range(inter):
        try:
			total=genTextString(11)
			handle([i,total])
        except Exception as e:
            print e
