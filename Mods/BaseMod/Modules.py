"""
A module is a puzzle. The puzzles can be very many things like press buttons in order,
cut the right wires, etc.
The puzzles ARE NOT defined in the source code, but in a different file named Mods/[YourMod]/Modules.
A module reads the data from the given file and automatically fills up its varibles
"""

import Mods.BaseMod.Wires as Wires
import random
from Mods.BaseMod.HookScreenObject import *
from Mods.BaseMod.HelperFunctions import *
import Mods.BaseMod.HookFunctions as HookVars
from Mods.BaseMod.Arrows import *
from Mods.BaseMod.HintDots import *
from Mods.BaseMod.ScreenForDots import *
from Mods.BaseMod.TimerSegments import *
from Mods.BaseMod.KeyPadButtons import *

class Module(ScreenObject) :

    #All of the modules in the game
    CurrentModulesInGame = []

    #All of the available modules
    AvailableModules = GetImagesByPart("MODULE_")

    #TODO: The solution to the bomb must be show by another puzzle that involves all of the modules (i.e. Have the modules each have their own led color or blink in a certain way)
    AvailableSolvedModules = GetImagesByPart("SOLVED_MODULE")

    #Make sure that the empty module is the first one in the list
    EmptyName = ""
    for ThisModuleName in AvailableModules :
        print(ThisModuleName)
        if "MODULE_EMPTY" in ThisModuleName :
            EmptyName = ThisModuleName

    AvailableModules.remove(EmptyName)
    AvailableModules.insert(0, EmptyName)    

    def __init__(self, ModuleType, X, Y) :

        #Make the screen object
        super().__init__(X, Y, Wires.GetImage(ModuleType), True)

        self.solved = False

        self.GiveCode()
        
        self.Disabled = False

        Module.CurrentModulesInGame.append(self)

    def GetModules(ThisModuleName) :
        ModulesFound = []
        for ThisModule in Module.CurrentModulesInGame :
            if ThisModuleName in ThisModule.Name :
                ModulesFound.append(ThisModule)
        return ModulesFound

    #Gives the correct attributes to the module
    def GiveCode(self) :
        #The module's children dictionary has the image as key and the object as the value

        
        #This module is a wires modules
        if "MODULE_WIRES" in self.GetName():

            #Get all of the available wire types
            AllWires = Wires.WireClass.WireTypes.copy()

            #The displacements of each wire relative to the module
            WireDisplacements = [6, 24, 41, 59]

            NumberOfWires = len(AllWires)
 
            for iterator in range(0, 4) :

                #Randomly order the wires
                RandomNumber = random.randint(0,len(AllWires)-1)
                ThisWire = Wires.WireClass(WireDisplacements[iterator], 5, AllWires.pop(RandomNumber))

                #Convert the pixel coordinates to normalized screen top left
                ThisWire.GetNormalizedScreenCoordinates(self)

                self.Children.append(ThisWire)

   
        elif "MODULE_ARROWS" in self.GetName() :

            #The displacements of the arrows from top left in pixels
            ArrowDisplacements = [(24,1), (51,18), (24,46),(8,18)]

            #Rotation of the arrows relative to the base image (pointed up)
            ArrowRotations = [0, 270, 180, 90]

            #Give the arrows their positions and rotations
            #They are order in this way: UP, RIGHT, DOWN, LEFT
            for ArrowIterator in range(0, len(ArrowDisplacements)) :

                #Construct object. Take arrow displacements X and Y and also add rotation data
                ThisArrow = Arrow(ArrowDisplacements[ArrowIterator][0], ArrowDisplacements[ArrowIterator][1], ArrowRotations[ArrowIterator])

                ThisArrow.GetNormalizedScreenCoordinates(self)

                #Add the arrow to the dictionary
                self.Children.append(ThisArrow)

            #This module has to be solved mutiple times. It is "officially" solved when 0 solves are left
            self.SolvesLeft = 3

            #Add the screen to the module
            TypesOfScreens = ScreenForDot.AvailableScreenTypes.copy()
            ThisScreenForDot = ScreenForDot(26,20,TypesOfScreens[random.randint(0,len(TypesOfScreens)-1)])
            ThisScreenForDot.GetNormalizedScreenCoordinates(self)

            self.Children.append(ThisScreenForDot)

            

        elif "MODULE_BOMB" in self.GetName() :

            #TODO: Rewerite without using .reverse()
            #The positions of all of the timer segments
            TimerSegmentsDisplacements = [(3,26), (10.5,26), (17,26), (24,26), (31,26), (38,26), (45,26), (52,26), (59,26), (66,26)]

            #TimerSegmentsDisplacements.reverse()
            #Add the segments and normalize their coordinates
            for TimerSegmentIterator in range(0,len(TimerSegmentsDisplacements)) :
                ThisTimerSegment = TimerSegment(TimerSegmentsDisplacements[TimerSegmentIterator][0], TimerSegmentsDisplacements[TimerSegmentIterator][1])
                ThisTimerSegment.GetNormalizedScreenCoordinates(self)

                self.Children.append(ThisTimerSegment)


            KeyPadButtonsDisplacements = [(3,44), (11,44), (19,44), (27,44), (35,44), (43,44), (51,44), (59,44), (67,44)]
            AvailableKeyPadButtonTypes = KeyPadButton.KeyPadTypes.copy()

            #Add the key pad buttons and normalize their coordinates
            for KeyPadButtonIterator in range(0,len(KeyPadButtonsDisplacements)) :
                ThisKeyButton = KeyPadButton(KeyPadButtonsDisplacements[KeyPadButtonIterator][0], KeyPadButtonsDisplacements[KeyPadButtonIterator][1], "KEYPAD_SEGMENT_"+str(KeyPadButtonIterator+1)+"_PRESSED")
                ThisKeyButton.GetNormalizedScreenCoordinates(self)
                self.Children.append(ThisKeyButton)
            self.InputtedCode = []

            #The amount of time the bomb has is determined by the game's difficulty
            self.BombTime = 100000/min(1,HookVars.GameDifficulty)

            #The amount of time to add to the bomb for each mistake
            self.TimerPenalty = self.BombTime/10

            #The current amount of time penalty
            self.CurrentTimePenalty = 0

            #The code to disarm this bomb
            self.SecretCode = []

            #The code's length is dependent on how many modules are in the game
            for ModuleCount in range(0,len(Module.CurrentModulesInGame)) :
                self.SecretCode.append(random.randint(1,9))

            print(self.SecretCode)

        #Add the error indicator to the module (A red blinking outline)
        RedOutline = ScreenObject(-1,-1, GetImage("OUTLINE_RED.png"))
        #print(RedOutline.GetName())
        RedOutline.Visible = False
        self.Children.append(RedOutline)

    def GiveBombCode(self, CodeLength) :
        if "MODULE_BOMB" in self.Name :
            self.SecretCode = []
            #The code's length is dependent on how many modules are in the game
            for ModuleCount in range(0,CodeLength) :
                self.SecretCode.append(random.randint(1,9))

            print(self.SecretCode)
       




    def LookupRules(self) :

        if "MODULE_WIRES" in self.GetName():

            #TODO: Replace this temporary solution with led colors for each module
            #self.Image = self.AvailableSolvedModules[self.AvailableBombCodes.pop(0)-1]
            
            ThisModuleWires = self.GetChildren("WIRE_")

            CorrectWire = ""
            if len(ThisModuleWires) > 0 :
                if "WIRE_BLUE" in ThisModuleWires[0].GetName() :
                    CorrectWire = "WIRE_RED"
                elif "WIRE_YELLOW" in ThisModuleWires[0].GetName() :
                    CorrectWire = "WIRE_BLUE"

        elif "MODULE_ARROWS" in self.GetName() :

            ThisModuleArrows = self.GetChildren("ARROW_PRESSED")
            
            ThisModuleScreen = self.GetChildren("DOT_SCREEN_")[0]
            #All of the custom rules for the arrows module reside here
            ThisModuleDots = ThisModuleScreen.GetChildren("DOT_FOR_SCREEN")
            

            ThisModuleAddedScore = 0
            if "GREEN" in ThisModuleScreen.GetName() :
                ThisModuleAddedScore = 1
            elif "RED" in ThisModuleScreen.GetName() :
                ThisModuleAddedScore = 2
            elif "WHITE" in ThisModuleScreen.GetName() :
                ThisModuleAddedScore = 3

            #TODO: add rules.
            #The colors add +1 to the arrows position. Order is blue(+0), green(+1), red(+2) , white(+3). Dictated by the order in the images list      
            #For example, if this module has dot top left and top right visible, if it is blue, press the right arrow. green, the bottom, red the left and white the top
            
            if ThisModuleDots[0].Visible and ThisModuleDots[1].Visible :

                #If the right arrow is pressed (for blue)

                if ThisModuleArrows[ThisModuleAddedScore].Pressed :
                    self.SolvesLeft = self.SolvesLeft - 1
                else :
                    self.Disabled = True

            elif ThisModuleDots[2].Visible and ThisModuleDots[3].Visible :

                #If the down arrow is pressed (for blue)
                if ThisModuleArrows[(ThisModuleAddedScore)].Pressed :
                    self.SolvesLeft = self.SolvesLeft - 1
                else :
                    self.Disabled = True
            
            if self.SolvesLeft <= 0 :
                self.solved = True

        elif "MODULE_BOMB" in self.GetName() :      
                                                                 
            ThisModuleTimerSegments = self.GetChildren("DISPLAY_SEGMENT")
            ThisModuleKeyPadNumbers = self.GetChildren("KEYPAD_SEGMENT")

            
            for ThisKeyPadNumber in ThisModuleKeyPadNumbers :
                
                if ThisKeyPadNumber.Pressed :

                    for KeyNameChar in ThisKeyPadNumber.GetName() :


                        if KeyNameChar.isdigit() :

                            #Add the number in the keypad to the code
                            self.InputtedCode.append(int(KeyNameChar))

  

            if len(self.InputtedCode) > 0 :   
                print(self.SecretCode)
                print(self.InputtedCode)
                if self.InputtedCode[len(self.InputtedCode)-1] != self.SecretCode[len(self.InputtedCode)-1] :
                    self.InputtedCode.pop()

                    #Consistent damage that is better for, well, consistency. More punishing, but multiple bars disappear at once (which makes sense)
                    #HookVars.BombTime = HookVars.BombTime - self.TimerPenalty

                    self.CurrentTimePenalty = self.CurrentTimePenalty + self.TimerPenalty
                    #Relative damage, always 1/10 of time left
                    #HookVars.SetBombTime(HookVars.BombTime/10*9)

                elif len(self.InputtedCode) == len(self.SecretCode) :
                    self.solved = True  

                    for ThisCode in range(0,len(self.InputtedCode)) :
                        if self.InputtedCode[ThisCode] != self.SecretCode[ThisCode] :
                            self.solved = False


            ChildNumber = 1
            for ThisChild in ThisModuleTimerSegments :
                #TimeLeftFactor= 1.0 - (float(pygame.time.get_ticks()))/float(HookVars.BombTime)
                #If the current time is bigger than the portion that the segment represents
                if ThisChild.Visible and (1.0-((HookVars.CurrentTime+self.CurrentTimePenalty)/self.BombTime))*10 < ChildNumber :

                    #Then do not display the segment
                    ThisChild.Visible = False
                ChildNumber = ChildNumber + 1

    def UpdateModule(self, RelativeMouseCoordsIn):

        if self.Disabled :
            #Because the player cannot interact with the module, the last interaction time can be used to set a timer for the error border
            if HookVars.CurrentTime - self.LastInteraction >= 3000 :
                #Enable module again
                self.Disabled = False
                self.GetChildren("OUTLINE_RED")[0].Visible = False
            else :
                if (HookVars.CurrentTime - self.LastInteraction)%500 < 100:
  
                    self.GetChildren("OUTLINE_RED")[0].Visible = not self.GetChildren("OUTLINE_RED")[0].Visible
            #elif (HookVars.CurrentTime - self.LastInteraction) and 


        else :
            if "MODULE_WIRES" in self.Image :

                ThisModuleWires = self.GetChildren("WIRE")

                #Loop through all of the wires
                for ThisWire in ThisModuleWires :
                    MaxPoint = GetMaxPoint(ThisWire.X, ThisWire.Y, ThisWire.Width, ThisWire.Height, self.Width, self.Height)
                        
                    #Check if the mouse is within the bounds of the wire
                    if RelativeMouseCoordsIn[0] > ThisWire.X and RelativeMouseCoordsIn[0] < MaxPoint[0] and RelativeMouseCoordsIn[1] > ThisWire.Y and RelativeMouseCoordsIn[1] < MaxPoint[1] :
                        
                        if HookVars.MousePressed and not ThisWire.Cut :
                            #Cut the wire
                            ThisWire.Cut = True
        
                            ThisWire.Image = GetImage(ThisWire.Image.replace("WIRE_", "WIRECUT_"))


                self.LookupRules()
                

            elif "MODULE_ARROWS" in self.Image :

                ThisModuleArrows = self.GetChildren("ARROW")

                for ThisArrow in ThisModuleArrows :
   
                    MaxPoint = GetMaxPoint(ThisArrow.X, ThisArrow.Y, ThisArrow.Width, ThisArrow.Height, self.Width, self.Height)
                    ThisArrow.Pressed = False

                    #Check if the mouse is within the bounds of the arrow
                    if RelativeMouseCoordsIn[0] > ThisArrow.X and RelativeMouseCoordsIn[0] < MaxPoint[0] and RelativeMouseCoordsIn[1] > ThisArrow.Y and RelativeMouseCoordsIn[1] < MaxPoint[1] :
                        
                        #If the mouse is pressed, the arrow is not already pressed and the last interaction occured 0.5 or more seconds ago, press
                        if HookVars.MousePressed and not ThisArrow.Pressed and HookVars.CurrentTime - self.LastInteraction >= 500  :

                            ThisArrow.Visible = True
                            #The arrow is pressed
                            ThisArrow.Pressed = True

                            self.LookupRules()

                            MyScreen = self.GetChildren("SCREEN")[0]

                            #Randomize the dots
                            for ThisScreenDot in MyScreen.Children:
                                ThisScreenDot.Visible = random.choice([True,False])

                            self.LastInteraction = HookVars.CurrentTime

                    if HookVars.CurrentTime - self.LastInteraction >= 500 :
                        ThisArrow.Visible = False


            elif "MODULE_BOMB" in self.Image :  

                #Bomb module has segments and key pad buttons as children
                ThisModuleKeyPadNumbers = self.GetChildren("KEYPAD_SEGMENT")

                for ThisKeyPadNumber in ThisModuleKeyPadNumbers :
                    MaxPoint = GetMaxPoint(ThisKeyPadNumber.X, ThisKeyPadNumber.Y, ThisKeyPadNumber.Width, ThisKeyPadNumber.Height, self.Width, self.Height)

                    #Immediately set the keypad number being pressed to false, to register the click once
                    ThisKeyPadNumber.Pressed = False

                    #Check if the mouse is within the bounds of the arrpw
                    if RelativeMouseCoordsIn[0] > ThisKeyPadNumber.X and RelativeMouseCoordsIn[0] < MaxPoint[0] and RelativeMouseCoordsIn[1] > ThisKeyPadNumber.Y and RelativeMouseCoordsIn[1] < MaxPoint[1] :
                        
                        #If the mouse is pressed, the arrow is not already pressed and the last interaction occured 0.5 or more seconds ago, press
                        if HookVars.MousePressed and not ThisKeyPadNumber.Pressed and HookVars.CurrentTime - self.LastInteraction >= 500  :
                            ThisKeyPadNumber.Visible = True

                            #The arrow is pressed
                            ThisKeyPadNumber.Pressed = True

                            self.LastInteraction = HookVars.CurrentTime

                    #Visually show that the keypad number can be pressed again afet 0.5 seconds
                    if HookVars.CurrentTime - self.LastInteraction >= 500 :
                        ThisKeyPadNumber.Visible = False

                self.LookupRules()