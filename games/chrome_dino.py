import cv2
import pygame
import pyautogui as pg
from trackers.PoseModule import PoseDetector
import webbrowser

GAME_URL = 'https://elgoog.im/dinosaur-game/3d/'
UP_THRESHOLD = 260
DOWN_THRESHOLD = 100

def open_game_tab():
    webbrowser.open(GAME_URL, new=2)

def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('assets/chrome_dino/jump.mp3')
    pygame.mixer.music.play()

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

    jump_triggered = False

    while True:
        _, raw_img = cap.read()

        img = pose_detector.findPose(raw_img)
        lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)

        try:
            if len(lmList) >= 16:
                
                nose_coords = lmList[0][:2]
                

                specific_point = (350, 350)
                distance_specific_point, _, _ = pose_detector.findDistance(nose_coords, specific_point, img=img, color=(0, 0, 255), scale=5)

                # put_text(img, f"Distance: {round(distance_specific_point, 2)}", (img.shape[1]-300, 100))

                if distance_specific_point > UP_THRESHOLD and not jump_triggered:
                    pg.keyDown('up')
                    play_sound() 
                    jump_triggered = True

                elif distance_specific_point <= UP_THRESHOLD:
                    pg.keyUp('up')
                    jump_triggered = False
            
        except Exception as e:
            print(e)
                
        cv2.imshow("Videocam Output", raw_img)
        
        if cv2.waitKey(5) & 0xFF == 27:
            exit()
 
if __name__ == "__main__":
    main()