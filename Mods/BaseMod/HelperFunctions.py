"""
Some miscelanious helper functions
"""
#The X and Y are screen coordinates and the Width and the Height are in pixels
def GetNormalizedCoordinates(X, Y, Width, Height) :
    return [((X/Width- 0.5)*2), ((Y/Height- 0.5)*2)]

#X and Y in normalized screen coordinates
def GetScreenCoordinates(X, Y, Width, Height) :
    return[(X/2.0 + 0.5)*Width,(Y/2.0 + 0.5)*Height]

#Gets the max point when the position is in normalized coordinates and the width and height in pixels
def GetMaxPoint(X, Y, ObjectWidth, ObjectHeight, Width, Height) :
        
        #Get the screen coordinate versions of the normalized positions
        MaxPoint = GetScreenCoordinates(X, Y, Width, Height)

        #Calculate the screen coordinates of the max point
        MaxPoint[0] = MaxPoint[0] + ObjectWidth
        MaxPoint[1] = MaxPoint[1] + ObjectHeight

        #Calculate the normalized coordinates of the point
        return GetNormalizedCoordinates(MaxPoint[0], MaxPoint[1], Width, Height)