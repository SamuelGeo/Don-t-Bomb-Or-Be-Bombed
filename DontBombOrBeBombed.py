#Import dependencies
import pygame

import os
from pygame.locals import *
#All of the game logic is contained in the mods folder, whichever mod is chosen. By default, it is BaseMod
from Mods.BaseMod import *
import time
import math
from Mods.BaseMod.HookFunctions import *

#Initializes pygame, something that it wants to do for some reason. Not important to the logic.
pygame.init()

#The information of the current display
ScreenSize = pygame.display.Info()

#The "original" game scale that the game will scale from for different displays
#GameScale = (192,108)
#(228,128)
GameScale = (228,136)

#Sets the display GameWindowdow size. Defaulted to fullscreen
#NOTE: By FAR the biggest contributor to performance hit.
#DisplayGameWindow = pygame.display.set_mode((ScreenSize.current_w,ScreenSize.current_h))
#DisplayGameWindow = pygame.display.set_mode((ScreenSize.current_w/15,ScreenSize.current_h/15), pygame.FULLSCREEN | pygame.SCALED)
ScaleFactorDisplayGameWindow = max(ScreenSize.current_w/GameScale[0],ScreenSize.current_h/GameScale[1])


DisplayGameWindow = pygame.display.set_mode((ScreenSize.current_w/ScaleFactorDisplayGameWindow, ScreenSize.current_h/ScaleFactorDisplayGameWindow), pygame.FULLSCREEN | pygame.SCALED)

#Makes a pygame "surface". This is essentially an image. The scale is 16:9
GameWindow = pygame.Surface(GameScale, pygame.SRCALPHA)

#Key: An image's file path, Value: A surface object created by pygame.image.load() (effectively a loaded picture)
LoadedImages = {}

#Title of the GameWindowdow
pygame.display.set_caption("DontBombOrBeBombed")

#The clock of pygame. It is an artificial bottleneck to be sure that the game does not run too fast.
#Because the logic updates (ticks) and the graphical updates (frames) are linked (choice made by me), making the game run unchained will make it go MUCH faster than it is supposed to be.
clock = pygame.time.Clock()

#run is what makes the while loop run
run = True

#The scale factor of the game so that it looks the same on all displays
ScaleFactor = min(DisplayGameWindow.get_size()[0]/GameWindow.get_size()[0], DisplayGameWindow.get_size()[1]/GameWindow.get_size()[1])


#Checks if the game fills the screen in width
if ScaleFactor == DisplayGameWindow.get_size()[0]/GameWindow.get_size()[0] :

    #To make the game be in the middle, find the difference in size and divide by two (height wise)
    GameWindowOffset = (0, (DisplayGameWindow.get_size()[1]-GameWindow.get_size()[1]*ScaleFactor)/2)

#Same thing but fit for width
else :

    GameWindowOffset = ((DisplayGameWindow.get_size()[0]-GameWindow.get_size()[0]*ScaleFactor)/2, 0)

#The state of the game
#0 The game is running
#1 The game is won
#2 the game is lost
ThisGameState = 0

#The color of the backround (the part of the screen that the game does not cover) 
FutureBackroundColor = [0,0,0]

#The old backround color
CurrentBackroundColor = [0,0,0]

#How much of R,G and B to add such that the old color transitions to the new one over the span of X seconds
ColorChangeFactor = [0,0,0]

#Counts up to X ticks to calculate a new backround color
BackRoundColorTickCounter = 0

#A list of pre loaded shaders. It is actually just a list of multiple lists that contain pygame surfaces that each represent a frame of their respective shader
PreLoadedShadersList = []

#All of the shaders loaded into surfaces. Each element is a list of surfaces that each represent a frame of a shader
ShaderSurfacesList = []

def RenderScreen(ParentSurface, ThisScreenObjectArray) :

    #print(str(ThisScreenObjectArray))
    if len(ThisScreenObjectArray) != 0 :
        for ThisScreenObject in ThisScreenObjectArray :

            #If the screen object is visible
            if ThisScreenObject.Visible :
                #Get the screen coordinates of the screen object
                ThisScreenObjectCoordinates = GetScreenCoordinates(ThisScreenObject.X, ThisScreenObject.Y, ParentSurface.get_size()[0], ParentSurface.get_size()[1])
                #Get the loaded pygame picture and copy it 
                ThisObjectPicture = LoadedImages[ThisScreenObject.Image].copy()

                if len(ThisScreenObject.Children) != 0 :
                    #print("SCREENOBJECTPICTURE")
                    #print(str(ThisObjectPicture))
                    #Also render all of the children
                    RenderScreen(ThisObjectPicture, ThisScreenObject.Children)

                if ThisScreenObject.Rotation != 0 :
                    CenterPoint = GetScreenCoordinates(ThisScreenObject.X, ThisScreenObject.Y, ParentSurface.get_size()[0], ParentSurface.get_size()[1])
                    ThisObjectPicture = pygame.transform.rotate(ThisObjectPicture, ThisScreenObject.Rotation)
                    ParentSurface.blit(ThisObjectPicture, CenterPoint)
                else :
                    ParentSurface.blit(ThisObjectPicture, ThisScreenObjectCoordinates)
   

#Loads all of the images into pygame        
def LoadAllImages() :
    #Get all of the directories
    ImageDirectories = LoadImagesToEngine()
    #Loop through them
    for ThisPicture in ImageDirectories :
        #Append
        LoadedImages[ThisPicture] = pygame.image.load(ThisPicture).convert_alpha()
        testvar = pygame.image.load(ThisPicture).convert_alpha()
  
        testvar.get_rect().topleft

def CalculateultrasonicDistance() :
    return 1000


"""

-------------------------------
DEPRECATED METHODS
-------------------------------


def SurfaceSizeToPixelArraySize(ParentSurface, PixelArray) :

    SurfaceScaleX = len(PixelArray)/ParentSurface.get_size()[0]
    SurfaceScaleY = len(PixelArray[0])/ParentSurface.get_size()[1]

    ResizedSurface = pygame.Surface((len(PixelArray)/SurfaceScaleX,len(PixelArray[0])/SurfaceScaleY))

    return ResizedSurface
"""

"""
def SetShaderResolution(ParentSurface) :

    Resolution = GetBackroundShaderSize()
    SurfaceScale = max(ParentSurface.get_size()[0]/Resolution, ParentSurface.get_size()[1]/Resolution)
    ShaderSurface = pygame.Surface((ParentSurface.get_size()[0]/SurfaceScale,ParentSurface.get_size()[1]/SurfaceScale))
    #ShaderSurface = pygame.Surface((Resolution,Resolution))

    return ShaderSurface


def DisplayShader(SurfaceIn) :
    if SurfaceIn.get_size()[0] != GetBackroundShaderSize() or SurfaceIn.get_size()[1] != GetBackroundShaderSize():
        SetShaderResolution(SurfaceIn)
    
    ShaderPixels = GetBackroundShader(SurfaceIn.get_size()) 
    #print("FIRST",len(ShaderPixels[0]), len(ShaderPixels), SurfaceIn.get_size()[0], SurfaceIn.get_size()[1])
            
    pxarray = pygame.PixelArray(SurfaceIn)


    #print("SECOND",len(ShaderPixels[0]), len(ShaderPixels), SurfaceIn.get_size()[0], SurfaceIn.get_size()[1])
    
    for PosY in range(0,len(ShaderPixels)) :
  
        for PosX in range(0,len(ShaderPixels[PosY])) :
            #print(ShaderPixels[PosY][PosX])
            #print(str(PosX )+ ", " + str(PosY))
            pxarray[PosX, PosY] = tuple(ShaderPixels[PosY][PosX]) 
    pxarray.close()
"""
#TODO: get away from loading ALL of the frames into pygame surfaces, because it uses way too much RAM (150 pixels for 2 @ 60fps uses 6 gigs of RAM). 
def FrameToSurface(PixelArray) :
    global DisplayGameWindow

    ThisSurface = pygame.Surface(SetBackroundSurfaceSize(DisplayGameWindow.get_size()))
    pxarray = pygame.PixelArray(ThisSurface)

    for PosY in range(0,len(PixelArray)) :
  
        for PosX in range(0,len(PixelArray[PosY])) :
            #print(ShaderPixels[PosY][PosX])
            #print(str(PosX )+ ", " + str(PosY))
            pxarray[PosX, PosY] = tuple(PixelArray[PosY][PosX])
    pxarray.close()

    return ThisSurface

def LoadAllShaders() :
    
    NumberOfShaders = GetNumberOfShaders()
    for ShaderIterator in range(0,NumberOfShaders) :

        ThisShaderPixelFrames = LoadShader(ShaderIterator, SetBackroundSurfaceSize(DisplayGameWindow.get_size()))
        ThisShaderSurfaceFrames = []
        
        for ThisFrame in ThisShaderPixelFrames :

            NewFrameSurface = FrameToSurface(ThisFrame)
            ThisShaderSurfaceFrames.append(NewFrameSurface)

        ShaderSurfacesList.append(ThisShaderSurfaceFrames)

    return ShaderSurfacesList

def DisplayShader(SurfaceIn, TicksIn) :

    ShaderSurface = ShaderSurfacesList[GetShaderIndex()][(int(TicksIn)%(len(ShaderSurfacesList[GetShaderIndex()])))]

    #print((int(TicksIn)%(len(ShaderSurfacesList[GetShaderIndex()]))))
    SurfaceIn.blit(pygame.transform.smoothscale_by(ShaderSurface, (SurfaceIn.get_size()[0]/ShaderSurface.get_size()[0], SurfaceIn.get_size()[1]/ShaderSurface.get_size()[1])), (0,0))

LoadAllImages()



InitializeObjects(1, GameWindow.get_size())
#time.sleep(1)

#ColorSurfaceScale = max(DisplayGameWindow.get_size()[0]/30, DisplayGameWindow.get_size()[1]/30)
#ColorSurface = pygame.Surface((DisplayGameWindow.get_size()[0]/ColorSurfaceScale,DisplayGameWindow.get_size()[1]/ColorSurfaceScale))
#ColorSurface = pygame.Surface((805/3,453/3))

#The game time in microseconds. It is not real execution time, instead, it is calculated by the amount of updates.
GameTime = 0.0
GameTicks = 0

LoadAllShaders()

while run:

    #Won
    if ThisGameState == 1 :
        print("You won")
        run = False

    #Lost
    elif ThisGameState == 2 :

        print("You lost")
        run = False

    elif ThisGameState == 0 :
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
        

        # update game objects
        # [...]
        ButtonsPressed = [False, False, False]
        DistanceMesured = CalculateultrasonicDistance()
        TiltSensorState = False
        KeyPadPressedButtons = [False, False, False, False, False, False, False, False]
        MouseIsPressed = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Spacebar pressed once!")
            elif event.key == pygame.K_ESCAPE:
                run = False 

        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1:
                MouseIsPressed = True     

        MousePosition = list(pygame.mouse.get_pos())
        MousePosition[0] = MousePosition[0] - GameWindowOffset[0]
        MousePosition[1] = MousePosition[1] - GameWindowOffset[1]
        ThisGameState = UpdateLogic(MousePosition, MouseIsPressed, ButtonsPressed, DistanceMesured, TiltSensorState, KeyPadPressedButtons, list(GameWindow.get_rect().size), ScaleFactor, GameTime)
        DisplayShader(DisplayGameWindow, GameTicks)
        GameTicks = GameTicks + 1
        GameTime = GameTime + 1000.0/60.0

        # clear surface. Mo need to do it for the actual display, because this surface covers the entirety of the display.
        #GameWindow.fill((pygame.time.get_ticks()%255, 100, 100))

        # draw game objects
        # [...]
        #return (self.X, self.Y, self.Image, WireRenderInformation)

        RenderScreen(GameWindow, ScreenObject.ScreenObjectsArray)
        
        #DisplayGameWindow.fill((pygame.time.get_ticks()+random.randint(0,255))%255, (pygame.time.get_ticks()+random.randint(0,255))%255, (pygame.time.get_ticks()+random.randint(0,255))%255)
    
 
        #Now draw the surface that contains all of the images on it to the display. Also scale it before that.
        
        #DisplayGameWindow.blit(pygame.transform.scale_by(GameWindow, (ScaleFactor)), GameWindowOffset)

        # update display
        pygame.display.flip()

        # limit frames per second
        clock.tick(60) 
        print(clock.get_fps())

    if not run :
        ShaderSurfacesList.clear()
        LoadedImages.clear()
        GameWindow = None
        DisplayGameWindow = None
        pygame.display.quit()
        pygame.quit()

