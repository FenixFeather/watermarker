#!/usr/bin/env python

import Image
import os
def find_pos(image, watermark, corner=4, padding=50):
    '''Return the coordinates the image should be pasted at'''
    width, height = image.size
    wWidth, wHeight = watermark.size
    if padding < 1:
        padding *= width
    padding = int(padding)
    cornerMapping = {
        1:(padding, padding),
        2:(width - (padding + wWidth), padding),
        3:(padding, height - (padding + wHeight)),
        4:(width - (padding + wWidth), height - (padding + wHeight))
    }
    return cornerMapping[corner]
    
def overlay_watermark(watermarkPath,inPath,outPath,corner=4,padding=50):
    '''Do all the work'''
    inPath += '/'
    outPath += '/'
    watermark = Image.open(watermarkPath)
    contents = os.listdir(inPath)
    for pic in contents:
        try:
            workImage = Image.open(os.path.join(inPath + pic))
            position = find_pos(workImage, watermark, corner, padding)
            workImage.paste(watermark,position,watermark)
            workImage.save(os.path.join(outPath + pic))
            print pic
        except:
            print("Error with {0}".format(pic))
            raise
        
def main():
    overlay_watermark("watermark.png","test","out")
            
if __name__ == "__main__":
    main()
