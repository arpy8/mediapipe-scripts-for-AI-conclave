import cv2
import pyautogui as pg
from trackers.pose_tracker import PoseDetector
import webbrowser

GAME_URL = 'https://playpager.com/pinball-online/'
LEFT_THRESHOLD = RIGHT_THRESHOLD = 160

def open_game_tab():
    webbrowser.open(GAME_URL, new=2)

def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

def main():
    global count, hand_near_face, up_key_pressed

    cap = cv2.VideoCapture(0)

    pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)

    open_game_tab()

    left_key_pressed = False
    right_key_pressed = False

    while True:
        _, raw_img = cap.read()

        img = pose_detector.findPose(raw_img)
        lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)

        try:
            if len(lmList) >= 16:
                
                left_shoulder_coords = lmList[11][:2]
                left_elbow_coords = lmList[13][:2]
                left_wrist_coords = lmList[15][:2]
                
                right_shoulder_coords = lmList[12][:2]
                right_elbow_coords = lmList[14][:2]
                right_wrist_coords = lmList[16][:2]

                left_angle, _ = pose_detector.findAngle(left_shoulder_coords, left_elbow_coords, left_wrist_coords, img=img, color=(0, 0, 255), scale=5)
                right_angle, _ = pose_detector.findAngle(right_wrist_coords, right_elbow_coords, right_shoulder_coords, img=img, color=(0, 0, 255), scale=5)                

                # put_text(img, f"Left Angle: {left_angle}", (img.shape[1]-300, 100))
                # put_text(img, f"Right Angle: {right_angle}", (img.shape[1]-300, 150))

                if left_angle < LEFT_THRESHOLD and not left_key_pressed:
                    pg.keyDown('left')
                    left_key_pressed = True

                elif left_angle >= LEFT_THRESHOLD and left_key_pressed:
                    pg.keyUp('left')
                    left_key_pressed = False

                if right_angle < RIGHT_THRESHOLD and not right_key_pressed:
                    pg.keyDown('right')
                    right_key_pressed = True

                elif right_angle >= RIGHT_THRESHOLD and right_key_pressed:
                    pg.keyUp('right')
                    right_key_pressed = False

                # if left_angle < 90 and right_angle < 90 and not down_key_pressed:
                #     # pg.press("down")
                #     pg.keyDown('down')
                #     print("down down")
                #     down_key_pressed = True

                # elif left_angle >= 90 and right_angle >= 90 and down_key_pressed:
                #     pg.keyUp('down')
                #     print("up down")
                #     down_key_pressed = False 
            
        except Exception as e:
            print(e)
                
        cv2.imshow("Image", raw_img)
        if cv2.waitKey(5) & 0xFF == 27:
            break
 
if __name__ == "__main__":
    main()