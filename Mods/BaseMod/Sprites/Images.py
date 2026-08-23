"""
Helps with image management
"""


import os
import tkinter

#Returns the image specified
def GetImage(ImageName : str) :
    if os.path.exists(os.path.join(os.path.dirname(__file__), ImageName + ".png")) :
        return os.path.join(os.path.dirname(__file__), ImageName + ".png")
    
    elif os.path.exists(os.path.join(os.path.dirname(__file__), ImageName)) :
        return os.path.join(os.path.dirname(__file__), ImageName)

    elif os.path.exists(ImageName) :
        return ImageName
    
    else :
        return None

#Returns all of the images that contain the inputed name
def GetImagesByPart(NamePart : str) :

    #The list of images that will be exported
    ImagesList = []
    #Loop through each file name in the directory
    for ImageName in os.listdir(os.path.dirname(__file__)) :
        #If the file's name contains the inputed name
        if NamePart in ImageName :
            #Add the Image to the image list
            ImagesList.append(os.path.join(os.path.dirname(__file__), ImageName))
            print()

    #If no images have been found, return nothing
    if len(ImagesList) == 0 :
        return None
    
    return ImagesList

def GetImageWidthHeight(ImageName : str) :
    #Make sure that you can actually get an image
    
    ImageName = GetImage(ImageName)

    #If the image does not exist, return nothing
    if ImageName is None :
        return None
    else :
        root = tkinter.Tk()
        root.withdraw()
        ThisImage = tkinter.PhotoImage(file = ImageName)
        WidthHeight = (ThisImage.width(), ThisImage.height())
        root.destroy()
        return (WidthHeight)
        
    
        
