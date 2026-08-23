"""
Wires are a module puzzle. They can be pressed and that's about it.
"""

from Mods.BaseMod.Sprites.Images import *
from Mods.BaseMod.HookScreenObject import *

class Arrow(ScreenObject) :

    def __init__(self, X, Y, Rotation) :
        #Make the screen object
        super().__init__(X, Y, GetImage("ARROW_PRESSED.png"))

        #Rotation in degrees
        self.Rotation = Rotation

        #If the arrow is pointing left or right, rotate the bounding box
        if self.Rotation == 90 or self.Rotation == 270:
            HoldWidth = self.Width
            self.Width = self.Height
            self.Height = self.Width
        self.Visible = False
        
        #If this button has been pressed or not
        self.Pressed = False

