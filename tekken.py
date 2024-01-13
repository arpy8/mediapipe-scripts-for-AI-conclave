import cv2
import pydirectinput as pg

from trackers.PoseModule import PoseDetector
from trackers.HandTrackingModule import HandDetector

KEY1 = "w"
KEY2 = "s"
KEY3 = "a"
KEY4 = "d"

DELAY = 0.5
THRESH = 20

UP_COORDS = (300, 100)
RIGHT_COORDS = (100, 250)
LEFT_COORDS = (500, 250)
DOWN_COORDS = (300, 380)

key_pressed = False

def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

def press_key(closest_key, key_pressed):
    if closest_key==KEY1 and not key_pressed: 
        pg.keyDown(KEY1)
        key_pressed = True
    elif closest_key!=KEY1 and key_pressed: 
        pg.keyUp(KEY1)
        key_pressed = Falsea

    elif closest_key==KEY2 and not key_pressed: 
        pg.keyDown(KEY2)
        key_pressed = True
    elif closest_key!=KEY2 and key_pressed: 
        pg.keyUp(KEY2)
        key_pressed = False

    elif closest_key==KEY4 and not key_pressed: 
        pg.keyDown(KEY4)
        key_pressed = True
    elif closest_key!=KEY4 and key_pressed: 
        pg.keyUp(KEY4)
        key_pressed = False

    elif closest_key==KEY3 and not key_pressed: 
        pg.keyDown(KEY3)
        key_pressed = True
    elif closest_key!=KEY3 and key_pressed: 
        pg.keyUp(KEY3)
        key_pressed = False

def main():
    global key_pressed

    cap = cv2.VideoCapture(0)

    hand_detector = HandDetector(maxHands=1)
    pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)

    while True:
        _, raw_img = cap.read()
    
        img = pose_detector.findPose(raw_img)
        lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)
        # hand_detector.fingersUp()
        
        try:
            if len(lmList) >= 16:
                
                right_wrist_coords = lmList[20][:2]
                put_text(img, str(right_wrist_coords), (img.shape[1]-300, 100))
                
                UP_DISTANCE, _, _ = pose_detector.findDistance(right_wrist_coords, UP_COORDS, img=img, color=(0, 0, 255), scale=5)
                LEFT_DISTANCE, _, _ = pose_detector.findDistance(right_wrist_coords, LEFT_COORDS, img=img, color=(0, 0, 255), scale=5)
                RIGHT_DISTANCE, _, _ = pose_detector.findDistance(right_wrist_coords, RIGHT_COORDS, img=img, color=(0, 0, 255), scale=5)
                DOWN_DISTANCE, _, _ = pose_detector.findDistance(right_wrist_coords, DOWN_COORDS, img=img, color=(0, 0, 255), scale=5)

                distances = {
                    KEY1: UP_DISTANCE,
                    KEY3: LEFT_DISTANCE,
                    KEY4: RIGHT_DISTANCE,
                    KEY2: DOWN_DISTANCE
                }

                closest_key = min(distances, key=distances.get)

                press_key(closest_key, key_pressed)
                put_text(img, str(closest_key), (img.shape[1]-300, 200))
                
        except Exception as e:
            print(e)
        
        cv2.circle(img, LEFT_COORDS, THRESH, (0, 255, 0), -1)
        cv2.circle(img, RIGHT_COORDS, THRESH, (255, 0, 0), -1)
        cv2.circle(img, UP_COORDS, THRESH, (0, 255, 255), -1)
        cv2.circle(img, DOWN_COORDS, THRESH, (0, 0, 0), -1)
                
        cv2.imshow("Tekken Game", raw_img)
        if cv2.waitKey(5) & 0xFF == 27:
            break
 
if __name__ == "__main__":
    main()