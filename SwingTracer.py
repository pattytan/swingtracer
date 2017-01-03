import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
import imutils
import cv2
import os.path


###############################################################################
pygame.init()

width = 1100
height = 700
screen = pygame.display.set_mode((width, height), RESIZABLE)
pygame.display.set_caption("Swing-Tracer 1.12")
sreen1 = pygame.display.get_surface()


# TEXTS #######################################################################
black = (40,40,40)
grassGreen = (109,192,102)
red = (183, 10, 10)

fontObj = pygame.font.Font("fonts/big_noodle_titling_oblique.ttf", 140)
titleSurfaceObj = fontObj.render("Swing-Tracer", True, black)
titleRectObj = titleSurfaceObj.get_rect()
titleRectObj.center = (width//2, height//2-40)

fontObj = pygame.font.Font("fonts/big_noodle_titling.ttf", 40)
SubSurfaceObj = fontObj.render("v 1.12", True, grassGreen)
SubRectObj = SubSurfaceObj.get_rect()
SubRectObj.center = (width//2, height//2+50)

BackSurfaceObj = fontObj.render("Back", True, grassGreen)
BackRectObj = BackSurfaceObj.get_rect()
BackRectObj.center = (width//18, height//18)

GoodSwingSurfaceObj = fontObj.render("Good", True, grassGreen)
GoodSwingRectObj = GoodSwingSurfaceObj.get_rect()
GoodSwingRectObj.center = (width - width//10, height -height//5)

AboveSurfaceObj = fontObj.render("Above Plane", True, red)
AboveRectObj = AboveSurfaceObj.get_rect()
AboveRectObj.center = (width - width//10, height -height//5)

UnderSurfaceObj = fontObj.render("Under Plane", True, red)
UnderRectObj = UnderSurfaceObj.get_rect()
UnderRectObj.center = (width - width//10, height -height//5)

fontObj = pygame.font.Font("fonts/big_noodle_titling.ttf", 50)
beginSurfaceObj = fontObj.render("Begin", True, black)
beginRectObj = beginSurfaceObj.get_rect()
beginRectObj.center = (width//2, height//2 + height//5)

InstructionSurfaceObj = fontObj.render("Instructions", True, black)
InstructionRectObj = InstructionSurfaceObj.get_rect()
InstructionRectObj.center = (width//2, height//2 - height//7)

VisualizeSurfaceObj = fontObj.render("Visualize", True, black)
VisualizeRectObj = VisualizeSurfaceObj.get_rect()
VisualizeRectObj.center = (width//2, height//2)

CompareSurfaceObj = fontObj.render("Compare", True, black)
CompareRectObj = CompareSurfaceObj.get_rect()
CompareRectObj.center = (width//2, height//2 + height//7)

margin = height//12
UploadSurfaceObj = fontObj.render("Upload", True, black)
UploadRectObj = UploadSurfaceObj.get_rect()
UploadRectObj.center = (width//2+width//10, height//2 - height//8)
UploadRectObj1 = UploadSurfaceObj.get_rect()
UploadRectObj1.center = (width//2 - width//4, height//2)
UploadRectObj2 = UploadSurfaceObj.get_rect()
UploadRectObj2.center = (width//2 + width//4, height//2)

ClearSurfaceObj = fontObj.render("Clear", True, black)
ClearRectObj = ClearSurfaceObj.get_rect()
ClearRectObj.center = (width//10, margin + height//6)
ClearRectObj1 = ClearSurfaceObj.get_rect()
ClearRectObj1.center = (width//6, height//4 - height//12)

DrawLineSurfaceObj = fontObj.render("Draw Lines", True, red)
DrawLineRectObj = DrawLineSurfaceObj.get_rect()
DrawLineRectObj.center = (width//10, margin + 2*(height//6))
DrawLineRectObj1 = DrawLineSurfaceObj.get_rect()
DrawLineRectObj1.center = (2.7*(width//6), height//4 - height//12)

ClearSurfaceObj = fontObj.render("Clear", True, black)
Clear2RectObj = ClearSurfaceObj.get_rect()
Clear2RectObj.center = (width//10, margin + 3*(height//6))

DrawingSurfaceObj = fontObj.render("Drawing", True, black)
DrawingRectObj = DrawingSurfaceObj.get_rect()
DrawingRectObj.center = (width//10, margin + 3*(height//6) + height//13)

CDSurfaceObj = fontObj.render("Clear Drawing", True, black)
CDRectObj = CDSurfaceObj.get_rect()
CDRectObj.center = (4.5*(width//6), height//4 - height//12)

fontObj = pygame.font.Font("fonts/big_noodle_titling.ttf", 20)
BeingDrawnSurfaceObj = fontObj.render("Drawing...", True, red)
BeingDrawnRectObj = BeingDrawnSurfaceObj.get_rect()
BeingDrawnRectObj.center = (width//20, height - height//30)

TracingSurfaceObj = fontObj.render("Tracing...", True, red)
TracingRectObj = TracingSurfaceObj.get_rect()
TracingRectObj.center = (width//20, height - 2*(height//30))
TracingRectObj1 = TracingSurfaceObj.get_rect()
TracingRectObj1.center = (width - width//20, height - 2*(height//30))



###############################################################################
def init(data):
    data.Screen = "SplashScreen"
    data.points = []
    data.points1 = []
    data.points2 = []
    data.pause = False
    data.pause1 = False
    data.pause2 = False
    data.draw = False
    data.draw1 = False
    data.cap = None
    data.cap1 = None
    data.cap2 = None
    data.start = None
    data.temp = None
    data.start1 = None
    data.temp1 = None
    data.lines = []
    data.lines1 = []
    data.OnPlane = None

def findPoints(cnt): #taken from OpenCV demo notes pygame_hand-detection.py
    total = [] #will be list of all areas
    allArrays = [] #will be list of 4 coordinate points
    if len(cnt) > 0:
        for array in cnt: 
            total.append(cv2.arcLength(array, True)) #finds largest area index
            allArrays.append(array)
        bigIndex = total.index(max(total))
        return cv2.boundingRect(allArrays[bigIndex]) #returns bounding box
    else:
        return (0,0,0,0)

def findClub(data, n): #main function that uses opencv to read and contour file
    if n == 0: 
        cap = data.cap
    elif n == 1:
        cap = data.cap1
    elif n == 2:
        cap = data.cap2
    while (cap.isOpened()):
        _, camInput = cap.read() #basic camera input
        if camInput is None:
            if n == 0:
                data.cap = None
                data.OnPlane = None
            elif n == 1:
                data.cap1 = None
            elif n == 2:
                data.cap2 = None
            break
        camInput = np.rot90(camInput)
        camInput = cv2.flip(camInput, 0)
        lowerBound = np.array([90, 31, 40], dtype = "uint8")
        upperBound = np.array([255, 250, 117], dtype = "uint8")
        #adapted from pyimagesearch "OpenCV and Python Color Detection"
        threshold = cv2.inRange(camInput, lowerBound, upperBound) #binary image
        output = cv2.bitwise_and(camInput, camInput, mask = threshold) 
        contours, hierarchy = cv2.findContours(threshold,
            cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
            #taken from pygame_hand-detection
        x,y,w,h = findPoints(contours) #bounding box coordinates
        if n == 0: #boundaries for how big and small contours are allowed to be
            wlower = 22
        elif n == 1 or n == 2:
            wlower = 15
        if w > wlower and w <200 and h > wlower and h < 200:
            if n == 0:
                list = data.points
            elif n == 1:
                list = data.points1
            elif n == 2:
                list = data.points2
            if list != []:
                previousx = list[-1][0]
                if abs(previousx - x) < 300: #contous must be close together
                                        #for them to be connected by line
                    cv2.rectangle(camInput, (x,y), (x+w, y+h), (213,255,0),5)
                    if n == 0:
                        if data.pause == False:
                            list.append((x,y,w,h)) #contours are added to a list
                            #which is then called in another function that 
                            #draws all the points in the list
                    elif n == 1:
                        if data.pause1 == False:
                            list.append((x,y,w,h))
                    elif n == 2:
                        if data.pause2 == False:
                            list.append((x,y,w,h))
            else: 
                cv2.rectangle(camInput, (x,y), (x+w, y+h), (213,255,0),5)
                if data.pause == False: 
                    list.append((x,y,w,h))
        else:
            pass
        camInput = cv2.cvtColor(camInput, cv2.COLOR_BGR2RGB) #convert BGR to RGB
        trace(data, camInput, n) #trace function that iterates through list
        window=pygame.surfarray.make_surface(camInput) 
            #converts openCV to pygame
        return window 

def trace(data, window, n):
    #connects each point in list of points
    if n == 0:
        list = data.points
        width = 10
        radius = 5
    elif n == 1:
        list = data.points1
        width = 6
        radius = 3
    elif n == 2:
        list = data.points2
        width = 6
        radius = 3
    for i in range(len(list)-1):
        #takes center from sequential points and draws line connecting them
        point1 = list[i]
        x1 = point1[0]
        y1 = point1[1]
        w1 = point1[2]
        h1 = point1[3]
        point2 = list[i+1]
        x2 = point2[0]
        y2 = point2[1]
        w2 = point2[2]
        h2 = point2[3]
        center1 = ((x1+(w1//2)), (y1+(h1//2)))
        center2 = ((x2+(w2/2)), (y2+(h2//2)))
        if abs(center1[0] - center2[0]) < 30:
            #lines has to be relatively close for them to be connected together
            if x2 > x1 + 3 and i > 20:
                #a separate color for the down swing 
                color = [255, 9, 99] #red
            else:
                color = [0, 255,213] #green
            cv2.circle(window, center1, radius, color, -1)
            cv2.line(window, center1, center2, color, width)
    if n == 0:
        xlowerbound = 414 
        xupperbound = 426
        #algorithm for plabe check
        if len(list) > 80:
            temp = []
            for i in range(len(list)):
                #finds two points with similar x values 
                #one on the way back, the other on the way down
                if list[i][0] > xlowerbound and list[i][0] < xupperbound:
                    temp.append(list[i])
            if temp[0][0] > temp[1][0]:
                #if x values are greater or lower than the other, create delta
                delta = 2*abs(temp[0][0] - temp[1][0])
            elif temp[0][0] < temp[1][0]:
                delta = -2*abs(temp[0][0] - temp[1][0])
            else:
                delta = 0
            if temp[0][1] > temp[1][1] + delta: #checks y values of 2 points
                if n == 0:
                    data.OnPlane = "Above"
            elif temp[0][1] < temp[1][1] + delta:
                if n == 0:
                    data.OnPlane = "Under"
            else:
                if n == 0:
                    data.OnPlane = "OnPlane"

def upload(data, n):
    #raw video input function
    msg = """
    Enter video file name: 
    """
    input = raw_input(msg)
    source = ("/Users/patricktan/Desktop/sophomore/15-112/termProject/"
                +"videos/" +str(input))
    #make sure this path is correct before starting
    if os.path.isfile(source):
        #checks if file is True
        if n == 0:
            data.cap = cv2.VideoCapture(source)
        elif n == 1:
            data.cap1 = cv2.VideoCapture(source)
        elif n == 2:
            data.cap2 = cv2.VideoCapture(source)
    else:
        #if not True, print this error message
        msg = """
        Error: File not in Directory
        Booooooo enter a real file name
        """
        print msg


def startDraw(data, event):
    #sets up data.start and data.temp values for draw line functions
    mousex, mousey = event.pos
    xbound = data.width//4.8
    xbound1 = data.width - data.width//47.8
    ybound = data.height//70
    ybound1 = data.height//1.3
    if (mousex > xbound and mousex < xbound1 and
        mousey > ybound and mousey < ybound1):
        if data.draw == True:
            data.start = (mousex, mousey)
            data.temp = (mousex, mousey)

def startDraw1(data, event):
    #same thing for a separate screen
    mousex, mousey = event.pos
    xbound = 0
    xbound1 = data.width
    ybound = data.height//3.5
    ybound1 = data.height// 3.5 + data.height//2.3
    if (mousex > xbound and mousex < xbound1 and
        mousey > ybound and mousey < ybound1):
        if data.draw1 == True:
            data.start1 = (mousex, mousey)
            data.temp1 = (mousex, mousey)

def drawLines(data, n): #line drawing function
    red = (183, 10, 10)
    width = 5
    #draws line based on your starting position and temporary positions
    if n == 0:
        pygame.draw.line(screen, red, data.start, data.temp, width)
    elif n == 1:
        pygame.draw.line(screen, red, data.start1, data.temp1, width)

def finishLine(data, event, n):
    mousex, mousey = event.pos
    #takes in mouse release to finish lines
    if n == 0:
        if data.start != None:
            width = 5
            pygame.draw.line(screen, red, data.start, (mousex, mousey), width)
            data.lines.append((data.start, (mousex, mousey)))
                #add start and finish to list of lines
            data.start = None
            data.temp = None
    elif n == 1:
        if data.start1 != None:
            width = 5
            pygame.draw.line(screen, red, data.start1, (mousex, mousey), width)
            data.lines1.append((data.start1, (mousex, mousey)))
            data.start1 = None
            data.temp1 = None

def drawAllLines(data, n):
    #all lines in the list of lines are draw onto pygame
    red = (183, 10, 10)
    if n == 0:
        lines = data.lines
    elif n == 1:
        lines = data.lines1
    for line in lines:
        x = line[0][0]
        y = line[0][1]
        x1 = line[1][0]
        y1 = line[1][1]
        width = 5
        pygame.draw.line(screen, red, (x,y), (x1,y1), width)


def mousePressUp(data, event): 
    #checks for mouse release events
    #X,Y coordinates hard coded based on size of screen
    mousex, mousey = event.pos
    cx = width//2
    cy = height//2
    gap = height//12
    margin = width//45

    if data.Screen == "SplashScreen":
        if (mousex > cx-(width/30) and mousex < cx+(width//30) and
            mousey > cy+(height//6) and mousey < cy + (height//4.5)):
            data.Screen = "LoadScreen"

    if data.Screen == "LoadScreen":
        if (mousex > margin and mousex < width//12 and 
            mousey > margin and mousey < height//11):
            data.Screen = "SplashScreen"
        if (mousex > cx-(width//11) and mousex < cx+(width//11) and 
            mousey > cy-(height//5.8) and mousey < cy-(height//8.5)):
            data.Screen = "Instructions"
        if (mousex > cx-(width//15) and mousex < cx+(width//15) and 
            mousey > cy-(height//35) and mousey < cy+(height//35)):
            data.Screen = "Visualize"
        if (mousex > cx-(width//15) and mousex < cx+(width//15) and 
            mousey > cy+(height//8.5) and mousey < cy+(height//5.8)):
            data.Screen = "Compare"

    if data.Screen == "Instructions":
        if (mousex > margin and mousex < width//12 and 
            mousey > margin and mousey < height//11):
            data.Screen = "LoadScreen"

    if data.Screen == "Visualize":
        if (mousex > margin and mousex < width//12 and 
            mousey > margin and mousey < height//11):
            data.Screen = "LoadScreen"
        if (mousex > width//10 - margin and mousex < width//10 + margin and 
            mousey > gap + height//6 - margin and mousey < gap + height//6 + 
            margin):
            data.points = []
        pausex = width - width//3 - width//7
        pausey = height - height//6
        if (mousex > pausex - width//30 and mousex < pausex + width//30 and 
            mousey > pausey - height//17 and mousey < pausey + height//17):
            data.pause = True
        startx = width - width//3
        starty = height - height//6
        if (mousex > startx - width//30 and mousex < startx + width//30 and 
            mousey > starty - height//17 and mousey < starty + height//17):
            data.pause = False
        uploadx = width//2 + width//10
        uploady = height//2 - height//8
        if data.cap == None:
            if (mousex > uploadx - width//30 and mousex < uploadx+width//30 and
                mousey > uploady - height//27 and mousey < uploady+height//27):
                upload(data, 0)
        drawx = width//10
        drawy = height//12 + 2*(height//6)
        if (mousex > drawx - width//20 and mousex < drawx + width//20 and
            mousey > drawy - height//27 and mousey < drawy + height//27):
            if data.draw == True:
                data.draw = False
            elif data.draw == False:
                data.draw = True
        clearDrawingx = width//10
        clearDrawingy = height//12 + 3*(height//6) + height//26
        if (mousex > clearDrawingx - width//20 and 
            mousex < clearDrawingx + width//20 and
            mousey > clearDrawingy - height//13 and 
            mousey < clearDrawingy + height//13):
            data.lines = []
        if (mousex > width-width//27 and mousex < width and
            mousey > height//70 and mousey < height//17.5):
            data.cap = None
            data.points = []
            data.OnPlane = None

    if data.Screen == "Compare":
        if (mousex > margin and mousex < width//12 and 
            mousey > margin and mousey < height//11):
            data.Screen = "LoadScreen"
        clearx = width//6
        cleary = height//4 - height//12
        if (mousex > clearx - width//30 and mousex < clearx + width//30 and
            mousey > cleary - height//27 and mousey < cleary + height//27):
            data.points = []
            data.points1 = []
        drawx = 2.7*(width//6)
        drawy = height//4 - height//12
        if (mousex > drawx - width//20 and mousex < drawx + width//20 and
            mousey > drawy - height//27 and mousey < drawy + height//27):
            if data.draw1 == True:
                data.draw1 = False
            elif data.draw1 == False:
                data.draw1 = True
        clearDrawingx = 4.5*(width//6)
        clearDrawingy = height//4 - height//12
        if (mousex > clearDrawingx - width//15 and 
            mousex < clearDrawingx + width//15 and
            mousey > clearDrawingy - height//27 and 
            mousey < clearDrawingy + height//27):
            data.lines1 = []
        upload1x = width//2 - width//4
        upload1y = height//2
        if data.cap1 == None:
            if (mousex > upload1x - width//20 and 
                mousex < upload1x + width//20 and
                mousey > upload1y - height//27 and 
                mousey < upload1y + height//27):
                upload(data, 1)
        upload2x = width//2 + width//4
        upload2y = height//2
        if data.cap2 == None:
            if (mousex > upload2x - width//20 and mousex < upload2x + width//20 and
                mousey > upload2y - height//27 and mousey < upload2y + height//27):
                upload(data, 2)
        if (mousex > width//2-width//27 and mousex < width//2 and
            mousey > height//3.5 and mousey < height//3):
            data.cap1 = None
            data.points1 = []
        if (mousex > width-width//27 and mousex < width and
            mousey > height//3.5 and mousey < height//3):
            data.cap2 = None
            data.points1 = []
        pause1x = width//6-35
        pause1y = height - height//5
        pause2x = 4*(width//6)-35
        start1x = 2*(width//6)-35
        start2x = 5*(width//6)-35
        if (mousex > pause1x - width//30 and mousex < pause1x + width//30 and 
            mousey > pause1y - height//17 and mousey < pause1y + height//17):
            data.pause1 = True
        if (mousex > start1x - width//30 and mousex < start1x + width//30 and 
            mousey > pause1y - height//17 and mousey < pause1y + height//17):
            data.pause1 = False
        if (mousex > pause2x - width//30 and mousex < pause2x + width//30 and 
            mousey > pause1y - height//17 and mousey < pause1y + height//17):
            data.pause2 = True
        if (mousex > start2x - width//30 and mousex < start2x + width//30 and 
            mousey > pause1y - height//17 and mousey < pause1y + height//17):
            data.pause2 = False


def redrawAll(data):
    WHITE = (255,255,255)
    BLACK = (0, 0, 0)
    if data.Screen == "SplashScreen":
        screen.fill(WHITE)
        screen.blit(titleSurfaceObj, titleRectObj)
        screen.blit(SubSurfaceObj, SubRectObj)
        screen.blit(beginSurfaceObj, beginRectObj)

    elif data.Screen == "LoadScreen":
        screen.fill(WHITE)
        screen.blit(InstructionSurfaceObj, InstructionRectObj)
        screen.blit(VisualizeSurfaceObj, VisualizeRectObj)
        screen.blit(CompareSurfaceObj, CompareRectObj)
        screen.blit(BackSurfaceObj, BackRectObj)

    elif data.Screen == "Instructions":
        screen.fill(WHITE)
        screen.blit(BackSurfaceObj, BackRectObj)
        Instructions = pygame.image.load("images/Instructions.png")
        InstructionsRectObj = Instructions.get_rect()
        InstructionsRectObj.center = (width//2, height//2)
        screen.blit(Instructions, InstructionsRectObj)

    elif data.Screen == "Visualize":
        screen.fill(WHITE)
        screen.blit(BackSurfaceObj, BackRectObj)
        close = pygame.image.load("images/close.png")
        if data.cap == None:
            screen.blit(UploadSurfaceObj, UploadRectObj)
        else:
            window = findClub(data, 0)
            if window is not None: #only uploads if there is a stream
                screen.blit(window,(230,10))
                screen.blit(close, (width-30, 10))
        screen.blit(ClearSurfaceObj, ClearRectObj)
        screen.blit(DrawLineSurfaceObj, DrawLineRectObj)
        screen.blit(ClearSurfaceObj, Clear2RectObj)
        screen.blit(DrawingSurfaceObj, DrawingRectObj)
        pause = pygame.image.load("images/pause.png")
        start = pygame.image.load("images/start.png")
        marginx = width//3 + width//7
        marginy = height//5
        screen.blit(pause, (width - marginx, height-marginy))
        screen.blit(start, (width - marginx +width//7, height-marginy))
        if data.draw == True and data.start != None and data.temp != None:
            drawLines(data, 0)
        drawAllLines(data, 0)
        if data.draw == True:
            screen.blit(BeingDrawnSurfaceObj, BeingDrawnRectObj)
        if data.pause == False and data.cap != None:
            screen.blit(TracingSurfaceObj, TracingRectObj)
        if data.OnPlane != None:
            if data.OnPlane == "OnPlane":
                screen.blit(GoodSwingSurfaceObj, GoodSwingRectObj)
            elif data.OnPlane == "Under":
                screen.blit(UnderSurfaceObj, UnderRectObj)
            elif data.OnPlane == "Above":
                screen.blit(AboveSurfaceObj, AboveRectObj)


    elif data.Screen == "Compare":
        screen.fill(WHITE)
        screen.blit(BackSurfaceObj, BackRectObj)
        screen.blit(ClearSurfaceObj, ClearRectObj1)
        screen.blit(DrawLineSurfaceObj, DrawLineRectObj1)
        screen.blit(CDSurfaceObj, CDRectObj)
        pause = pygame.image.load("images/pause.png")
        start = pygame.image.load("images/start.png")
        screen.blit(pause, (width//6-35, height - height//5))
        screen.blit(start, (2*(width//6)-35, height - height//5))
        screen.blit(pause, (4*(width//6)-35, height - height//5))
        screen.blit(start, (5*(width//6)-35, height - height//5))

        close = pygame.image.load("images/close.png")
        if data.cap1 == None:
            screen.blit(UploadSurfaceObj, UploadRectObj1)
        else:
            window = findClub(data, 1)
            if window is not None:
                screen.blit(window, (0, height//3.5))
                screen.blit(close, (520, height//3.5))
        if data.cap2 == None:
            screen.blit(UploadSurfaceObj, UploadRectObj2)
        else:
            window = findClub(data, 2)
            if window is not None:
                screen.blit(window, (width//2, height//3.5))
                screen.blit(close, (width-30, height//3.5))
        if data.draw1 == True and data.start1 != None and data.temp1 != None:
            drawLines(data, 1)
        drawAllLines(data, 1)
        if data.draw1 == True:
            screen.blit(BeingDrawnSurfaceObj, BeingDrawnRectObj)
        if data.pause1 == False and data.cap1 != None:
            screen.blit(TracingSurfaceObj, TracingRectObj1)
        elif (data.pause2 == False and data.cap2 != None):
            screen.blit(TracingSurfaceObj, TracingRectObj1)
        else: pass

###############################################################################
def main(): #main function that sets up data and main loop
    width = 1100
    height = 700
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    init(data)

    while True:
        redrawAll(data) #draws each screen

        checkForQuit()   
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONDOWN:
                if data.draw == True:
                    startDraw(data, event)
                if data.draw1 == True:
                    startDraw1(data, event)
            elif event.type == MOUSEMOTION:
                if data.Screen == "Visualize":
                    data.temp = event.pos
                if data.Screen == "Compare":
                    data.temp1 = event.pos
            elif event.type == MOUSEBUTTONUP:
                if data.draw == True:
                    finishLine(data, event, 0)
                if data.draw1 == True:
                    finishLine(data, event, 1)
                mousePressUp(data, event)
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if data.pause == False:
                        data.pause = True
                    elif data.pause == True:
                        data.pause = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        cv2.destroyAllWindows()

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


main()


