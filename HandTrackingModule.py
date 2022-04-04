import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res = self.hands.process(img_RGB)
        if self.res.multi_hand_landmarks:
            for handLandmark in self.res.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, handLandmark, self.mp_hands.HAND_CONNECTIONS)

        return img
    def find_pos(self, img, hand_no=0, draw=True):
        landmarkList=[]
        if self.res.multi_hand_landmarks:
            my_hand=self.res.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                landmarkList.append([id, cx, cy])
                if draw:
                   cv2.circle(img, (cx, cy), 10, (100, 72, 164), cv2.FILLED)
        return landmarkList



def main():
    prev_time = 0
    curr_time = 0
    capture = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = capture.read()
        img = detector.find_hands(img)
        landmarkList = detector.find_pos(img)
        print(landmarkList)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        cv2.putText(img, f'FPS: {str(int(fps))}', (10, 65), cv2.FONT_HERSHEY_PLAIN, 2, (100, 72, 164), 3)

        cv2.imshow("Video Capture", img)
        cv2.waitKey(1)




if __name__ == "__main__":
    main()