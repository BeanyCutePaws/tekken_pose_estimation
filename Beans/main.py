from player import Player # imports the Player class from the player module ( This includes the pose.landmarks and keyboard inputs corresponding to the player's actions)
import cv2 # imports opencv for Computer Vision
import mediapipe as mp # imports MediaPipe for Pose Estimation that detects the body landmarks


# MediaPipe Initialization
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) 
#static_image_mode=False - This ensures that the frames are tracked continuosly and smoothly instead of treating frames separtely
# min_detection_confidence=0.5, min_tracking_confidence=0.5 - this  ensures the accuracy of the detection, it reuire 50% confidence to be detected and it shouldn't drop to 50% otehrwise re-attempt

# Access Webcam 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #Sets the video frame width to 640 pixels
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #Sets the video frame height to 480 pixels
cap.set(cv2.CAP_PROP_FPS, 30) # HELPED BY AI - Sets to 30 frames per second (for less intensive processing of frames)


# Frame Size
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Stores the width of the video frame as am integer
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Stores the height of the video frame as am integer
P_WIDTH, P_HEIGHT = 320, 240 # Stores the width and height for smaller frame size (to process the frames more efficiently)

LEFT_MARGIN_THRESHOLD = int(WIDTH * (1 / 3)) # Threshold for upper body movement to left (LEFT)
RIGHT_MARGIN_THRESHOLD = int(WIDTH * (2 / 3)) # Threshold for upper body movement to right (RIGHT)
CROUCH_THRESHOLD = 260 # Threshold for shoulder point (CROUCH)
NOSE_THRESHOLD = int(HEIGHT * 0.2)  # Threshold for nose point (JUMP)
STAND_THRESHOLD = int(HEIGHT * 0.75) # Standing Threshold

# Movement Direction
MD_STAND = 0 # Status of Standing Position
MD_LEFT = 1 # Status of Moving Left
MD_RIGHT = 2 # Status of Moving Right

# Initialize Player from player module. Creates a player object to be used to get the body landmarks and tekken controls set in the player module
# The video frame's width and height are passed to map out the nmovements within the frame
player = Player(WIDTH, HEIGHT)

# Main Function
def main():
    while cap.isOpened(): #The program will run while the webcam is on
        ret, frame = cap.read() # Captures and reads each frame form the webcam
        if not ret: # The while-loop will stop when no frame is read
            break

        frame = cv2.flip(frame, 1) # Horizontally flips the video frame
        small_frame = cv2.resize(frame, (P_WIDTH, P_HEIGHT)) # Resize the video frame with smaller width and height for a faster and more efficient processing
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB) # Converts small_frame from BGR to RGB to be used for MediaPipe
        results = pose.process(rgb_frame) # MediaPipe pose detection to process and detect the body landmarks

        # If a person is successfully detected, pose landmarks are identified; otherwise, none are detected.
        if results.pose_landmarks is not None:
            cv2.line(frame, (0, CROUCH_THRESHOLD), (WIDTH, CROUCH_THRESHOLD), (255, 255, 0), 2) # Draws the line for Crouch Threshold (for crouching)
            cv2.line(frame, (0, NOSE_THRESHOLD), (WIDTH, NOSE_THRESHOLD), (255, 0, 255), 2) # Draws the line for Nose Threshold (for jumping)
            cv2.line(frame, (LEFT_MARGIN_THRESHOLD, 0), (LEFT_MARGIN_THRESHOLD, HEIGHT), (0, 0, 255), 2) # Draws the line for Left Margin Threshold (for left movement)
            cv2.line(frame, (RIGHT_MARGIN_THRESHOLD, 0), (RIGHT_MARGIN_THRESHOLD, HEIGHT), (255, 0, 0), 2) # Draws the line for Left Margin Threshold (for right movement)
            cv2.putText(frame, 'JUMP', (280, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA) # Places a text for JUMP
            cv2.putText(frame, 'LEFT', (80, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) # Places a text for LEFT
            cv2.putText(frame, 'RIGHT', (460, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA) # Places a text for RIGHT
            cv2.putText(frame, 'CROUCH', (260, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA) # Places a text for CROUCH

            landmarks = results.pose_landmarks.landmark # Extracts the landmark points
            player.update(landmarks) # The player class is updated with the latest landmark positions
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) #This then draws the detected landmarks on teh video frame for visualization

            cv2.circle(frame, (player.MIDDLE_CHEST, player.Y_CHEST), radius=3, color=(0, 0, 255), thickness=3) # Draws a red circle at the computed middle chest (x, y) from the player module, serving as a key point for the MIDDLE CHEST
            check_stance() # Calls the check_stance function which determines if the player is either jumping, crouching, or in a neutral position
            detect_pose(frame) # Calls the detect_pose function, which checks the player's stance (neutral, crouch, or jump) and triggers move() to detect and execute the corresponding Tekken controls 
            if player.cd <= 13: # Cool down timer (0-13) which adds a delay between repeated actions
              player.cd += 1

        cv2.imshow('Tekken Pose Frame', frame) # Displays the Tekken Pose Estimation Video feed with the title "Tekken Pose Frame"

        if cv2.waitKey(10) & 0xFF == ord('q'): # Checks for every 10 milliseconds if q is pressed it will end the loop and stop the program
            break

    # Release the webcam
    cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


# Checks the Player's Stance : CROUCH, JUMP, NEUTRAL
def check_stance():
    

    if player.R_SHOULDER.y * HEIGHT > CROUCH_THRESHOLD and player.L_SHOULDER.y * HEIGHT > CROUCH_THRESHOLD: # Gets the actual pixel position of the Right and Left shoulder points and compares it it to the crouch threshold to look if the shoulder is low enough for crouching 
        print("CROUCHING!")
        if player.STANCE != 1: # If player.STANCE is not equal to the assigned value "1" (crouch), it will update it to 1
            player.STANCE = 1
            player.crouch() # Calls the crouch function from the Player class, triggering the corresponding keyboard input for crouching

    elif player.NOSE.y * HEIGHT < NOSE_THRESHOLD: # Gets the atcual pixel position of the nose point and compares it it to the nose threshold to look if the nose is low enough for jumping
        print("JUMPING!")
        if player.STANCE != 2: # If player.STANCE is not equal to the assigned value "2" (jump), it will update it to 2
            player.STANCE = 2
            player.jump() # Calls the jump function from the Player class, triggering the corresponding keyboard input for jumping
    else:
        print("NEUTRAL!") # Else, if not within the crocuhing or jumping thresholds, the player stance will remain neutral which will update the player.STANCE to '0'
        if player.STANCE != 0:
            player.STANCE = 0
            player.neutral() # Calls the neutral function from the Player class, triggering the corresponding keyboard input for neutral


# TEKKEN CONTROL INPUTS available for each STANCE
def detect_pose(frame):
   
    # neutral stance
    if player.STANCE == 0:
        move(frame) # Calls the move function to execute the corresponding Tekken control based on detected movements

    # crouched stance
    elif player.STANCE == 1:
        move(frame) # Calls the move function to execute the corresponding Tekken control based on detected movements

    # jump stance
    elif player.STANCE == 2:
        move(frame) # Calls the move function to execute the corresponding Tekken control based on detected movements
     
    
# This function processes the frame and detected movements and execute the corresponding TEKKEN CONTROL INPUTS  
def move(frame):
  # neutral stances
    right_arm_extended = (player.R_HAND.x > player.R_SHOULDER.x + 0.2) and (abs(player.R_HAND.y - player.R_SHOULDER.y) < 0.1) # Checks that the right hand is positioned at least 0.2 units farther to the right of the right shoulder, it also checks that the y-axis position difference between the hand and shoulder is within 0.1 to confirm the right arm is horizontally extended 
    left_arm_extended = (player.L_HAND.x < player.L_SHOULDER.x - 0.2) and (abs(player.L_HAND.y - player.L_SHOULDER.y) < 0.1) # Checks that the left hand is positioned at least 0.2 units farther to the left of the left shoulder, it also checks that the y-axis position difference between the hand and shoulder is within 0.1 to confirm the left arm is horizontally extended 
    right_to_left = (player.R_HAND.x < player.L_SHOULDER.x + 0.1) # Checks that the left hand is positioned at least 0.1 units farther to the right of the right shoulder (trigger punch to the left)
    left_to_right = (player.L_HAND.x > player.R_SHOULDER.x - 0.1) # Checks that the left hand is positioned at least 0.1 units farther to the left of the left shoulder (trigger punch to the right)
    left_up = int(player.L_SHOULDER.y * 0.9) < player.L_ELBOW.y < int(player.L_SHOULDER.y * 1.1) or (player.L_ELBOW.y < player.L_SHOULDER.y) and (player.L_ELBOW.y < player.R_ELBOW.y) # Checks whether the left elbow's y-position is within a range 10% above and below the left shoulder. Alternatively, it can also check if the left elbow is positioned higher than both the left shoulder and the right elbow (this is a left upward punch)
    right_up= int(player.R_SHOULDER.y * 0.9) < player.R_ELBOW.y < int(player.R_SHOULDER.y * 1.1) or (player.R_ELBOW.y < player.R_SHOULDER.y) and (player.R_ELBOW.y < player.L_ELBOW.y) # Checks whether the right elbow's y-position is within a range 10% above and below the right shoulder. Alternatively, it can also check if the right elbow is positioned higher than both the right shoulder and the left elbow (this is a right upward punch)
    if (left_up): # If left_up (left upwards punch) is detected then it will call the left_punch function which will trigger the keyboard input for 'Special Move (u)' 
        print("SPECIAL MOVE (U)")
        player.special_move()
    if (right_up): # If right_up (right upwards punch) is detected then it will call the right_punch function which will trigger the keyboard input for 'AIR COMBOS (i)' 
        print("AIR COMBOS (I)")
        player.air_combos()
    if(right_arm_extended ): # If right_arm_extended (right arm extended to the right) is detected then it will call the right_arm_extended function which will trigger the keyboard input for 'Air Combos (j)' 
        print("POWER CRUSH (J)")
        player.power_crush()
    if(left_arm_extended ): # If left_arm_extended (left arm extended to the left) is detected then it will call the left_arm_extended function which will trigger the keyboard input for 'Low Attack/Throws (k)'
        print("LOW ATTACKS / THROWS (K)")
        player.low_throw()
    if right_to_left: # If right_to_left (right punch to left) is detected then it will call the right_to_left function which will trigger the keyboard input for 'Heat Burst (p)' 
        print("HEAT BURST (P)") 
        player.HEAT()
    if (left_to_right): # If left_to_right (left punch to right) is detected then it will call the left_to_right function which will trigger the keyboard input for 'Rage Art (;)' 
        print("RAGE ART (;)")
        player.RAGE()   
    elif (LEFT_MARGIN_THRESHOLD < player.L_EAR.x * WIDTH < player.R_EAR.x * WIDTH < RIGHT_MARGIN_THRESHOLD and LEFT_MARGIN_THRESHOLD < player.MIDDLE_CHEST < RIGHT_MARGIN_THRESHOLD): # Checks if both ears and the middle chest are within the screen's central region, ensuring the player is centered. This triggers the stand function which ensures the player is at standing position
        if player.movement != MD_STAND:
            player.movement = MD_STAND
            player.stand()
            print("STAND")
    elif (player.L_EAR.x * WIDTH < LEFT_MARGIN_THRESHOLD and player.MIDDLE_CHEST < LEFT_MARGIN_THRESHOLD): # Checks if  the left ear and the middle chest are left of the LEFT_MARGIN_THRESHOLD, this calls the move_left function which triggers the player's movement to go left
        if player.movement != MD_LEFT:
            player.movement = MD_LEFT
            player.move_left()
            print("MOVE LEFT")
    elif (player.R_EAR.x * WIDTH > RIGHT_MARGIN_THRESHOLD and player.MIDDLE_CHEST > RIGHT_MARGIN_THRESHOLD): # Checks if  the right ear and the middle chest are left of the RIGHT_MARGIN_THRESHOLD, this calls the move_right function which triggers the player's movement to go right
        if player.movement != MD_RIGHT:
            player.movement = MD_RIGHT
            player.move_right()
            print("MOVE RIGHT")    


    

if __name__ == '__main__':
    main() # Calls the main function