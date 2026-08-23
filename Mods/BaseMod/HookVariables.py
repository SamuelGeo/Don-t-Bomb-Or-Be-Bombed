#TODO: Make all of the hook variable import from hooks to hook variables

#Have to use a class in order to make getters and setters for the variables implicit. A.k.a. not having to use get_ and set_
#Cool thing is that the only thing that has to be imported from this file the is the GlobalProperties object.
class GlobalPropertiesClass :

    #The coordinates of the mouse on the game surface, in pixels
    _MouseCoords = [0,0]

    #True: mouse is pressed
    _MousePressed = False

    #Which buttons have been pressed (True if pressed) in order: Red, Green, Blue
    _ButtonsPressed = [False, False, False]

    #The distance measured from the ultrasonic sensor in cm
    _DistanceMesured = 10000

    #True if the board has been tilted
    _Tilted = False

    #The keypad inputs. A combination of X (the first four bools) and Y (the rest) booleans shows what has been pressed.
    _KeyPadInputs = [False, False, False, False, False, False, False, False]

    #The game window's width and height in pixels
    _GameWindowWidthHeight = (0,0)

    #The amount of time since launching the game, in milliseconds
    _CurrentTime = 0.0

    #The game difficulty, each +1 represents more difficulty, with added modules
    _GameDifficulty = 0

    #0: The game is playing
    #1: The game is won
    #2: The game is lost
    _GameState = 0


    @property
    def MouseCoords(self) :
        return self._MouseCoords

    @MouseCoords.setter
    def MouseCoords(self, value) :
        self._MouseCoords = value


    @property
    def MousePressed(self) :
        return self._MousePressed

    @MousePressed.setter
    def MousePressed(self, value) :
        self._MousePressed = value


    @property
    def ButtonsPressed(self) :
        return self._ButtonsPressed

    @ButtonsPressed.setter
    def ButtonsPressed(self, value) :
        self._ButtonsPressed = value


    @property
    def DistanceMesured(self) :
        return self._DistanceMesured

    @DistanceMesured.setter
    def DistanceMesured(self, value) :
        self._DistanceMesured = value


    @property
    def Tilted(self) :
        return self._Tilted

    @Tilted.setter
    def Tilted(self, value) :
        self._Tilted = value


    @property
    def KeyPadInputs(self) :
        return self._KeyPadInputs

    @KeyPadInputs.setter
    def KeyPadInputs(self, value) :
        self._KeyPadInputs = value


    @property
    def GameWindowWidthHeight(self) :
        return self._GameWindowWidthHeight

    @GameWindowWidthHeight.setter
    def GameWindowWidthHeight(self, value) :
        self._GameWindowWidthHeight = value


    @property
    def CurrentTime(self) :
        return self._CurrentTime

    @CurrentTime.setter
    def CurrentTime(self, value) :
        self._CurrentTime = value


    @property
    def GameDifficulty(self) :
        return self._GameDifficulty

    @GameDifficulty.setter
    def GameDifficulty(self, value) :
        self._GameDifficulty = value

    
    @property
    def GameState(self) :
        return self._GameState

    @GameState.setter
    def GameState(self, value) :
        self._GameState = value

GlobalProperties = GlobalPropertiesClass()
