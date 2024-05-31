import cv2
import mediapipe as mp
import time
import math
import pygame
import random

# Determines whether or not the distance of pixels between @prev and @current is greater than @tolerance
def hasMoved(prev, current, tolerance):
    if abs(prev.x - current.x) > tolerance or abs(prev.y - current.y) > tolerance:
        return True
    else:
        return False

# Create a new 2D point at the average of @one and @two
def pointAverage(one, two):
    return Point((one.x + two.x) / 2, (one.y + two.y) / 2)

# Calculate a points coordinate relative to the screen (pixel coordinates)
def calculateRelativePoint(point, image):
    return Point(point.x * image.shape[1], point.y * image.shape[0])

# Return the direction of movement from prev -> current
def getDirection(prev, curr, tolerance):
    left = None
    up = None
    # Moving left:
    if curr.x - prev.x > tolerance:
        left = True
    
    # Moving right:
    if curr.x - prev.x < -1 * tolerance:
        left = False
    
    # Moving up:
    if curr.y - prev.y > tolerance:
        up = True
    
    # Moving down:
    if curr.y - prev.y < -1 * tolerance:
        up = False
    
    return (left, up)


# Initialize MediaPipe Hand solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize webcam
cap = cv2.VideoCapture(0)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

prev_center = Point(-1, -1)


# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Dino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 229, 255)
BLUE = (0, 0, 255)
PURPLE = (89, 0, 255)
PINK = (255, 0, 234)

# Game variables
block_size = 30
block_y = SCREEN_HEIGHT - block_size
block_x = 50
block_y_change = 0
gravity = 1
jump_speed = -15
line_width = 20
line_height = random.randint(20, 30)
line_x = SCREEN_WIDTH
line_speed = 10
score = 0
font = pygame.font.Font(None, 36)
# lower = more frequent
line_frequency = 400

# Clock
clock = pygame.time.Clock()

# Initialize font
pygame.font.init()
number_font = pygame.font.Font(None, 28)

def getColor(finger_count):
    match finger_count:
        case 0:
            return RED
        case 1: 
            return ORANGE
        case 2: 
            return BLUE
        case 3: 
            return PURPLE
        case 4: 
            return PINK
        case 5: 
            return GREEN
    return RED
        

# Lines list
lines = []

# Game loop
running = True
while running:
    direction = (None, None)
    screen.fill((74, 74, 74))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    # Display the count of raised fingers
    cv2.putText(image, f'Fingers: {finger_count}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the image
    cv2.imshow('Finger Count', image)

    if direction[1] == True and block_y == SCREEN_HEIGHT - block_size:
        block_y_change = jump_speed

    # Update block
    block_y_change += gravity
    block_y += block_y_change
    if block_y > SCREEN_HEIGHT - block_size:
        block_y = SCREEN_HEIGHT - block_size
        block_y_change = 0

    # Draw block
    pygame.draw.rect(screen, getColor(finger_count), (block_x, block_y, block_size, block_size))

# Update and draw lines
    if not lines or lines[-1]['x'] < SCREEN_WIDTH - line_frequency:  
        line_height = random.randint(20, 30)
        line_number = random.randint(0, 5)
        lines.append({'x': SCREEN_WIDTH, 'height': line_height, 'number': line_number})

    for line in lines[:]:
        line['x'] -= line_speed
        pygame.draw.rect(screen, getColor(line['number']), (line['x'], SCREEN_HEIGHT - line['height'], line_width, line['height']))
        
        # Render and draw number
        number_surface = number_font.render(str(line['number']), True, WHITE)
        screen.blit(number_surface, (line['x'] + line_width // 2 - number_surface.get_width() // 2, SCREEN_HEIGHT - line['height'] // 2 - number_surface.get_height() // 2))

        if line['x'] < -line_width:
            lines.remove(line)
            score += 1
            line_speed += 1

    # Collision detection
    for line in lines:
        if line['x'] < block_x + block_size and line['x'] + line_width > block_x and block_y + block_size > SCREEN_HEIGHT - line['height']:
            if line['number'] != finger_count:
                running = False

    # Display score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

# Close the game window
pygame.quit()

print(f"You scored {score}. Better luck next time!")

# Release the webcam and close OpenCV window
cap.release()
cv2.destroyAllWindows()