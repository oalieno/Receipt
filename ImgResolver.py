import os
import re
import hashlib
import logging as log
from PIL import Image,ImageEnhance
from ImgDBManager import ImgDBManager

class ImgResolver(object):
    def __init__(self):
        self.imgdbmanager = ImgDBManager()
        self.SHA = ""
        self.captcha = ""
    def Solve(self,image):
        self.SHA = hashlib.sha1(image).hexdigest()
        MEM = self.imgdbmanager.SearchID(self.SHA)
        if MEM != None:
            return MEM
        with open("image.jpeg",'w') as imagefile:
            imagefile.write(image) 
        #Enhance image
        img = Image.open("image.jpeg")
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.0)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(3.0)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(10.0)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(20.0)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(0.0)
        img.save("image.jpeg")
        #Enhance image
        self.captcha = os.popen("tesseract -l eng image.jpeg stdout").read().strip()
        log.debug("regex match : {}".format(re.match("\w{5}",self.captcha)))
        if len(self.captcha) == 5 and re.match("\w{5}",self.captcha):
            return self.captcha
        else:
            return None
    def Store(self):
        self.imgdbmanager.StoreData(self.SHA,self.captcha) 
