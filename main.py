import cv2
import mediapipe as mp
import numpy as np


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


handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    results = handsDetector.process(flippedRGB)
    if results.multi_hand_landmarks is not None:
        d = get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        cv2.drawContours(flippedRGB, [get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)], 0,
                         (255, 0, 0), 2)
        (x, y), r = cv2.minEnclosingCircle(get_points(results.multi_hand_landmarks[0].landmark, flippedRGB.shape))
        a = np.array([d[0], d[16], d[20]])
        (x2, y2), r2 = cv2.minEnclosingCircle(a)
        ws = palm_size(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        ws2 = palm_size2(results.multi_hand_landmarks[0].landmark, flippedRGB.shape)
        cv2.circle(flippedRGB, (int(x), int(y)), int(r), (0, 0, 255), 2)
        cv2.circle(flippedRGB, (int(x2), int(y2)), int(r2), (0, 0, 255), 2)
        print(2 * r / ws)
        print(2 * r2 / ws2)
        print("")
        if 2 * r / ws > 1.9 and 2 * r2 / ws2 < 1:
            cv2.putText(flippedRGB, "Scissors", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=2)
        elif 2 * r / ws > 1.8:
            cv2.putText(flippedRGB, "Paper", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=2)
        elif 2 * r / ws < 1.5:
            cv2.putText(flippedRGB, "Rock", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=2)
        else:
            cv2.putText(flippedRGB, "Error", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=2)

    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    cv2.imshow("Hands", res_image)

handsDetector.close()
