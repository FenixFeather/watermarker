#!/usr/bin/env python
import Tkinter as tk
import ttk
import tkFileDialog
import os
import Image

class Application(ttk.Frame):              
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.style = ttk.Style()
        self.style.theme_use(self.style.theme_names()[0])
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        #Variables
        self.watermarkPath = tk.StringVar()
        self.inputPath = tk.StringVar()
        self.outputPath = tk.StringVar()
        self.corner = tk.StringVar()
        self.padding = tk.StringVar()
        
        self.cornerDict = {"Top Left":1 , "Top Right":2 , "Bottom Left":3 , "Bottom Right":4 }
        self.corner.set(self.cornerDict.keys()[0])
        
        self.home = os.path.expanduser('~')
    
        #Labels
        labels = ["Watermark Image", "Input Folder","Output Folder","Corner","Padding"]
        for i,label in enumerate(labels):
            labelWidget = ttk.Label(self, text=label)
            labelWidget.grid(column=0,row=i,pady=5,padx=5)
            
        #Line entries
        self.watermarkEdit = ttk.Entry(self, textvariable=self.watermarkPath, width=50)
        self.watermarkEdit.grid(column=1,row=0)
        
        self.inputEdit = ttk.Entry(self, textvariable=self.inputPath, width=50)
        self.inputEdit.grid(column=1,row=1)
        
        self.outputEdit = ttk.Entry(self, textvariable=self.outputPath, width=50)
        self.outputEdit.grid(column=1,row=2,padx=2.5)
        
        self.paddingEdit = ttk.Entry(self, textvariable=self.padding, width=50)
        self.paddingEdit.grid(column=1,row=4)
        
        #Option menu
        self.cornerOptions = ttk.OptionMenu(self, self.corner, self.cornerDict.keys()[0],*tuple(self.cornerDict.keys()))
        self.cornerOptions.grid(column=1,row=3)
        
        #Buttons
        self.browseWatermark = ttk.Button(self,text='Browse',command=self.get_file)
        self.browseWatermark.grid(column=2,row=0, padx=2.5)
        
        self.browseInput = ttk.Button(self, text='Browse', command = lambda: self.get_directory(self.inputPath))
        self.browseInput.grid(column=2,row=1, padx=2.5)
        
        self.browseOutput = ttk.Button(self, text='Browse',command=lambda: self.get_directory(self.outputPath))
        self.browseOutput.grid(column=2,row=2, padx=2.5)
        
        self.goButton = ttk.Button(self, text='Watermark!', command=self.go)
        self.goButton.grid(column=1,row=5,pady=5, padx=2.5)
        
#        self.setPadding()
        
    def setPadding(self):
        rows, columns = self.goButton.grid_size()
        for row in range(rows):
            self.goButton.rowconfigure(row,pad=5)
        for column in range(columns):
            self.goButton.columnconfigure(column,pad=5)
        
    def get_directory(self, tvar):
        tvar.set(tkFileDialog.askdirectory(initialdir=self.home,parent=self,title="Select Directory"))
        
    def get_file(self):
        self.watermarkPath.set(tkFileDialog.askopenfilename(parent=self,initialdir=self.home,title="Select Image File"))
    
    def go(self):
        watermark = Image.open(self.watermarkPath.get())
        self.inputFolder = self.inputPath.get() + '/'
        self.outputFolder = self.outputPath.get() + '/'
        contents = os.listdir(self.inputFolder)
        for pic in contents:
            try:
                workImage = Image.open(os.path.join(self.inputFolder + pic))
                position = find_pos(workImage, watermark, self.cornerDict[self.corner.get()], get_padding(self.padding.get()))
                workImage.paste(watermark,position,watermark)
                workImage.save(os.path.join(self.outputFolder + pic))
                print pic
            except:
                print("Error with {0}".format(pic))
                raise
                
def get_padding(padding):
    while True:
        try:
            if int(float(padding)) == float(padding):
                return abs(int(padding))
            return abs(float(padding))
        except ValueError:
            return 50
                            
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
        
if __name__ == "__main__":
    app = Application()
    app.master.title('WatermarkerTk')
    app.mainloop() 
