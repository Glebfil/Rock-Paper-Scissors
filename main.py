import cv2
import mediapipe as mp
import numpy as np
import time
import random

def get_points(landmark, shape):
    points = []
    for mark in landmark:
        points.append([mark.x * shape[1], mark.y * shape[0]])
    return np.array(points, dtype=np.int32)


def palm_size(landmark, shape):
    x1, y1 = landmark[0].x * shape[1], landmark[0].y * shape[0]
    x2, y2 = landmark[9].x * shape[1], landmark[5].y * shape[0]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


def palm_size2(landmark, shape):
    x1, y1 = landmark[0].x * shape[1], landmark[0].y * shape[0]
    x2, y2 = landmark[13].x * shape[1], landmark[5].y * shape[0]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


def hand_detector():
    handsDetector = mp.solutions.hands.Hands()
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    if results.multi_hand_landmarks is not None:
        d = get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        (x, y), r = cv2.minEnclosingCircle(get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape))
        a = np.array([d[0], d[16], d[20]])
        (x2, y2), r2 = cv2.minEnclosingCircle(a)
        ws = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        ws2 = palm_size2(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        if 2 * r / ws > 1.9 and 2 * r2 / ws2 < 1:
            return "Scissors"
        elif 2 * r / ws > 1.8:
            return "Paper"
        elif 2 * r / ws < 1.5:
            return "Rock"

    handsDetector.close()


print("Greeting Player! Welcome to the Rock-Paper-Scissors game with the computer. To play you should write +:")
c = input()
while True:
    r = random.choice(["Rock", "Paper", "Scissors"])
    if c == "+":
        print("Ok, you are ready to play. In a second I will start writing Rock, Paper, Scissors and when I will print SHOOT! you should show your sign.")
        time.sleep(7)
        print("Rock")
        time.sleep(2)
        print("Paper")
        time.sleep(2)
        print("Scissors")
        time.sleep(2)
        print("SHOOT!")
        h = hand_detector()
        print(h)
        if r == h:
            print("Draw!")
        elif (r == "Rock" and h == "Scissors") or (r == "Scissors" and h == "Paper") or (r == "Paper" and h == "Rock"):
            print("I won! I showed ", r)
        else:
            print("Congratulations! You are the winner. I showed", r)
    else:
        break
    time.sleep(3)
    print("Would you like to play again? Write + or - :")
    c = input()
print("Game over!")