#!/usr/bin/env python

import Image
import os
#class Spreader(QtGui.QMainWindow):
#    def __init__(self):
#        super(Spreader, self).__init__()
        
        
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
def get_corner():
    corners = [1,2,3,4]
    while True:
        try:
            corner = int(raw_input("Which corner? \n(1 for top-left, 2 for top-right, 3 for bottom-left, and 4 for bottom-right):\n"))
            if corner in corners:
                return corner
        except ValueError:
            continue
        
def main():
    print("Enter relative or absolute paths.")
    overlay_watermark(raw_input("Watermark image path: "),raw_input("Input images folder: "),raw_input("Processed images folder: "))
            
if __name__ == "__main__":
    main()
