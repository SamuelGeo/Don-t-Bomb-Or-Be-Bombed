"""
These key pad buttons show what key pad buttons have been pressed
"""

from Mods.BaseMod.Sprites.Images import *
from Mods.BaseMod.HookScreenObject import *

class KeyPadButton(ScreenObject) :

    KeyPadTypes = GetImagesByPart("KEYPAD_SEGMENT_")
    def __init__(self, X, Y, KeyButtonType : str) :

        #Make the screen object
        super().__init__(X, Y, GetImage(KeyButtonType))

        #By default, the keypad keys are not pressed
        self.Visible = False

        #If the key button has been pressed or not
        self.Pressed = False