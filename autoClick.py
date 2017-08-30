from pymouse import *
from PIL import Image
from PIL import ImageGrab
import time
import os
import argparse  # Command line parsing



# im0 =ImageGrab.grab((300, 100, 1400, 600))  
# im0 =  im0.convert('RGB')
# im0.save('imgHis/m1.jpeg')
# m = PyMouse() 
# m.move(100,400)

def parseArgs():
    parser = argparse.ArgumentParser()
    
    globalArgs = parser.add_argument_group('Global options')
    globalArgs.add_argument('--subDir', type=str, help='dir of you movieSub')
    globalArgs.add_argument('--mode',   type=str,
                                        choices=['mergevocab','convert','mergesub'],
                                        default='mergesub'
                            )
    globalArgs.add_argument('--tag', type=str, default='train')
    globalArgs.add_argument('--fileType', type=str, default='ass,sub,txt')
    globalArgs.add_argument('--sourceCode', type=str, default='utf-8')
    globalArgs.add_argument('--splitCode', type=str, default='-->')
    globalArgs.add_argument('--minVocab', type=int, default=1)
    globalArgs.add_argument('--splitWord', type=str, default='on')
    return parser.parse_args()

def getGray(image_file):
    tmpls=[]
    for h in range(0,  image_file.size[1]):#h
        for w in range(0, image_file.size[0]):#w
            tmpls.append( image_file.getpixel((w,h))  )     
    return tmpls
 
def os_exec(cCMD):
    os.system(cCMD)

def getAvg(ls):#获取平均灰度值
  return sum(ls)/len(ls)
 
def getMH(a,b):#比较100个字符有几个字符相同
    dist = 0;
    for i in range(0,len(a)):
        if a[i]==b[i]:
            dist=dist+1
    return round(100*dist/len(a),2)
 
def getImgHash(fileName,type):
    if type == 'File':
        image_file = Image.open(fileName) # 打开
    else:
        image_file =  fileName

    #image_file=image_file.resize((24, 24))#重置图片大小24px X 24px
    image_file=image_file.convert("L")#转256灰度图
    Grayls=getGray(image_file)#灰度集合
    avg=getAvg(Grayls)#灰度平均值
    bitls=''#接收获取0或1
    #除去变宽1px遍历像素
    for h in range(1,  image_file.size[1]-1):#h
        for w in range(1, image_file.size[0]-1):#w
            if image_file.getpixel((w,h))>=avg:#像素的值比较平均值 大于记为1 小于记为0
                bitls=bitls+'1'
            else:
                bitls=bitls+'0'
    return bitls


'''         
   m2 = hashlib.md5()   
   m2.update(bitls)
   print m2.hexdigest(),bitls
   return m2.hexdigest()
'''
 
def checkImage(tag,fileName,fileNameBase):

    b=getImgHash(fileName,False)
    compare=getMH(imageHashBase[tag],b)
    print('   相似度:' + str(compare) + '%')
    return compare


def checkArea(tag,r,x1,y1,x2,y2):
    print(tag + ':\t'+str(r))
    fileBaseName = os.path.join(baseDir , tag+'.base.'+'jpeg')
    fileName = os.path.join(hisDir ,'{}.{}.jpeg'.format(tag,str(r))) 
    im0 =ImageGrab.grab((x1, y1, x2, y2))
    im0 =  im0.convert('RGB')

    im0=im0.resize((24, 24))#重置图片大小24px X 24px

    #im0.save(fileName)
    if not os.path.exists(fileBaseName):
        im0.save(fileBaseName)
        imageHashBase[tag] = getImgHash(im0,'Memory')
        #imageHashBase[tag] = getImgHash(fileBaseName,'File')
    
    if not tag in imageHashBase:
        imageHashBase[tag] = getImgHash(fileBaseName,'File')

    imageSim = checkImage(tag,im0,fileBaseName)
    if imageSim >= 97:
        print('   click')

def cleanHisImage(r):
    fileList = [os.path.join(hisDir, f) for f in os.listdir(hisDir)]
    for f in fileList:
        fSplit = f.replace(hisDir,'').split('.')
        if len(fSplit) ==3:
            fNum = f.split('.')[1]
            if int(fNum)>r or int(fNum)<=r - 10:
                os.remove(f)


if __name__ == "__main__":
    rootDir = '/shareDisk/autoTest'
    hisDir = os.path.join(rootDir,'imgHis')
    baseDir =  os.path.join(rootDir,'imgBase')

    args = parseArgs()
    imageHashBase ={}

    r = 0
    while True: 
        r += 1
        checkArea('tag1',r,100,100,300,200)
        checkArea('tag2',r,100,100,200,200)
        time.sleep(3)
        if r%10 == 1:
            cleanHisImage(r)