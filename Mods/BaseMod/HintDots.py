"""
Dots are used for a puzzle. They are served to show hints during the arrow puzzle
"""

from Mods.BaseMod.Sprites.Images import *
from Mods.BaseMod.HookScreenObject import *

class HintDot(ScreenObject) :

    def __init__(self, X, Y) :
        #Make the screen object
        super().__init__(X, Y, GetImage("DOT_FOR_SCREEN.png"))


