"""
This file is mandatory for the mod to be able to talk with the engine.
All mods need to use specifically these function (hooks). You can put whatever you want in these functions.
Furthermore, all objects need to inherit from the ScreenObject class.
"""

from Mods.BaseMod.Sprites.Images import *
from Mods.BaseMod.HookScreenObject import *
from Mods.BaseMod.HelperFunctions import *
from Mods.BaseMod.Modules import Module
from Mods.BaseMod.HookVariables import GlobalProperties as GP
from Mods.BaseMod.BackroundShaders import CalculateShader
from Mods.BaseMod.BackroundShaders import SetBackroundShader
from Mods.BaseMod.BackroundShaders import NumberOfShaders
from Mods.BaseMod.BackroundShaders import DifferencyScore
from Mods.BaseMod.BackroundShaders import ShaderFPS
from Mods.BaseMod.BackroundShaders import ShadersResolution
from Mods.BaseMod.BackroundShaders import SelectedShader
from Mods.BaseMod.BackroundShaders import LoadShader
import random

def SetBackroundSurfaceSize(SurfaceSizeIn) :

    SurfaceScaleBy = max(SurfaceSizeIn[0]/ShadersResolution, SurfaceSizeIn[1]/ShadersResolution)
   
    return (int(SurfaceSizeIn[0]/SurfaceScaleBy),int(SurfaceSizeIn[0]/SurfaceScaleBy))

def LoadThisShader(ShaderIndex, SurfaceSize) :

    return LoadShader(ShaderIndex, SurfaceSize)

def InitializeObjects(GameMode, GameWindowSize) :
    
    GP.GameWindowWidthHeight = GameWindowSize

    GP.GameDifficulty = GameMode

    ModulesList = Module.AvailableModules.copy()
    
    ModuleSize = GetImageWidthHeight(GetImage(ModulesList[0]))
    SizeOfModule = GetMaxPoint(-1, -1, ModuleSize[0], ModuleSize[1], GP.GameWindowWidthHeight[0], GP.GameWindowWidthHeight[1])
    print(ModuleSize[0])

    SizeOfModule = (SizeOfModule[0], SizeOfModule[1])
    #quit()
    AvailableSlots = []
  
    for ThisSlotY in range(0,GP.GameWindowWidthHeight[1], ModuleSize[1]) :
        
        for ThisSlotX in range(0,GP.GameWindowWidthHeight[0], ModuleSize[0]) :

            if ThisSlotY + ModuleSize[1] <= GP.GameWindowWidthHeight[1] and ThisSlotX + ModuleSize[0] <= GP.GameWindowWidthHeight[0]:
                AvailableSlots.append(GetNormalizedCoordinates(int(ThisSlotX), int(ThisSlotY), GP.GameWindowWidthHeight[0], GP.GameWindowWidthHeight[1]))

    SlotsPositions = AvailableSlots

  
    #SlotsPositions = [(-1,-1) , (-0.325, -1), (0.34, -1), (-1, -0.01), (-0.325, -0.01), (0.34, -0.01)]

    #The easiest difficulty, with only two modules to solve 
    if GP.GameDifficulty == 0 :

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

    elif GP.GameDifficulty == 1 :
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

def LoadImagesToEngine() :
    #Loads all of the images to the engine
    return GetImagesByPart(".png")

#The amount of time left pereived by the bomb
def GetPerceivedBombTime() :
    
    return Module.GetModules("MODULE_BOMB")[0].CurrentTimePenalty + GP.CurrentTime

def GetShaderIndex() :

    #Return index of the currently selected shader
    
    return (SelectedShader)

def GetNumberOfShaders():

    return NumberOfShaders


#TODO: Remove this
def GetBombTime() :
    
    ThisBombModule = Module.GetModules("MODULE_BOMB")
    #print(ThisBombModule[0].BombTime)
    return ThisBombModule[0].BombTime

def UpdateLogic(MouseCoordsIn, MousePressedIn, ButtonPressesIn, DistanceMesurementIn, TiltedIn, KeyPadInputsIn, GameWindowWidthHeightIn, ScaleFactor, CurrentTimeIn):
 
    

    GP.CurrentTime = CurrentTimeIn

    GP.GameWindowWidthHeight = GameWindowWidthHeightIn.copy()

    #The mouse coordinates converted to normalized screen coordinates
    
    GP.MouseCoords = MouseCoordsIn.copy()
  
    GP.MouseCoords[0] = (GP.MouseCoords[0]/ScaleFactor/GP.GameWindowWidthHeight[0] - 0.5)*2
    GP.MouseCoords[1] = (GP.MouseCoords[1]/ScaleFactor/GP.GameWindowWidthHeight[1] - 0.5)*2

    #Registers if the mouse has been pressed
    GP.MousePressed = MousePressedIn

    
    #Registers any of the button presses (RGB buttons)
    GP.ButtonPresses = ButtonPressesIn.copy()

    #Registers the distance mesured by the sensor
    GP.DistanceMesurement = DistanceMesurementIn                                    

    #Registers if the board is tilted or not
    GP.Tilted = TiltedIn

    #Registers if the keypad key presses
    GP.KeyPadInputs = KeyPadInputsIn.copy()

    #SetBackroundShader(int(GP.CurrentTime/1000.0)%4)
   
    #Loop through all of the modules
    for ThisModule in Module.CurrentModulesInGame :

        MaxPoint = GetMaxPoint(ThisModule.X, ThisModule.Y, ThisModule.Width, ThisModule.Height, GP.GameWindowWidthHeight[0], GP.GameWindowWidthHeight[1])

        #The mouse position relative to the module
        MouseRelativeToModule = [1000,1000]

        #Array is modified, so copy
        MouseRelativeToModule = MouseCoordsIn.copy()

        ModuleScreenPosition = GetScreenCoordinates(ThisModule.X, ThisModule.Y, GP.GameWindowWidthHeight[0], GP.GameWindowWidthHeight[1])

        #Make the mouse relative to this module. To do that, the mouse position should be relative to the module position and then normalize
        MouseRelativeToModule[0] = ((MouseCoordsIn[0]/ScaleFactor - ModuleScreenPosition[0])/ThisModule.Width - 0.5)*2
        MouseRelativeToModule[1] = ((MouseCoordsIn[1]/ScaleFactor - ModuleScreenPosition[1])/ThisModule.Height - 0.5)*2

        #Update the module with the relative mouse position
        ThisModule.UpdateModule(MouseRelativeToModule)

    #Check for a game over. Losing means that the current time is equal to the bomb time, winning means that the bomb is solved
    #if BombTime <= CurrentTime :
    if Module.GetModules("MODULE_BOMB")[0].CurrentTimePenalty + GP.CurrentTime >= GetBombTime() :
        GP.GameState = 2
    elif Module.GetModules("MODULE_BOMB")[0].solved :
        GP.GameState = 1

    return GP.GameState

