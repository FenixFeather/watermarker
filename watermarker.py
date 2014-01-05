#!/usr/bin/env python

import Image
import os
import sys
from PyQt4 import QtGui, QtCore

class Watermarker(QtGui.QMainWindow):
    def __init__(self):
        super(Watermarker, self).__init__()
        
        self.initUI()
        
        QtCore.QObject.connect(QtGui.qApp, QtCore.SIGNAL('notify(PyQt_PyObject)'), self.notify)
        
    def center(self):
        '''Center the window'''
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def initUI(self):
        '''Initialize the UI'''
        self.watermarker = Settings()
        self.setCentralWidget(self.watermarker)
        
        #Actions
        exitAction = QtGui.QAction(QtGui.QIcon('img/application-exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        #Statusbar
        self.statusBar()
        
        #Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        
        fileMenu.addAction(exitAction)
        
        #Window Stuff
        self.setWindowIcon(QtGui.QIcon('img/image.png'))
#        self.resize(650,400)
        self.center()
        self.setWindowTitle('Watermarker')    
        self.show()
        
    def notify(self, message):
        self.statusBar().showMessage(message)
        
class Settings(QtGui.QWidget):
    def __init__(self):
        super(Settings, self).__init__()
        self.home = os.path.expanduser('~')
        
        self.watermark = ""
        self.inputFolder = ""
        self.outputFolder = ""
        self.corner = 1
        self.padding = 50
        
        self.initUI()
    
    def initUI(self):
        validator = QtGui.QIntValidator(0,9999999)
        grid = QtGui.QGridLayout()
        
        #Watermark Edit
        self.watermarkLabel = QtGui.QLabel('Watermark image')
        
        self.watermarkEdit = QtGui.QLineEdit()
#        self.watermarkEdit.setValidator(validator)
        self.watermarkEdit.setText(self.home)
        
        self.watermarkButton = QtGui.QPushButton('Browse')
        
        self.watermarkEdit.textChanged[str].connect(self.change)
        self.watermarkButton.clicked.connect(self.get_watermark)
        
        #Input folder edit
        self.inputFolderLabel = QtGui.QLabel('Input folder')
        
        self.inputFolderEdit = QtGui.QLineEdit()
        self.inputFolderEdit.setText(self.home)
        
        self.inputFolderButton = QtGui.QPushButton('Browse')
        
        self.inputFolderEdit.textChanged[str].connect(self.change)
        self.inputFolderButton.clicked.connect(self.get_folder)
        
        #Output folder edit
        self.outputFolderLabel = QtGui.QLabel('Output folder')
        
        self.outputFolderEdit = QtGui.QLineEdit()
        self.outputFolderEdit.setText(self.home)
        
        self.outputFolderButton = QtGui.QPushButton('Browse')
        
        self.outputFolderEdit.textChanged[str].connect(self.change)
        self.outputFolderButton.clicked.connect(self.get_folder)
        
        #Get corner
        self.cornerDict = {"Top Left":1 , "Top Right":2 , "Bottom Left":3 , "Bottom Right":4 }
        self.comboLabel = QtGui.QLabel('Corner')
        self.combo = QtGui.QComboBox()
        for corner in self.cornerDict.keys():
            self.combo.addItem(corner)
        self.combo.activated[str].connect(self.change)
        
        #Get padding
        self.paddingLabel = QtGui.QLabel('Padding (pixels or decimal%)')
        
        self.paddingEdit = QtGui.QLineEdit()
        self.paddingEdit.setText('50')
        self.paddingEdit.setValidator(validator)
        self.paddingEdit.textChanged[str].connect(self.change)
        
        #GO
        self.goButton = QtGui.QPushButton('Watermark!')
        self.goButton.clicked.connect(self.process)
        
        #Grid
        grid.addWidget(self.watermarkLabel, 1, 0); grid.addWidget(self.watermarkEdit, 1, 1); grid.addWidget(self.watermarkButton, 1, 2)
        grid.addWidget(self.inputFolderLabel, 2, 0); grid.addWidget(self.inputFolderEdit, 2, 1); grid.addWidget(self.inputFolderButton, 2, 2)
        grid.addWidget(self.outputFolderLabel, 3, 0); grid.addWidget(self.outputFolderEdit, 3, 1); grid.addWidget(self.outputFolderButton, 3, 2)
        grid.addWidget(self.comboLabel, 4, 0); grid.addWidget(self.combo, 4, 1)
        grid.addWidget(self.paddingLabel, 5, 0); grid.addWidget(self.paddingEdit, 5, 1)
        grid.addWidget(self.goButton, 6, 2)
        
        self.setLayout(grid)
        
    def get_watermark(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select Watermark', self.home)
        self.watermarkEdit.setText(fname)
        
    def get_folder(self):
        sender = self.sender()
        fname = QtGui.QFileDialog.getExistingDirectory(self,'Select Folder', self.home)
        if sender is self.inputFolderButton:
            self.inputFolderEdit.setText(fname)
        elif sender is self.outputFolderButton:
            self.outputFolderEdit.setText(fname)
        
    def change(self, s):
        sender = self.sender()
        self.watermark = str(self.watermarkEdit.text())
        self.inputFolder = str(self.inputFolderEdit.text()) + '/'
        self.outputFolder = str(self.outputFolderEdit.text()) + '/'
        if sender is self.combo:
            self.corner = self.cornerDict[str(s)]
        self.padding = int(self.paddingEdit.text())
        
    def process(self):
        print(self.watermark)
        watermark = Image.open(self.watermark)
        contents = os.listdir(self.inputFolder)
        QtGui.qApp.emit(QtCore.SIGNAL("notify(PyQt_PyObject)"), "Working...")
        for pic in contents:
            try:
                workImage = Image.open(os.path.join(self.inputFolder + pic))
                position = find_pos(workImage, watermark, self.corner, self.padding)
                workImage.paste(watermark,position,watermark)
                workImage.save(os.path.join(self.outputFolder + pic))
                print pic
            except:
                print("Error with {0}".format(pic))
                raise
        QtGui.qApp.emit(QtCore.SIGNAL("notify(PyQt_PyObject)"), "Done!")
        
        
                
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
            
def get_padding():
    while True:
        try:
            padding = raw_input("Enter padding (fraction or pixel value): ")
            if int(float(padding)) == float(padding):
                return abs(int(padding))
            return abs(float(padding))
        except ValueError:
            print("Invalid input.")
            continue
            
def main():
    print("Enter relative or absolute paths.")
    overlay_watermark(
        raw_input("Watermark image path: "),
        raw_input("Input images folder: "),
        raw_input("Processed images folder: "),
        get_corner(),
        get_padding()
    )

def mainw():
    app = QtGui.QApplication(sys.argv)
    ex = Watermarker()
    sys.exit(app.exec_())  
            
if __name__ == "__main__":
    mainw()
