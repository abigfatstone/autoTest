from pymouse import *
from PIL import Image
from PIL import ImageGrab
import time
import os
import argparse  # Command line parsing
import random


# im0 =ImageGrab.grab((300, 100, 1400, 600))  
# im0 =  im0.convert('RGB')
# im0.save('imgHis/m1.jpeg')
# m = PyMouse() 
# m.move(100,400)

def parseArgs():
    parser = argparse.ArgumentParser()
    
    globalArgs = parser.add_argument_group('Global options')
    globalArgs.add_argument('--rootDir', type=str, default = '/shareDisk/autoTest' ,help='dir of you movieSub')
    globalArgs.add_argument('--mode', type=str,choices=['ghost','exp','god'],default='ghost')
    globalArgs.add_argument('--user', type=str,choices=['master','slaver'],default='ghost')
    globalArgs.add_argument('--tag', type=str, default='train')
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
    # print('   相似度:' + str(compare) + '%')
    return compare

def clickScreen(x1Random,y1Random):
    m.click(x1Random + random.randint(3,6),y1Random + random.randint(3,6),1)
    print('   move mouse to:' + str(x1Random + random.randint(3,6)) +','+ str(y1Random + random.randint(3,6)))

def checkArea(tag,r,minSim):

    fileBaseName = os.path.join(baseDir , tag+'.base.'+'jpeg')
    fileName = os.path.join(hisDir ,'{}.{}.jpeg'.format(tag,str(r)))
    x1 = int(imageSize[tag].split(',')[0].strip())
    y1 = int(imageSize[tag].split(',')[1].strip())
    x2 = int(imageSize[tag].split(',')[2].strip())
    y2 = int(imageSize[tag].split(',')[3].strip())

    clickX1 = int(imageSize[tag].split(',')[4].strip())
    clickY1 = int(imageSize[tag].split(',')[5].strip())
    clickX2 = int(imageSize[tag].split(',')[6].strip())
    clickY2 = int(imageSize[tag].split(',')[7].strip())

    im0 =ImageGrab.grab((x1, y1, x2, y2))
    im0 =  im0.convert('RGB')

    #im0=im0.resize((24, 24))#重置图片大小24px X 24px
    #im0.save(fileName)

    if not os.path.exists(fileBaseName):
        im0.save(fileBaseName)
        imageHashBase[tag] = getImgHash(im0,'Memory')
    
    if not tag in imageHashBase:
        imageHashBase[tag] = getImgHash(fileBaseName,'File')
    

    imageSim = checkImage(tag,im0,fileBaseName)
    if imageSim >= minSim:
        print(tag + ':\t'+str(r) +'\t相似度:' + str(imageSim) + '%')
        x1Random = random.randint(clickX1 + 1, clickX2 - 1)
        y1Random = random.randint(clickY1 + 1, clickY2 - 1) 

        for i in range(random.randint(2,4)):    
            clickScreen(x1Random,y1Random)
        
        if tag =='success.master' or tag =='success.slaver' :
            for i in range(random.randint(2,4)):   
                print(" click agagin")
                time.sleep(random.randint(1,30)/10)
                x1Random = random.randint(99 + 1, 999 - 1)
                y1Random = random.randint(650 + 1, 750 - 1) 
                clickScreen(x1Random,y1Random)

def loadSize():
    f = open(os.path.join(rootDir, 'size.conf'),'r')
    for line in f:
        imageSize[line.split(':')[0]]=line.split(':')[1]

def cleanHisImage(r):
    fileList = [os.path.join(hisDir, f) for f in os.listdir(hisDir)]
    for f in fileList:
        fSplit = f.replace(hisDir,'').split('.')
        if len(fSplit) ==3:
            fNum = f.split('.')[1]
            if int(fNum)>r or int(fNum)<=r - 10:
                os.remove(f)
def subGod():
    pass

def subExp():
    pass

def subSlaverGhost():
    checkArea('prepare.slaver',r,90)
    checkArea('teamSlave.slaver',r,90)
    checkArea('success.slaver',r,90)

def subMasterGhost():
    checkArea('prepare.master',r,90)
    checkArea('startFight.master',r,90)
    checkArea('startTeam.master',r,90)
    checkArea('success.master',r,90)

if __name__ == "__main__":

    args = parseArgs()
    rootDir = args.rootDir
    hisDir = os.path.join(rootDir,'imgHis')
    baseDir =  os.path.join(rootDir,'imgBase')
    m = PyMouse() 

    imageHashBase ={}
    imageSize = {}

    r = 0
    loadSize()

    while True: 
        r += 1
        loadSize()
        if args.mode == 'ghost' and args.user == 'master':
            subMasterGhost()
        elif args.mode == 'ghost' and args.user == 'slaver':
            subSlaverGhost()    
        elif args.mode == 'exp':
            subGod()            
        elif args.mode == 'god':
            subGod()   

        time.sleep(random.randint(1,50)/10)
        if r%10 == 1:
            cleanHisImage(r)