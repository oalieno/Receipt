import os
import logging as log
from PIL import Image,ImageEnhance

class ImgResolver(object):
    def __init__(self):
        pass
    def solve(self,image):
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
        captcha = os.popen("tesseract -l eng image.jpeg stdout").read()
        return captcha.strip()
