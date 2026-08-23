"""
ScreenObjects are the link between the game engine and the logic system. They are placed in a different python file because of circular references problems
"""

from Mods.BaseMod.Sprites.Images import *

class ScreenObject :

    #Stores all of the screen objects. Does not include children screen objects.
    ScreenObjectsArray = []

    def __init__(self, X : float, Y : float, Image, IsParent = False) :

        #The X and Y coordinate to draw to. They are position in the top left. From -1 to 1 (normalized screen coordinates)
        self.X = X
        self.Y = Y

        #The image of the ScreenObject. Not an actual image, just the diretory of that image
        self.Image = Image

        #The height and width of the ScreenObject, in pixels. NOT NORMALIZED
        WidthHeight = GetImageWidthHeight(Image)
        self.Width = WidthHeight[0]
        self.Height = WidthHeight[1]

        #The ScreenObject's children. The X and Y coordinates of them will be relative to the top left of the parent ScreenObject
    
        self.Children = []

        #The rotation of the ScreenObject
        self.Rotation = 0

        #If this ScreenObject is to be rendered or not
        self.Visible = True

        #The time of the last interaction by the user 
        self.LastInteraction = 0.0

        #The name of the ScreenObject is the .png image that it has
        self.Name = self.GetName()

        #If this screen object has children, then add it to the array
        if IsParent :
            #Add this ScreenObjet to the array. These ScreenObjects have no parent
            ScreenObject.ScreenObjectsArray.append(self)

    #TODO: Rename to SetNormalizedScreenCoordinates
    def GetNormalizedScreenCoordinates(self, ParentScreenObject) :
        #self.X = (self.X/ParentScreenObject.Width*2) - 1
        self.X = (self.X/ParentScreenObject.Width- 0.5)*2
        #self.Y = 1.0 - (self.Y/ParentScreenObject.Height*2)
        self.Y = (self.Y/ParentScreenObject.Height - 0.5)*2

    #TODO: Rename to GetNormalizedScreenCoordinates
    def ReturnNormalizedScreenCoordinates(self, WidthHeight) :
        return ((self.X/WidthHeight[0]- 0.5)*2, (self.Y/WidthHeight[1] - 0.5)*2)

    def GetName(self) :
        self.Name = self.Image.split("/").pop()
        return self.Name

        #Returns the children that have a name that include ValueIn
    def GetChildren(self, NameIn : str) :

        #An array of the children that have a name that include ValueIn
        ChildrenFound = []

        #Loop through all of the children
        for ThisChild in self.Children :

            #Having an "in" allows to get multiple similar children. Very useful when having a module that has children that have different behaviors
            if NameIn in ThisChild.GetName() :
                ChildrenFound.append(ThisChild)

        return ChildrenFound