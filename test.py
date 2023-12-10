import cv2
import mediapipe as mp
import time
from govee import GoveeClient, Device

client = GoveeClient("ca158097-0f23-4dbf-9e21-df25440146b0")

desk_lights = client.devices[1]
wall_lights = client.devices[0]

# Initialize MediaPipe Hand solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize the time of the last update
last_update_time = 0
update_interval = 1  # Time interval for updates in seconds

prev_count = 0


while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)

    # Check if 5 seconds have passed since the last update
    current_time = time.time()
    
    # Update the finger count
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    finger_count = 0
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            finger_tips = [8, 12, 16, 20]
            middle_joints = [5, 9, 13, 17]
            
            for tip, joint in zip(finger_tips, middle_joints):
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[joint].y:
                    finger_count += 1
            
            # Handle thumb for right hand forwards
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                finger_count += 1

            # Draw the hand landmarks on the image
            mp.solutions.drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    x = finger_count
    if prev_count != x:
        if current_time - last_update_time > update_interval:
            print(x)
            prev_count = x
            last_update_time = current_time
    
    # if finger_count > 1 and prev_open == False:
    #     if current_time - last_update_time > update_interval:
    #         print("ON")
    #         last_update_time = current_time
    #         prev_open = True

    # if finger_count == 1 and prev_open == True:
    #     if current_time - last_update_time > update_interval:
    #         print("OFF")
    #         last_update_time = current_time
    #         prev_open = False
    # elif finger_count > 1:
    #     prev_open = True 

    # Display the count of raised fingers
    cv2.putText(image, f'Fingers: {finger_count}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the image
    cv2.imshow('Finger Count', image)

    # Break loop on pressing 'q'
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV window
cap.release()
cv2.destroyAllWindows()
