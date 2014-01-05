#!/usr/bin/env python

import Image
import os
def find_best_pos():
    pass
    
def overlay_watermark(watermarkPath,inPath,outPath):
    watermark = Image.open(watermarkPath)
    contents = os.listdir(inPath)
    for pic in contents:
        try:
            workimage = Image.open(os.path.join(inPath + pic))
            width, height = workimage.size
            width = width - 530
            height = height - 423
            workimage.paste(watermark,(width,height),watermark)
            out = workimage
            out.save("out/" + pic)
            print pic
        except:
            print("Error with {0}".format(pic))
        
def main():
    pass
            
if __name__ == "__main__":
    main()
