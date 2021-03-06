#!/usr/local/bin/python
#!/usr/bin/env python

# always seem to need this
from __future__ import print_function
import string;print(string.__file__)
import sys

# This gets the Qt stuff
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
from PIL import Image
# This is our window from QtCreator
from threading import Thread
import threading
import picamera
import time
import datetime
import mainwindow_auto
import secondwindow_auto
import dropbox
import os
from os.path import exists
import DropboxAPI
import strandtest
from neopixel import *
import RPi.GPIO as GPIO

LED_COUNT      = 44      # Number of LED pixels was 120.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

#This token is attirbuted to your account.
#You can change this to upload to different drop box account
token = 'iXbb2YaVfCAAAAAAAAAADOLjMyg5FGJw6coQnbpyLG7-mqGFG0SGZR6I1L722gzd'             

#white function turns led's white    
def white(strip):
        strip.show()
        for i in range(0,46):
                strip.setPixelColor(i,Color(255,255,255))
        strip.show()
        time.sleep(1)

#clear function turns led's off
def clear(strip):
	#time.sleep(5)
        strip.show()
        for i in range(0,46):
                strip.setPixelColor(i,Color(0,0,0))
	
        strip.show()
        time.sleep(1)

#theaterChase function keeps the LED's rotating
def theaterChase(strip, color, wait_ms=100, iterations=1):
	"""Movie theater light style chaser animation."""
	#for j in range(iterations):
	for q in range(3):
		for i in range(0, strip.numPixels(), 3):
			strip.setPixelColor(i+q, color)
		strip.show()
		time.sleep(wait_ms/1000.0)
		for i in range(0, strip.numPixels(), 3):
			strip.setPixelColor(i+q, 0)
#This thread keeps the LED's running while GUI is active
class myThread(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.strip  = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP) 
                self.strip.begin()
                self.daemon = True
                self.pause = False
                self.state = threading.Condition()
	        self.begining = True
        def run(self):
                while self.begining is True:
                        while self.pause is False:
                                theaterChase(self.strip, Color(240,70,1))
        def pause(self):
                self.pause = True
	def destroy(self):
		self.begining = False
		self.pause = True
		
        def strat(self):
                self.pause = False

#This window allows you to preview your pictures/upload/re-take
class PreviewWindow(QMainWindow, secondwindow_auto.Ui_SecondWindow):
    def __init__(self,parent = None):
        super(PreviewWindow,self).__init__(parent)
        self.setupUi(self)
        self.partnerwindow = parent
        self.filename = 'default'
        self.logo = 'default'
        self.pic = PyQt5.QtWidgets.QLabel(self)
        self.Loadbutton.clicked.connect(lambda: self.handleimage())
        self.Exitbutton.clicked.connect(lambda: self.close())
        self.Retakebutton.clicked.connect(lambda: self.retake())
        self.eebutton.clicked.connect(lambda: self.pressedeebutton())
        self.Uploadbutton.clicked.connect(lambda: self.pressedupload())

    def recieve_logo(self,item):
        self.logo = item
    def recieve_filename(self,item):
        self.filename = item
    def pressedeebutton(self):
	
        sys.exit()
    def pressedupload(self):
        DropboxAPI.upload(token, self.filename)
        dbx = dropbox.Dropbox(token)
	self.hide()
    def close(self):
        self.pic.clear()
        self.hide()
        
    def retake(self):
        os.remove(os.path.expanduser('/home/pi/Desktop/Picture/' + self.filename))
        self.hide()
    def handleimage(self):
        print(self.geometry().width())
        print(self.geometry().height())
        
        if self.logo.lower() != 'default':
            mimage = Image.open(os.path.expanduser('/home/pi/Desktop/Picture/' + self.filename))
            limage = Image.open(self.logo)

            wsize =  int(min(mimage.size[0],mimage.size[1]) * 0.25)
            wpercent = (wsize/float(limage.size[0]))
            hsize = int((float(limage.size[1]) * float(wpercent)))

            simage = limage.resize((wsize,hsize), Image.ANTIALIAS)
            mbox = mimage.getbbox()
            sbox = simage.getbbox()

            box = (mbox[2] - sbox[2], mbox[3] - sbox[3])
            mimage.paste(simage,box)
            mimage.save(os.path.expanduser('/home/pi/Desktop/Picture/' + self.filename))
        
        self.pic.setScaledContents(True)
        self.pic.setPixmap(PyQt5.QtGui.QPixmap(os.path.expanduser('/home/pi/Desktop/Picture/' + self.filename)))
        self.pic.installEventFilter(self)
        self.pic.setGeometry(self.geometry().height()/2,self.geometry().width()/10,240,340)
        self.pic.show()
    
       
#main window allows for you to 
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # gets defined in the UI file
        
        # Hooks for the buttons
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        self.strip.begin()
	
        self.thread1 = myThread()
        self.thread1.start()
        self.resx = 320  # default x resolution
        self.resy = 240  # default y resolution was at 240
        self.firstpicturepath = 'default'
        self.secondpicturepath = 'default'
        self.thirdpicturepath = 'default'
        self.pngpath = 'default'
        self.delay = 3
        self.Flash = 'OFF'
        self.partnerwindow = PreviewWindow(self)
        self.cameraStart.clicked.connect(lambda: self.pressedpicbutton())
        self.OverlayButton.clicked.connect(lambda: self.pressedbrowsebutton())
        self.exitButton.clicked.connect(lambda: self.emergencybutton())
        self.flash.clicked.connect(lambda: self.flashcall())
    	
    def flashcall(self):
        if self.Flash == 'OFF':
            self.Flash = 'ON'
            self.flash.setText('ON')
        else:
            self.Flash = 'OFF'
            self.flash.setText('OFF')
        print(self.Flash)
    def emergencybutton(self):
	self.thread1.destroy()
	self.thread1.join()
	clear(self.strip)
	print('sup')
        sys.exit()
    def pressedbrowsebutton(self):
        filename = QFileDialog.getOpenFileName(self, "Open Image", "/home", "Images (*.png *.jpg *.PNG *.JPG)")
        self.partnerwindow.recieve_logo(filename[0])
    def pictureprompt(self,value):
	    print('here')
            with picamera.PiCamera() as camera:
                    camera.resolution = (self.resx, self.resy)
                    camera.framerate = 24
                    camera.start_preview()
                    time.sleep(self.delay)
                    today = str(datetime.datetime.today())
                    if value == 1:
                            self.firstpicturepath = today[:19] + '.jpg'            
                            camera.capture(self.firstpicturepath)
                    elif value == 2:
                            self.secondpicturepath = today[:19] + '.jpg'            
                            camera.capture(self.secondpicturepath)
                    else:
                            self.thirdpicturepath = today[:19] + '.jpg'            
                            camera.capture(self.thirdpicturepath)
                    camera.stop_preview()
                     
    def pressedpicbutton(self):
        self.thread1.destroy()
	self.thread1.join()
	
        if self.Flash == 'ON':
		
		white(self.strip)
		white(self.strip)


	else:
		
		clear(self.strip)
		clear(self.strip)
		
        
        self.pictureprompt(1)

        #prompt
        
        

        self.pictureprompt(2)

        #prompt

        self.pictureprompt(3)

        list_image = [self.firstpicturepath,self.secondpicturepath,self.thirdpicturepath]
        list_image = map(Image.open,[self.firstpicturepath,self.secondpicturepath,self.thirdpicturepath])
        widths, heights = zip(*(i.size for i in list_image))
        
        total_width = max(widths)
        max_height = sum(heights)
        
        new_image  = Image.new('RGB',(total_width,max_height))
        y_offset = 0
        x_offset = 0
        for elem in list_image:
                print(elem)
                new_image.paste(elem,(0,y_offset))
                y_offset += elem.size[1]

            
            
        today = str(datetime.datetime.today())
        name = today[:19] + '.jpg'
        new_image.save(os.path.expanduser('/home/pi/Desktop/Picture/' + name))
            
        os.remove(self.firstpicturepath)
        os.remove(self.secondpicturepath)
        os.remove(self.thirdpicturepath)
            
        self.thread1.strat() 
        self.partnerwindow.recieve_filename(name)
        new_image.close()
        self.partnerwindow.setGeometry(10,10,1080,780)
        self.partnerwindow.show()
        self.partnerwindow.showFullScreen()
	self.thread1 = myThread()
        self.thread1.start()
              
          
def main():

    if not os.path.exists(os.path.expanduser('/home/pi/Desktop/Picture/')):
        os.makedirs(os.path.expanduser('/home/pi/Desktop/Picture/'))
        print('Hello')    
    with picamera.PiCamera() as camera:
	camera.start_preview()
	time.sleep(1)
	camera.stop_preview()
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())
    


# python bit to figure how who started This
if __name__ == "__main__":
    main()
