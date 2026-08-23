"""
Wires are a module puzzle. They can be cut and that's about it.
"""

from Mods.BaseMod.Sprites.Images import *
from Mods.BaseMod.HookScreenObject import *

class WireClass(ScreenObject) :
    WireTypes = GetImagesByPart("WIRE_")
    #print(WireTypes)
    #print("THE WIRE TYPESSSSSSSSSSSSSSSSSSS")
    def __init__(self, X, Y, WireType : str) :

        #Make the screen object
        super().__init__(X, Y, GetImage(WireType))

        self.Cut = False

