# Handtracking Colormatch Game
  Built using **PyGame**, **OpenCV**, and **Mediapipe**.

Requires a working webcam.


## Build
First, install the required libraries:
```
pip install -r requirements.txt
```
## Run
Run the game file
```
python/python3 colormatch.py
```
## How the Game Works
You play as a colored cube moving against oncoming different colored blocks. For every block you collide with, you must be holding up the same amount of fingers as the number displayed on the block (you must match your color to the color of any incoming block). The game gets progressively harder with every point scored. 

The backend uses openCV and mediapipe to process your webcam feed and track your hand. 

![alt text](https://github.com/Sxzo/Handtracking-Colormatch/blob/main/handtrack.png?raw=true)

From there, the game runs with if conditions in a PyGame loop to update the game screen. 

Here's a gameplay example:

![alt text](https://github.com/Sxzo/Handtracking-Colormatch/blob/main/colormatch_gameplay.mp4?raw=true)








