import cv2
import mediapipe as mp
import numpy as np
from time import sleep
import random


def get_points(landmark, shape):
    points = []
    for mark in landmark:
        points.append([mark.x * shape[1], mark.y * shape[0]])
    return np.array(points, dtype=np.int32)


def palm_size(landmark, shape, a, b):
    x1, y1 = landmark[a].x * shape[1], landmark[a].y * shape[0]
    x2, y2 = landmark[b].x * shape[1], landmark[b].y * shape[0]
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

        ws = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape, 0, 9)
        ws2 = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape, 0, 10)
        ws3 = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape, 12, 16)
        ws4 = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape, 12, 8)

        if 2 * r / ws > 1.8 and ws3 > 60 and ws4 > 40:
            return "Scissors"
        elif 2 * r / ws < 1.5 or 2 * r / ws2 < 1.3:
            return "Rock"
        elif 2 * r / ws > 1.8:
            return "Paper"

    handsDetector.close()


print("Greetings Player! Welcome to the Rock-Paper-Scissors game with the computer. To play you should write +:")
c = input()

if c == "+":
    print("Ok, you are ready to play. In a second I will start writing Rock, Paper, Scissors and when I will print SHOOT!, you should show your sign to the camera. ")
    sleep(5)

    while True:
        r = random.choice(["Rock", "Paper", "Scissors"])

        if c == "+":
            print("Get ready!")
            sleep(2.5)
            print("Rock")
            sleep(1)
            print("Paper")
            sleep(1)
            print("Scissors")
            sleep(1)
            print("SHOOT!")
            h = hand_detector()

            if r == h:
                print("You showed", h)
                print("Draw! I showed", r, "too")
            elif h is None:
                print("Your hand was not in the camera")
            elif (r == "Rock" and h == "Scissors") or (r == "Scissors" and h == "Paper") or (r == "Paper" and h == "Rock"):
                print("You showed", h)
                print("I won! I showed", r)
            else:
                print("You showed", h)
                print("Congratulations! You are the winner. I showed", r)
        else:
            break

        sleep(3)
        print("Would you like to play again? Write + or -:")
        c = input()

print("Game over!")
