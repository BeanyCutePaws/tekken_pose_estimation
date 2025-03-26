import pydirectinput # This library is imported to use the keyboard inputs to send commands to the tekken game
import time # This is a built-in python module that is used for delays in this program


class Player:
    def __init__(self, WIDTH, HEIGHT): #This constructor method will intitialize the player's body landmarks and the status of otehr variables and will run when Player object is created
        # The body landmarks are initially set to none
        self.NOSE = None
        self.R_EAR = None
        self.L_EAR = None
        self.R_ELBOW = None
        self.L_ELBOW = None
        self.R_SHOULDER = None
        self.L_SHOULDER = None
        self.R_HAND = None
        self.L_HAND = None
        self.STANCE = 0 # Initially set to 0 which is the neutral stance
        self.MIDDLE_CHEST = None
        self.Y_CHEST = None
        self.cd = 13 # Sets the cooldown timer to 13 so that the player can perform a move immediately at the start of the game
        self.movement = 0  # Initially set to 0 which is the stand position
        self.WIDTH = WIDTH # Stores the width of the video frame for mapping and scaling the landmark positions
        self.HEIGHT = HEIGHT # Stores the height of the video frame for mapping and scaling the landmark positions
    def update(self, landmarks): #This method will update the player's body landmarks with the pose landmarks
        self.NOSE = landmarks[0]
        self.R_EAR = landmarks[7]
        self.L_EAR = landmarks[8]
        self.R_ELBOW = landmarks[13]
        self.L_ELBOW = landmarks[14]
        self.R_SHOULDER = landmarks[11]
        self.L_SHOULDER = landmarks[12]
        self.R_HAND = landmarks[15]
        self.L_HAND = landmarks[16]
        self.MIDDLE_CHEST = int((self.L_SHOULDER.x + self.R_SHOULDER.x) * self.WIDTH / 2) # Averages the left and right shoulder's x position to get the middle chest x position
        self.Y_CHEST = int((self.L_SHOULDER.y + self.R_SHOULDER.y) * self.HEIGHT / 2) # Averages the left and right shoulder's y position to get the middle chest y position

    def power_crush(self): # When this function is called, the pyinputdirect module will simulate pressing the j key to execute the power crush
        #if self.cd >= 4:
            pydirectinput.press('j')
           # self.cd = 0

    def low_throw(self): # When this function is called, the pyinputdirect module will simulate pressing the k key to execute the low attacks/throws
        #if self.cd >= 4:
            pydirectinput.press('k')
           # self.cd = 0
    

    def special_move(self): # When this function is called, the pyinputdirect module will simulate pressing the u key to execute the special move
        #if self.cd >= 2:
            pydirectinput.press('u')
           # self.cd = 0

    def air_combos(self): # When this function is called, the pyinputdirect module will simulate pressing the i key to execute the air combos
        #if self.cd >= 2:
            pydirectinput.press('i')
           # self.cd = 0

    def HEAT(self):# When this function is called, the pyinputdirect module will simulate pressing the p key to execute the heat burst
        if self.cd >= 13:
            pydirectinput.press('p')
            self.cd = 0

    def RAGE(self):# When this function is called, the pyinputdirect module will simulate pressing the ; key to execute the rage art
        if self.cd >= 13:
            pydirectinput.press(';')
            self.cd = 0

    def crouch(self): # When this function is called, the pyinputdirect module will simulate holding down the s key to execute the crouching
        pydirectinput.keyDown('s')

    def jump(self): # When this function is called, the pyinputdirect module will simulate briefly holding down the w key for 0.1 seconds and releasing it to execute jump
        pydirectinput.keyDown('w')
        time.sleep(0.1)
        pydirectinput.keyUp('w')

    def neutral(self): # When this function is called, the pyinputdirect module will ensure that the s key is up and not pressed to execute the neutral stance
        pydirectinput.keyUp('s')

    def stand(self):  # When this function is called, the pyinputdirect module will ensure that all  w, a, s and d keys are up and not pressed down to execute a standing position
        pydirectinput.keyUp('s')
        pydirectinput.keyUp('a')  
        pydirectinput.keyUp('d')
        pydirectinput.keyUp('w')

    def move_left(self): # When this function is called, the pyinputdirect module will simulate holding down the a key and ensuring that the d key is not pressed to execute the player's movement to the left
        pydirectinput.keyUp('d')
        pydirectinput.keyDown('a')

    def move_right(self): # When this function is called, the pyinputdirect module will simulate holding down the d key and ensuring that the a key is not pressed to execute the player's movement to the right 
        pydirectinput.keyUp('a')
        pydirectinput.keyDown('d')
    
