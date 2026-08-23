"""
These segments show how much time is left on the bomb
"""

from Mods.BaseMod.Sprites.Images import *
from Mods.BaseMod.HookScreenObject import *

class TimerSegment(ScreenObject) :

    def __init__(self, X, Y) :

        #Make the screen object
        super().__init__(X, Y, GetImage("DISPLAY_SEGMENT_ON.png"))
