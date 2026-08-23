"""
ScreenForDots is the screen contained within the dot puzzle that shows all of the dots.
"""

from Mods.BaseMod.Sprites.Images import *
from Mods.BaseMod.HookScreenObject import *
from Mods.BaseMod.HintDots import *
import random

class ScreenForDot(ScreenObject) :
    AvailableScreenTypes = GetImagesByPart("DOT_SCREEN_")
    #print(WireTypes)
    #print("THE WIRE TYPESSSSSSSSSSSSSSSSSSS")
    def __init__(self, X, Y, ScreenType : str) :

        #Make the screen object
        super().__init__(X, Y, GetImage(ScreenType))

        #The displacements for each dot
        DotsDisplacements = [(3,3),(14,3),(3,16),(14,16)]

        #Give the screen its four dots, with random number of dots being visible
        for DotIterator in range(0, 4) :
            self.Children.append(HintDot(DotsDisplacements[DotIterator][0],DotsDisplacements[DotIterator][1]))
            self.Children[DotIterator].GetNormalizedScreenCoordinates(self)
            self.Children[DotIterator].Visible = random.choice([True, False])
            

