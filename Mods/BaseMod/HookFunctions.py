"""
This file is mandatory for the mod to be able to talk with the engine.
All mods need to use specifically these function (hooks). You can put whatever you want in these functions.
Furthermore, all objects need to inherit from the ScreenObject class.
"""

from Mods.BaseMod.Sprites.Images import *
from Mods.BaseMod.HookScreenObject import *
from Mods.BaseMod.HelperFunctions import *
from Mods.BaseMod.Modules import Module

import random

MouseCoords = [0,0]
MousePressed = False
ButtonPresses = [False, False, False]
DistanceMesurement = 10000
Tilted = False
KeyPadInputs = [False, False, False, False, False, False, False, False]
GameWindowWidthHeight = (0,0)
CurrentTime = 0.0

GameDifficulty = 0

#0: The game is playing
#1: The game is won
#2: The game is lost
GameState = 0

def InitializeObjects(GameMode, GameWindowSize) :

    global GameWindowWidthHeight
    GameWindowWidthHeight = GameWindowSize

    global GameDifficulty
    GameDifficulty = GameMode

    ModulesList = Module.AvailableModules.copy()
    
    ModuleSize = GetImageWidthHeight(GetImage(ModulesList[0]))
    SizeOfModule = GetMaxPoint(-1, -1, ModuleSize[0], ModuleSize[1], GameWindowWidthHeight[0], GameWindowWidthHeight[1])
    print(ModuleSize[0])

    SizeOfModule = (SizeOfModule[0], SizeOfModule[1])
    #quit()
    AvailableSlots = []
  
    for ThisSlotY in range(0,GameWindowWidthHeight[1], ModuleSize[1]) :
        
        for ThisSlotX in range(0,GameWindowWidthHeight[0], ModuleSize[0]) :

            if ThisSlotY + ModuleSize[1] <= GameWindowWidthHeight[1] and ThisSlotX + ModuleSize[0] <= GameWindowWidthHeight[0]:
                AvailableSlots.append(GetNormalizedCoordinates(int(ThisSlotX), int(ThisSlotY), GameWindowWidthHeight[0], GameWindowWidthHeight[1]))

    SlotsPositions = AvailableSlots

  
    #SlotsPositions = [(-1,-1) , (-0.325, -1), (0.34, -1), (-1, -0.01), (-0.325, -0.01), (0.34, -0.01)]

    #The easiest difficulty, with only two modules to solve 
    if GameDifficulty == 0 :

        ModulesList = Module.AvailableModules.copy()

        ModuleIterator = 0
        #Iterate through all of the modules except the empty one
        for ModuleIterator in range(1, 3) :
            ChosenModule = ModulesList.pop(random.randint(1, len(ModulesList)-1))

            ModuleAdded = Module(ChosenModule, SlotsPositions[ModuleIterator-1][0], SlotsPositions[ModuleIterator-1][1])
            
        for ThisBombModule in Module.GetModules("MODULE_BOMB") :
            ThisBombModule.GiveBombCode(len(Module.CurrentModulesInGame))

        #Fill up the rest with the empty one
        for ModuleIterator in range(ModuleIterator, len(SlotsPositions)) :

            ModuleAdded = Module(ModulesList[0], SlotsPositions[ModuleIterator][0], SlotsPositions[ModuleIterator][1])

    elif GameDifficulty == 1 :
        ModulesList = Module.AvailableModules.copy()

        ModuleIterator = 0
        #Iterate through all of the modules except the empty one
        for ModuleIterator in range(1, len(ModulesList)) :
            ChosenModule = ModulesList.pop(random.randint(1, len(ModulesList)-1))

            ModuleAdded = Module(ChosenModule, SlotsPositions[ModuleIterator-1][0], SlotsPositions[ModuleIterator-1][1])

        for ThisBombModule in Module.GetModules("MODULE_BOMB") :
            ThisBombModule.GiveBombCode(len(Module.CurrentModulesInGame))

        #Fill up the rest with the empty one
        for ModuleIterator in range(ModuleIterator, len(SlotsPositions)) :

            ModuleAdded = Module(ModulesList[0], SlotsPositions[ModuleIterator][0], SlotsPositions[ModuleIterator][1])



def SetBombTime(SetValue) :

    global CurrentTime
    global BombTime
    BombTime = SetValue
    print(str(CurrentTime) + " " + str(BombTime))




def LoadImagesToEngine() :
    #Loads all of the images to the engine
    return GetImagesByPart(".png")

#The amount of time left pereived by the bomb
def GetPerceivedBombTime() :
    return Module.GetModules("MODULE_BOMB")[0].CurrentTimePenalty + CurrentTime


def GetBombTime() :
    
    ThisBombModule = Module.GetModules("MODULE_BOMB")
    #print(ThisBombModule[0].BombTime)
    return ThisBombModule[0].BombTime

def UpdateLogic(MouseCoordsIn, MousePressedIn, ButtonPressesIn, DistanceMesurementIn, TiltedIn, KeyPadInputsIn, GameWindowWidthHeightIn, ScaleFactor, CurrentTimeIn):
    
    global MouseCoords
    global MousePressed 
    global ButtonPresses
    global DistanceGameWindowWidthHeightInMesurement
    global Tilted 
    global KeyPadInputs 
    global GameWindowWidthHeight
    global CurrentTime
    global GameState
    global BombTime

    CurrentTime = CurrentTimeIn

    GameWindowWidthHeight = GameWindowWidthHeightIn.copy()

    #The mouse coordinates converted to normalized screen coordinates
    MouseCoords = MouseCoordsIn.copy()
  
    MouseCoords[0] = (MouseCoords[0]/ScaleFactor/GameWindowWidthHeight[0] - 0.5)*2
    MouseCoords[1] = (MouseCoords[1]/ScaleFactor/GameWindowWidthHeight[1] - 0.5)*2

    #Registers if the mouse has been pressed
    MousePressed = MousePressedIn

    
    #Registers any of the button presses (RGB buttons)
    ButtonPresses = ButtonPressesIn.copy()

    #Registers the distance mesured by the sensor
    DistanceMesurement = DistanceMesurementIn                                    

    #Registers if the board is tilted or not
    Tilted = TiltedIn

    #Registers if the keypad key presses
    KeyPadInputs = KeyPadInputsIn.copy()
   
    #Loop through all of the modules
    for ThisModule in Module.CurrentModulesInGame :

        MaxPoint = GetMaxPoint(ThisModule.X, ThisModule.Y, ThisModule.Width, ThisModule.Height, GameWindowWidthHeightIn[0], GameWindowWidthHeightIn[1])

        #The mouse position relative to the module
        MouseRelativeToModule = [1000,1000]

        #Array is modified, so copy
        MouseRelativeToModule = MouseCoordsIn.copy()

        ModuleScreenPosition = GetScreenCoordinates(ThisModule.X, ThisModule.Y, GameWindowWidthHeight[0], GameWindowWidthHeight[1])

        #Make the mouse relative to this module. To do that, the mouse position should be relative to the module position and then normalize
        MouseRelativeToModule[0] = ((MouseCoordsIn[0]/ScaleFactor - ModuleScreenPosition[0])/ThisModule.Width - 0.5)*2
        MouseRelativeToModule[1] = ((MouseCoordsIn[1]/ScaleFactor - ModuleScreenPosition[1])/ThisModule.Height - 0.5)*2

        #Update the module with the relative mouse position
        ThisModule.UpdateModule(MouseRelativeToModule)

    #Check for a game over. Losing means that the current time is equal to the bomb time, winning means that the bomb is solved
    #if BombTime <= CurrentTime :
    if Module.GetModules("MODULE_BOMB")[0].CurrentTimePenalty + CurrentTime >= GetBombTime() :
        GameState = 2
    elif Module.GetModules("MODULE_BOMB")[0].solved :
        GameState = 1

    return GameState

