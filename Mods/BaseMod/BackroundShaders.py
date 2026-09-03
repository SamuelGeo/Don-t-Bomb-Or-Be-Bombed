from Mods.BaseMod.HookScreenObject import ScreenObject
from Mods.BaseMod.HookVariables import GlobalProperties as GP
from Mods.BaseMod.Modules import Module
import random

import math

"""
The backround shader playing during the game. Is a glorified function (the f(x) kind).
"""

#NOTE: This code could have been directly inserted into the hook functions, but the file would have been too long

#The currently selected shader
SelectedShader = 1

#The number of shaders available. Treat as len()
NumberOfShaders = 2

#The number of frames per second that each shader is running at
ShaderFPS = 60

#Represents the resolution of the shader along one of its axis. Determined by if the other axis will have a resolution smaller than what ShadersResolution says.
#3rd september 2026 12:26AM : The limit at the moment is 150 pixels. Used 7.6/7.6 gigs of avilable RAM.
ShadersResolution = 150

def SetBackroundShader(Value) :
    global SelectedShader
    SelectedShader = Value



def CalculateShader(SurfaceSize, TimeIn) :

    OutputShader = []

    def mix(A : float, B : float, T :float) :
        return A * (1.0 - T) + B * T

    def smoothstep (edge0, edge1, X) :
        t = max(0.0, min((X - edge0) / (edge1 - edge0), 1.0))
        return t * t * (3.0 - 2.0*t)

    if SelectedShader == 0 :

        ThisBombModule = Module.GetModules("MODULE_BOMB")[0]
                
        TimeLeftFactor= 1.0 - (ThisBombModule.CurrentTimePenalty + TimeIn)/float(ThisBombModule.BombTime)
                
        for PosY in range(0,SurfaceSize[1]) :
            OutPutShaderRow = []
            for PosX in range(0,SurfaceSize[0]) :
                uvX = PosX/SurfaceSize[0]
                uvY = PosY/SurfaceSize[1]       


                PixelColorR = (0.5 + 0.5*math.cos(TimeIn/1000+uvX))*TimeLeftFactor
                PixelColorG = (0.5 + 0.5*math.cos(TimeIn/1000+uvY+2))*TimeLeftFactor
                PixelColorB = (0.5 + 0.5*math.cos(TimeIn/1000+uvX+4))*TimeLeftFactor
                OutPutShaderRow.append([PixelColorR*255, PixelColorG*255, PixelColorB*255])
                
            OutputShader.append(OutPutShaderRow)


    #https://www.shadertoy.com/view/XXtBRr
    elif SelectedShader == 1:

        SPIN_ROTATION = -2.0
        SPIN_SPEED = 7.0
        OFFSET = (0.0, 0.0)
        COLOUR_1 = (0.871, 0.267, 0.231, 1.0)
        COLOUR_2 = (0.0, 0.42, 0.706, 1.0)
        COLOUR_3 = (0.086, 0.137, 0.145, 1.0)
        CONTRAST = 3.5
        LIGTHING = 0.4
        SPIN_AMOUNT = 0.25
        PIXEL_FILTER = 745.0
        SPIN_EASE = 1.0
        PI = 3.14159265359
        IS_ROTATE = False 

        ScreenSize = math.sqrt(SurfaceSize[0]*SurfaceSize[0] + SurfaceSize[1]*SurfaceSize[1])

        pixel_size = ScreenSize / PIXEL_FILTER
        pixel_size = 1.0

        ThisBombModule = Module.GetModules("MODULE_BOMB")[0]
        
        TimeLeftFactor= 1.0 - (ThisBombModule.CurrentTimePenalty + TimeIn)/float(ThisBombModule.BombTime)


        for PosY in range(0,SurfaceSize[1]) :
            OutPutShaderRow = []
            for PosX in range(0,SurfaceSize[0]) :

                uvX = (math.floor(PosX*(1.0/pixel_size))*pixel_size - 0.5*SurfaceSize[0])/ScreenSize - OFFSET[0]
                uvY = (math.floor(PosY*(1.0/pixel_size))*pixel_size - 0.5*SurfaceSize[1])/ScreenSize - OFFSET[0]

                uvLen = math.sqrt(uvX*uvX + uvY*uvY)

                speed = SPIN_ROTATION*SPIN_EASE*0.2

                if (IS_ROTATE) :
                    speed = TimeIn/1000 * speed

                speed = speed + 302.2

                NewPixelAngle = math.atan2(uvY, uvX) + speed - SPIN_EASE*20.0*(1.0*SPIN_AMOUNT*uvLen + (1.0 - 1.0*SPIN_AMOUNT))

                MidX = (SurfaceSize[0]/ScreenSize)/2
                MidY = (SurfaceSize[1]/ScreenSize)/2

                uvX = uvLen*math.cos(NewPixelAngle) 
                uvY = uvLen*math.sin(NewPixelAngle)

                uvX = uvX*30.0
                uvY = uvY*30.0

                speed = TimeIn/1000*SPIN_SPEED

                uv2X = uvX
                uv2Y = uvY

                for iterator in range(0,6) :
                    uv2X = uv2X + math.sin(max(uvX,uvY)) + uvX
                    uv2Y = uv2Y + math.sin(max(uvX,uvY)) + uvY

                    uvX = uvX + 0.5*math.cos(5.1123314 + 0.353*uv2Y + speed*0.131121)
                    uvY = uvY + math.sin(uv2X - 0.113*speed)

                    olduvX = uvX
                    olduvY = uvY

                    uvX = uvX - 1.0*math.cos(olduvX + olduvY) - 1.0*math.sin(olduvX*0.711 - olduvY)
                    uvY = uvY - 1.0*math.cos(olduvX + olduvY) - 1.0*math.sin(olduvX*0.711 - olduvY)

                ContrastMod = 0.25*CONTRAST + 0.5*SPIN_AMOUNT + 1.2
                PaintRes = min(2.0, max(0.0, math.sqrt(uvX*uvX + uvY*uvY)*0.035*ContrastMod))
                c1p = max(0.0, 1.0 - ContrastMod*abs(1.0-PaintRes))
                c2p = max(0.0, 1.0 - ContrastMod*abs(PaintRes))
                c3p = 1.0 - min(1.0, c1p + c2p)
                Light = (LIGTHING - 0.2)*max(c1p*5.0 - 4.0, 0.0) + LIGTHING*max(c2p*5.0 - 4.0, 0.0)

                PixelColorR = min(1.0,(0.3/CONTRAST)*COLOUR_1[0] + (1.0 - 0.3/CONTRAST)*(COLOUR_1[0]*c1p + COLOUR_2[0]*c2p + c3p*COLOUR_3[0]) + Light)
                PixelColorG = min(1.0,(0.3/CONTRAST)*COLOUR_1[1] + (1.0 - 0.3/CONTRAST)*(COLOUR_1[1]*c1p + COLOUR_2[1]*c2p + c3p*COLOUR_3[1]) + Light)
                PixelColorB = min(1.0,(0.3/CONTRAST)*COLOUR_1[2] + (1.0 - 0.3/CONTRAST)*(COLOUR_1[2]*c1p + COLOUR_2[2]*c2p + c3p*COLOUR_3[2]) + Light)

                PixelColorR = PixelColorR*TimeLeftFactor
                PixelColorG = PixelColorG*TimeLeftFactor
                PixelColorB = PixelColorB*TimeLeftFactor


                OutPutShaderRow.append([PixelColorR*255, PixelColorG*255, PixelColorB*255])
                            
            OutputShader.append(OutPutShaderRow)

    #https://www.shadertoy.com/view/tdG3Rd
    elif SelectedShader == 2 :

        ThisBombModule = Module.GetModules("MODULE_BOMB")[0]
        
        TimeLeftFactor= 1.0 - (ThisBombModule.CurrentTimePenalty + TimeIn)/float(ThisBombModule.BombTime)



        def colormap_red(X) :
            if X < 0.0 :
                return 54.0/255.0
            elif X < 20049.0 / 82979.0 :
                return (829.79 * X + 54.51) / 255.0
            else :
                return 1.0

        def colormap_green(X) :
            if X < 20049.0 / 82979.0:
                return 0.0
            elif X < 327013.0 / 810990.0 :
                return (8546482679670.0 / 10875673217.0 * X - 2064961390770.0 / 10875673217.0) / 255.0
            elif X <= 1.0 :
                return (103806720.0 / 483977.0 * X + 19607415.0 / 483977.0) / 255.0
            else :
                return 1.0          

        def colormap_blue(X) :
            if X < 0.0:
                return 54.0 / 255.0
            elif X < 7249.0 / 82979.0 :
                return (829.79 * X + 54.51) / 255.0
            elif X < 20049.0 / 82979.0 :
               return 127.0 / 255.0
            elif X < 327013.0 / 810990.0 :
               return (792.02249341361393720147485376583 * X - 64.364790735602331034989206222672) / 255.0
            else :
                return 1.0  

        def colormap(X) :

            return [colormap_red(X), colormap_green(X), colormap_blue(X), 1.0]

        def rand(nX, nY) :
            WholeValue = math.sin((nX*12.9898 + nY*4.1414))* 43758.5453
            return WholeValue - math.floor(WholeValue)


        def noise(pX, pY) :
            ipX = math.floor(pX)
            ipY = math.floor(pY)

            uX = pX - math.floor(pX)
            uY = pY - math.floor(pY)

            uX = uX*uX*(3.0-2.0*uX)
            uY = uY*uY*(3.0-2.0*uY)

            FirstInterpolation = mix(rand(ipX, ipY), rand(ipX + 1.0, ipY), uX)
            SecondInterpolation = mix(rand(ipX + 0.0, ipY + 1.0), rand(ipX + 1.0, ipY + 1.0), uX)
            ThirdInterpolation = mix(FirstInterpolation, SecondInterpolation, uY)

            return ThirdInterpolation*ThirdInterpolation

        def fbm(pX, pY) :
            f = 0.0

            f = f + 0.500000*noise(pX + TimeIn/1000.0, pY + TimeIn/1000.0); 

            OldpX = pX
            pX = (0.80*pX - 0.60*pY)*2.02
            pY = (0.60*OldpX + 0.80*pY)*2.02
           
            f = f + 0.031250*noise(pX, pY)

            OldpX = pX
            pX = (0.80*pX - 0.60*pY)*2.01
            pY = (0.60*OldpX + 0.80*pY)*2.01

            f = f + 0.250000*noise(pX, pY)

            OldpX = pX
            pX = (0.80*pX - 0.60*pY)*2.03
            pY = (0.60*OldpX + 0.80*pY)*2.03

            f = f + 0.125000*noise(pX, pY)

            OldpX = pX
            pX = (0.80*pX - 0.60*pY)*2.01
            pY = (0.60*OldpX + 0.80*pY)*2.01

            f = f + 0.062500*noise(pX, pY)

            OldpX = pX
            pX = (0.80*pX - 0.60*pY)*2.04
            pY = (0.60*OldpX + 0.80*pY)*2.04

            f = f + 0.015625*noise(pX + math.sin(TimeIn/1000.0), pY + math.sin(TimeIn/1000.0))

            return f/0.96875

        def pattern(pX, pY) :
            FirstFBM = fbm(pX, pY)
            
            pX = pX + FirstFBM
            pY = pY + FirstFBM

            SecondFBM = fbm(pX, pY)
            
            pX = pX + SecondFBM
            pY = pY + SecondFBM

            ThirdFBM = fbm(pX, pY)

            return ThirdFBM

        for PosY in range(0,SurfaceSize[1]) :
            OutPutShaderRow = []
            for PosX in range(0,SurfaceSize[0]) :
                uvX = PosX/SurfaceSize[0]
                uvY = PosY/SurfaceSize[0]       

                shade = pattern(uvX, uvY)

                ThisColormap = colormap(shade)

                PixelColorR = min(1.0,ThisColormap[0])*TimeLeftFactor
                PixelColorG = min(1.0,ThisColormap[1])*TimeLeftFactor
                PixelColorB = min(1.0,ThisColormap[2])*TimeLeftFactor

                OutPutShaderRow.append([PixelColorR*255, PixelColorG*255, PixelColorB*255])
                
            OutputShader.append(OutPutShaderRow)

    #https://www.shadertoy.com/view/WtjyzR
    elif SelectedShader == 3 :

        ThisBombModule = Module.GetModules("MODULE_BOMB")[0]
                
        TimeLeftFactor= 1.0 - (ThisBombModule.CurrentTimePenalty + TimeIn)/float(ThisBombModule.BombTime)

        NUM_LAYERS = 4
        ITER = 23

        def tex(pX, pY, pZ) :
            t = TimeIn/1000 + 78.0
            pW = 3.0*math.sin(t*0.1)
            decX = 1.0 + 0.06*math.cos(t*0.1)
            decY = 0.9 + 0.0
            decZ = 0.1 + 0.0
            decW = 0.15 + 0.14*math.cos(t*0.23)

            for iterator in range(0, ITER) :
                dotProd = pX*pX + pY*pY + pZ*pZ + pW*pW 
                pX = abs(pX/dotProd - decX)
                pY = abs(pY/dotProd - decY)
                pZ = abs(pZ/dotProd - decZ)
                pW = abs(pW/dotProd - decW)

            return [pX, pY, pZ, pW]

        
               
        for PosY in range(0,SurfaceSize[1]) :
            OutPutShaderRow = []
            for PosX in range(0,SurfaceSize[0]) :

                ScreenSize = math.sqrt(SurfaceSize[0]*SurfaceSize[0] + SurfaceSize[1]*SurfaceSize[1])

                uvX = (PosX-SurfaceSize[0]*0.5)/SurfaceSize[1]
                uvY = (PosY-SurfaceSize[1]*0.5)/SurfaceSize[1]  
                colX = 0.0
                colY = 0.0
                colZ = 0.0
                t = TimeIn/1000*0.3
                fractiterator = 0.0

                for iterator in range(0, NUM_LAYERS + 1) :

                    fractiterator = fractiterator + 1.0/NUM_LAYERS

                    d = fractiterator+t - math.floor(fractiterator+t)

                    s = mix(5.0, 0.5, d) 
                    f = d * smoothstep(1.0, 0.9, d)
                    texture = tex(uvX*s, uvY*s, fractiterator*4.0)
                    colX = colX + texture[0]*f
                    colY = colY + texture[1]*f
                    colZ = colZ + texture[2]*f

                colX = colX / NUM_LAYERS * 2.0
                colY = colY / NUM_LAYERS * 1.0
                colZ = colZ / NUM_LAYERS * 2.0

                colX = math.pow(colX, 0.5)
                colY = math.pow(colY, 0.5)
                colZ = math.pow(colZ, 0.5)

                
                PixelColorR = min(1.0,colX)*TimeLeftFactor
                PixelColorG = min(1.0,colY)*TimeLeftFactor
                PixelColorB = min(1.0,colZ)*TimeLeftFactor
                OutPutShaderRow.append([PixelColorR*255, PixelColorG*255, PixelColorB*255])
                
            OutputShader.append(OutPutShaderRow)
    return OutputShader

#The frames are a list of lists of RGB values
def DifferencyScore(Frame1, Frame2) :

    Score = 0.0
    NumberOfComparisons = 0


    for PosY in range(0, len(Frame1)) :
        for PosX in range(0, len(Frame1[PosY])) :

            #Calculate the difference between each pixel
            Score = Score + abs(Frame1[PosY][PosX][0] - Frame2[PosY][PosX][0]) + abs(Frame1[PosY][PosX][1] - Frame2[PosY][PosX][1]) + abs(Frame1[PosY][PosX][2] - Frame2[PosY][PosX][2])
            NumberOfComparisons = NumberOfComparisons + 3

    #print("SCORE COMPONENTS", Score, Score/255, NumberOfComparisons, Score/NumberOfComparisons, Score/255/NumberOfComparisons)

    #Normalize the score by making all of the rgb values go from 0,255 to 0,1 and also divide by the amount of comparisons to get the average value
    return (Score/255.0) / (NumberOfComparisons)

def LoadShader(ShaderIndex, SurfaceSize) :
    
    SetBackroundShader(ShaderIndex)
    

    StoredFrames = []

    TimeIncrementor = (1.0/ShaderFPS)*1000.0
    
    SimulatedTime = 0.0

    InitialFrame1 = CalculateShader(SurfaceSize, SimulatedTime)

    #Add one frame and also convert to microseconds
    SimulatedTime = SimulatedTime + TimeIncrementor
    InitialFrame2 = CalculateShader(SurfaceSize, SimulatedTime)

    SimulatedTime = SimulatedTime + TimeIncrementor
    InitialFrame3 = CalculateShader(SurfaceSize, SimulatedTime)


    StoredFrames.append(InitialFrame1)
    StoredFrames.append(InitialFrame2)
    StoredFrames.append(InitialFrame3)       


    SimulatedTime = SimulatedTime + TimeIncrementor
    NewFrame1 = CalculateShader(SurfaceSize, SimulatedTime)

    SimulatedTime = SimulatedTime + TimeIncrementor
    NewFrame2 = CalculateShader(SurfaceSize, SimulatedTime)

    SimulatedTime = SimulatedTime + TimeIncrementor
    NewFrame3 = CalculateShader(SurfaceSize, SimulatedTime)      

    StoredFrames.append(NewFrame1)
    StoredFrames.append(NewFrame2)
    StoredFrames.append(NewFrame3)       
    #print(DifferencyScore(NewFrame1 , InitialFrame1), DifferencyScore(NewFrame2 , InitialFrame2), DifferencyScore(NewFrame3 , InitialFrame3), SimulatedTime)

    DiffScore1 = DifferencyScore(NewFrame1 , InitialFrame1)
    DiffScore2 = DifferencyScore(NewFrame2 , InitialFrame2)
    DiffScore3 = DifferencyScore(NewFrame3 , InitialFrame3)

    #print(DiffScore1, DiffScore2, DiffScore3)
    # ( DiffScore1 >= 0.03 and DiffScore2 >= 0.03 and DiffScore3 >= 0.03) and 
    while (( DiffScore1 >= 0.03 and DiffScore2 >= 0.03 and DiffScore3 >= 0.03) and SimulatedTime <= 15000.0) or SimulatedTime <= 1000.0:

        #print(DifferencyScore(NewFrame1 , InitialFrame1), DifferencyScore(NewFrame2 , InitialFrame2), DifferencyScore(NewFrame3 , InitialFrame3), SimulatedTime)

        SimulatedTime = SimulatedTime + TimeIncrementor

        #Increment each frame by one
        NewFrame1 = NewFrame2
        NewFrame2 = NewFrame3
        NewFrame3 = CalculateShader(SurfaceSize, SimulatedTime)

        DiffScore1 = DifferencyScore(NewFrame1 , InitialFrame1)
        DiffScore2 = DifferencyScore(NewFrame2 , InitialFrame2)
        DiffScore3 = DifferencyScore(NewFrame3 , InitialFrame3)

        #print(DiffScore1, DiffScore2, DiffScore3, SimulatedTime)

        #Add the new frame
        StoredFrames.append(NewFrame3)
    #print (len(StoredFrames))
    return StoredFrames