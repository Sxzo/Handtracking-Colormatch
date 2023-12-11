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
You play as a colored cube moving against oncoming different colored blocks. For every block you collide with, you must be holding up the same amount of fingers as the number displayed on the block (you must match your color to the color of any incoming block). 

The backend uses openCV and mediapipe to process your webcam feed and track your hand. 

From there, the game runs with simplistic if conditions in a PyGame loop to update the game screen. 







