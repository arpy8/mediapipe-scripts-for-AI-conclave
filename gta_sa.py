# 7/1/24 note: shift to hand gestures

import cv2
import time
import pydirectinput as pg
from windows_toasts import Toast, WindowsToaster

from trackers.PoseModule import PoseDetector
from trackers.HandTrackingModule import HandDetector

DELAY = 0.5

THRESH = 50
THRESH_DIAG = 35
THRESH_BUG = 70

CHEATS = [
    'HESOYAM', 
    'AEZAKMI', 
    'BUFFMEUP',
    'CVWKXAM',
    'FULLCLIP',
    'WORSHIPME',
    'PROFESSIONALKILLER',
]


def put_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

def execute_cheat(cheat, long=False):
    KEYBOARD = ["a", "w", "s", "d", "space", "up", "down", "f"]
    
    if long:
        for keys in KEYBOARD:
            pg.keyUp(keys)         
    for c in cheat:
        pg.keyDown(c)
        time.sleep(0.03)
        pg.keyUp(c)
        print(c)
        
def chad_cj(count):
    toaster = WindowsToaster('Googoo Gaagaa Simulator')
    newToast = Toast()
    if count%2==0:
        text_fields = [[f"Initiating Chad CJ mode 🗣️💯🔥🔥"], [""]]
    else:
        text_fields = [[f"Initiating Virgin CJ mode 🤓"], ["de"]]
        
    newToast.text_fields = text_fields[0]
    toaster.show_toast(newToast)

    for cheat in CHEATS:
        for letter in cheat:
            pg.keyDown(letter)
            time.sleep(0.03)
            pg.keyUp(letter)
            
    newToast.text_fields = [f"{', '.join(map(str, CHEATS))} {text_fields[1]}activated successfully!"]
    toaster.show_toast(newToast)


def main():
    global last_playback_time
    global count, hand_near_face, up_key_pressed

    count = 0
    number_of_hands = 2

    breaks_pressed = False
    left_key_pressed    = False
    right_key_pressed = False
    up_pressed = False
    down_pressed = False
    
    cap = cv2.VideoCapture(0)
    
    hand_detector = HandDetector(maxHands=number_of_hands)
    pose_detector = PoseDetector(staticMode=False,
                                modelComplexity=1,
                                smoothLandmarks=True,
                                enableSegmentation=False,
                                smoothSegmentation=True,
                                detectionCon=0.5,
                                trackCon=0.5)

    finger_log = []
    
    while True:
        _, raw_img = cap.read()

        hands, _ = hand_detector.findHands(raw_img)
        img = pose_detector.findPose(raw_img)

        lmList, _ = pose_detector.findPosition(img, draw=True, bboxWithHands=True)

        try:
            if len(lmList) >= 16 and hands:
                hand_1 = hands[0]
                fingers_1 = hand_detector.fingersUp(hand_1)
                
                hand_2 = None
                if len(hands) == 2:
                    print(len(hands))
                    hand_2 = hands[1]
                    fingers_2 = hand_detector.fingersUp(hand_2)
                
                x, _ = lmList[20][:2]
                
                if len(finger_log) > 10:
                    finger_log.clear()
                
                finger_id = "".join(map(str, fingers_1))
                
                try:
                    if (finger_id != finger_log[-1]):
                        finger_log.append(finger_id)

                except IndexError:
                    finger_log.append(finger_id)
                
                print(finger_log)
                
                try:
                    forward_key_pressed = sum(fingers_1) >= 4
                    backward_key_pressed = fingers_1 == [0, 1, 1, 1, 0]

                    if backward_key_pressed: 
                        pg.keyDown('s') 
                    elif not backward_key_pressed: 
                        pg.keyUp('s')
                        
                    if forward_key_pressed:
                        pg.keyDown('w')
                        pg.keyDown('space')
                    elif not forward_key_pressed:
                        pg.keyUp('w')
                        pg.keyUp('space')
                            
                    # if forward_key_pressed or backward_key_pressed:
                    if x < 200 and not left_key_pressed:
                        pg.keyDown('d')
                        pg.keyDown('space')
                        left_key_pressed = True
                    elif not x < 200 and left_key_pressed:
                        pg.keyUp('d')
                        pg.keyUp('space')
                        left_key_pressed = False

                    elif x > 340 and not right_key_pressed:
                        pg.keyDown('a')
                        right_key_pressed = True
                    elif not x > 340 and right_key_pressed:
                        pg.keyUp('a')
                        right_key_pressed = False                   
                        
                    if hand_2:
                        print(fingers_2)
                        if fingers_2==[1,1,0,0,0] and not up_pressed:
                            print("up")
                            pg.keyDown('up')
                            up_pressed = True
                        elif not fingers_2==[1,1,0,0,0] and up_pressed:
                            pg.keyUp('up')
                            up_pressed = False
                        
                        if fingers_2 == [1,1,0,0,1] and not down_pressed:
                            print("down")
                            pg.keyDown('down')
                            down_pressed = True
                        elif not fingers_2 == [1,1,0,0,1] and down_pressed:
                            pg.keyUp('down')
                            down_pressed = False
                        
                    elif finger_log[-3:] == ['11000', '01000', '01100']:
                        chad_cj(count)
                        finger_log.clear()
                    
                    elif finger_log[-2:]==["00111", "01111"]:
                        pg.mouseDown(button='left')
                        time.sleep(0.03)
                        pg.mouseUp(button='left')
                        finger_log.clear()

                    elif fingers_1==[0,0,1,1,1]:
                        pg.keyDown('f')
                        time.sleep(0.03)
                        pg.keyUp('f')
                        finger_log.clear()
                        
                    elif fingers_1==[0,1,1,1,1] and not breaks_pressed:
                        pg.keyDown('s')
                        breaks_pressed = True
                    elif not fingers_1==[0,1,1,1,1] and breaks_pressed:
                        pg.keyUp('s')
                        breaks_pressed = False
                        finger_log.clear()

                    # else: pg.keyUp('space')
                    
                    if finger_log[-3:] == ['11000', '01000', '11000']:
                        execute_cheat("VROCKPOKEY")
                        finger_log.clear()

                    elif finger_log[-3:] == ['10001', '11001', '10111']:
                        execute_cheat("GOODBYECRUELWORLD", long=True)
                        finger_log.clear()

                    # elif finger_log[-3:] == ['11000', '11001', '10111']:
                    #     execute_cheat("GOODBYECRUELWORLD", long=True)
                    #     finger_log.clear()
                    
                    # elif finger_log[-1:] == ["10001", "11000"]:
                    #     execute_cheat('HESOYAM')
                    #     finger_log.clear()
            

                    elif finger_log[-2:] == ["10001", "11000"]:
                        execute_cheat('HESOYAM')
                        finger_log.clear()
            
                except IndexError:
                    pass    
                
            elif len(lmList) >= 16 and not hands:
                pg.keyUp('w')
                pg.keyUp('s')
                pg.keyUp('space')
        
        except Exception as e:
            print(e)

        cv2.imshow("GTA SA", raw_img)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

if __name__ == "__main__":
    main()