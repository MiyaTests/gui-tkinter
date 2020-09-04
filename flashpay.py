# import the necessary packages
import tkinter as tki
import threading
import cv2
from imutils.video import VideoStream
import time
import sys
from view.home_screen import *
from constant import *


# use cases
class FlashPay:
    def __init__(self, vs, outputPath):
        # configure tkinter window
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None
        self.root = tki.Tk()
        self.root.attributes("-fullscreen", True)
        self.panel = None
        self.use_case = -1 # 
        self.fullScreenState = False
        self.root.bind("<Escape>", self.quitFullScreen)
        self.root.bind("<F11>", self.toggleFullScreen)

        # initialize state machine
        self.event_manager()

	# initialize thread  
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.state_manager, args=())
        self.thread.daemon = True
        self.thread.start()

	# set a callback to handle when the window is closed
        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def state_manager(self):
	# loop during each state
        while not self.stopEvent.is_set():
            if self.use_case == S1:
                state1(self)	
            elif self.use_case == S2:
                state2(self)
            elif self.use_case == S4:
                state4(self)
    
    def event_manager(self, btn=None):
        if   self.use_case == SI:
            action0(self)
            self.use_case = S0
        elif self.use_case == S0:
            if btn == "go_client":
                action1(self)
                self.use_case = S1
        elif self.use_case == S1:
            if btn == "snapshot":
                action2(self)
                self.use_case = S2
            if btn == "go_home":
                action5(self)
                self.use_case = S0
        elif self.use_case == S2:
            if btn == "checkout":
                action3(self)
                self.use_case = S3
            if btn == "repeat":
                action4(self)
                self.use_case = S1
            if btn == "go_home":
                action6(self)
                self.use_case = S0
        elif self.use_case == S3:
            if btn == "pay":
                action9(self)
                self.use_case = S4
            if btn == "cancel":
                action7(self)
                self.use_case = S0
        elif self.use_case == S4:
            action8(self)
            self.use_case = S0

    def onClose(self):
        # Terminate everything
        print("[INFO] closing...")
        self.stopEvent.set()
        vs.stream.release()
        self.root.destroy()
        sys.exit()

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.root.attributes("-fullscreen", self.fullScreenState)

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)


PICAMERA = False
output = "images"

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=PICAMERA).start()
time.sleep(2.0)

# start the app
pba = FlashPay(vs, output)
pba.root.mainloop()

