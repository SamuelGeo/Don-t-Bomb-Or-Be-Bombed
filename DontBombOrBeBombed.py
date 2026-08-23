#Import dependencies
import pygame
import os
from pygame.locals import *
#All of the game logic is contained in the mods folder, whichever mod is chosen. By default, it is BaseMod
from Mods.BaseMod import *
import time
import math
import Mods.BaseMod.HookFunctions as HookVars
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
DisplayGameWindow = pygame.display.set_mode((ScreenSize.current_w,ScreenSize.current_h))

#Makes a pygame "surface". This is essentially an image. The scale is 16:9
GameWindow = pygame.Surface(GameScale)

#Key: An image's file path, Value: A surface object created by pygame.image.load() (effectively a loaded picture)
LoadedImages = {}

#Title of the GameWindowdow
pygame.display.set_caption("DontBombOrBeBombed")

#The clock of pygame. It is an artificial bottleneck to be sure that the game does not run too fast.
#Because the logic updates (ticks) and the graphical updates (frames) are linked (choice made by me), making the game run unchained will make it go MUCH faster than it is supposed to be.
clock = pygame.time.Clock()

#TODO: Remove this. Each object will have its own path to a picture. instead, call "draw sprites" to get all of the pictures and their positions
#LEDLights = (pygame.image.load(os.path.join(os.path.dirname(__file__), 'Sprites','LED_RED.png')).convert_alpha(), pygame.image.load(os.path.join(os.path.dirname(__file__), 'Sprites','LED_GREEN.png')).convert_alpha(), pygame.image.load(os.path.join(os.path.dirname(__file__), 'Sprites','LED_BLUE.png')).convert_alpha(), pygame.image.load(os.path.join(os.path.dirname(__file__), 'Sprites','LED_OFF.png')).convert_alpha())

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

#Converts normalized screen coordinates (-1 , 1) to the actual screen coordinates

#def GetScreenCoordinates(ThisScreenObject : ScreenObject, ParentSurface : pygame.Surface):
    #return((ThisScreenObject.X/2.0 + 0.5)*ParentSurface.get_size()[0], ((ThisScreenObject.Y)/2.0 + 0.5)*ParentSurface.get_size()[1])

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


def BackroundShader(SurfaceIn) :
    pxarray = pygame.PixelArray(SurfaceIn)

    for PixelY in range(0, SurfaceIn.get_size()[1]) :
        for PixelX in range(0, SurfaceIn.get_size()[0]) :
            uvX = PixelX/SurfaceIn.get_size()[0]
            uvY = PixelY/SurfaceIn.get_size()[1]
            #global BombTime
            #The closer to 0, the less time is left
            TimeLeftFactor= 1.0 - (GetPerceivedBombTime())/float(GetBombTime())
            #print(GetBombTime())
            PixelColorR = (0.5 + 0.5*math.cos(pygame.time.get_ticks()/1000+uvX))*TimeLeftFactor
            PixelColorG = (0.5 + 0.5*math.cos(pygame.time.get_ticks()/1000+uvY+2))*TimeLeftFactor
            PixelColorB = (0.5 + 0.5*math.cos(pygame.time.get_ticks()/1000+uvX+4))*TimeLeftFactor
            pxarray[PixelX, PixelY] = (max(0,PixelColorR*255), max(0,PixelColorG*255), max(0,PixelColorB*255))
    
    pxarray.close()

LoadAllImages()


InitializeObjects(1, GameWindow.get_size())
#time.sleep(1)


while run:

    #Won
    if ThisGameState == 1 :
        print("You won")
        quit()
    #Lost
    elif ThisGameState == 2 :

        print("You lost")
        quit()

    elif ThisGameState == 0 :
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        ThisGameState = UpdateLogic(MousePosition, MouseIsPressed, ButtonsPressed, DistanceMesured, TiltSensorState, KeyPadPressedButtons, list(GameWindow.get_rect().size), ScaleFactor, pygame.time.get_ticks())

        # clear surface. Mo need to do it for the actual display, because this surface covers the entirety of the display.
        #GameWindow.fill((pygame.time.get_ticks()%255, 100, 100))

        # draw game objects
        # [...]
        #return (self.X, self.Y, self.Image, WireRenderInformation)
        """
        if BackRoundColorTickCounter == 60 :
            CurrentBackroundColor = FutureBackroundColor.copy()
            FutureBackroundColor = [(pygame.time.get_ticks()+random.randint(0,255))%255, (pygame.time.get_ticks()+random.randint(0,255))%255, (pygame.time.get_ticks()+random.randint(0,255))%255]
            ColorChangeFactor = [(FutureBackroundColor[0]-CurrentBackroundColor[0])/60, (FutureBackroundColor[1]-CurrentBackroundColor[1])/60, (FutureBackroundColor[2]-CurrentBackroundColor[2])/60]
            BackRoundColorTickCounter = 0

        BackRoundColorTickCounter = BackRoundColorTickCounter + 1
        

        RoundedFillColor = CurrentBackroundColor.copy()
        RoundedFillColor[0] = int(RoundedFillColor[0])
        RoundedFillColor[1] = int(RoundedFillColor[1])
        RoundedFillColor[2] = int(RoundedFillColor[2])

        DisplayGameWindow.fill(RoundedFillColor)
        CurrentBackroundColor = [CurrentBackroundColor[0] + ColorChangeFactor[0] , CurrentBackroundColor[1] + ColorChangeFactor[1], CurrentBackroundColor[2] + ColorChangeFactor[2]]      
        """

        #Cool shader taken from shader toy to make the backround
        #Small screen because if using actual full resolution, python falls to its knees
        ColorSurface = pygame.Surface((2,2))

        BackroundShader(ColorSurface)

        RenderScreen(GameWindow, ScreenObject.ScreenObjectsArray)
        
        #DisplayGameWindow.fill((pygame.time.get_ticks()+random.randint(0,255))%255, (pygame.time.get_ticks()+random.randint(0,255))%255, (pygame.time.get_ticks()+random.randint(0,255))%255)
        

 
        #Now draw the surface that contains all of the images on it to the display. Also scale it before that.
        DisplayGameWindow.blit(pygame.transform.smoothscale_by(ColorSurface, (DisplayGameWindow.get_size()[0]/ColorSurface.get_size()[0], DisplayGameWindow.get_size()[1]/ColorSurface.get_size()[1])), (0,0))
        DisplayGameWindow.blit(pygame.transform.scale_by(GameWindow, (ScaleFactor)), GameWindowOffset)

        # update display
        pygame.display.flip()

        # limit frames per second
        clock.tick(60) 

pygame.quit()