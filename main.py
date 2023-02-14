import sys, time, keyboard
import pyautogui as pag
import cv2
import requests
url = "https://discord.com/api/webhooks/1065789001052729515/IGrZS24YS9GISq-hQYhaQFUzdecgYgCg8B4JR1zSJWz9PSYPHU6zqtOPpdVfSvZ5WcRa"
from PIL import Image
print(pag.FAILSAFE)
# try:
#     while True:
#         time.sleep(1)
#
#         x, y = pag.position()
#         position = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(position + "\n", end="")
#         if keyboard.is_pressed('q'):
#             break
# except KeyboardInterrupt:
#     print("\n")
# except pag.FailSafeException:
#     print("\n")

# res = pyautogui .locateOnScreen("edit.png")
# print(res)
# while not keyboard.is_pressed('q'):
#     res = pag.locateCenterOnScreen("search.png")
#     # print(res)
#     if res is not None:
#         time.sleep(0.5)
#         print('searching\n')
#         pag.moveTo(res)
#         pag.click()
#         pag.write('itskevers')
#         pag.hotkey("enter")
#         res = Nonec
#         break


"""
FNAF coords:
Top Left: 0, 0
Bottom Left: 0, 719
Top Right: 1279, 0
Bottom Right: 1279, 719
So 1280 x 720

Regular screen res is 1920 x 1080
"""
BONNIE = 1
CHICA = 0
facingLeft = False
bonnie = False
chica = False
eyes = False

# Opens or closes the camera
def toggleCam():
    pag.moveTo(640, 640)
    pag.moveTo(640, 670, 0.1)
    pag.moveTo(640, 640, 0.1)
    global facingCenter
    facingCenter = True

def pirateCove():
    # Switch to pirate's cove
    pag.moveTo(930, 490)
    pag.click()

def westHall():
    # Switch to west hall cam
    pag.moveTo(980, 600)
    pag.click()

def lookLeft():
    global facingLeft
    if not facingLeft:
        pag.moveTo(0, 360)
        time.sleep(0.4)
        facingLeft = True

def lookRight():
    global facingLeft
    if facingLeft:
        pag.moveTo(1279, 360)
        time.sleep(0.4)
        facingLeft = False

def leftDoor():
    lookLeft()
    pag.moveTo(56, 336)
    pag.click()

def leftLightOn():
    lookLeft()
    pag.moveTo(56, 447)
    pag.click()

def leftlightOff():
    pag.moveTo(56, 459)
    pag.click()

def rightDoor():
    lookRight()
    pag.moveTo(1212, 336)
    pag.click()

def rightLightOn():
    lookRight()
    pag.moveTo(1212, 447)
    pag.click()

def rightLightOff():
    pag.moveTo(1212, 459)
    pag.click()

def checkTronic(tronic):
    # Check if tronic is at door.
    # Double checks and lower confidence compensate for flashing lights or errors
    #timeout_start = time.time()
    #timeout = 0.25
    #time.sleep(0.25)
    if tronic:
        global bonnie
        #while time.time() < timeout + timeout_start:
        if bonnie:  # If Bonnie is already there before, check if still there
            bonnieAtDoor = pag.locateOnScreen("bonnieOutside.png", grayscale=True, confidence=0.8) is not None
            if not bonnieAtDoor:
                bonnieAtDoor = pag.locateOnScreen("bonnieOutside.png", grayscale=True, confidence=0.8) is not None

        else:  # Check if Bonnie has just arrived at the door
            bonnieAtDoor = pag.locateOnScreen("bonnieAtDoor.png", grayscale=True, confidence=0.8) is not None
            if not bonnieAtDoor:
                bonnieAtDoor = pag.locateOnScreen("bonnieAtDoor.png", grayscale=True, confidence=0.8) is not None
        bonnie = bonnieAtDoor
        #print("check")
        return bonnieAtDoor
        #if bonnieAtDoor:
                #data = {"content": 'Found Bonnie!'}
                #response = requests.post(url, json=data)
        #    return True

        #data = {"content": 'Did not find Bonnie'}
        #response = requests.post(url, json=data)
        #print("done")
        #return False
    else:
        global chica
        #while time.time() < timeout + timeout_start:
        if chica: # If Chica is already there before, check if still there
            chicaAtDoor = pag.locateOnScreen("chicaGone.png", grayscale=True, confidence=0.8) is None
            if chicaAtDoor:
                chicaAtDoor = pag.locateOnScreen("chicaGone.png", grayscale=True, confidence=0.9) is None
        else:  # Check if Chica has just arrived at the door
            chicaAtDoor = pag.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.8) is not None
            if not chicaAtDoor:
                chicaAtDoor = pag.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.9) is not None
        chica = chicaAtDoor
        time.sleep(0.1)  # Delay, the game doesn't like responses too fast for right door
        return chicaAtDoor
        #if chicaAtDoor:
                #data = {"content": 'Found Chica!'}
                #response = requests.post(url, json=data)
        #    return True

        #data = {"content": 'Did not find Chica'}
        #response = requests.post(url, json=data)
        #return False


def checkBonnie():
    leftLightOn()
    if bonnie != checkTronic(BONNIE):
        leftDoor()
    #elif bonnie != checkTronic(BONNIE):
     #   leftDoor()
    leftlightOff()

def checkChica():
    rightLightOn()
    if chica != checkTronic(CHICA):
        rightDoor()
    #elif chica != checkTronic(CHICA):
     #   rightDoor()
    rightLightOff()

def checkFoxy():
    # Foxy is there
    global eyes
    if eyes:
        # Check if Foxy is gone, after already seeing his second stage
        if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.6) is None:
            if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.6) is None:
                print("found foxy")
                eyes = False
                return True
    else:
        # Check for Foxy's second stage, one before he's gone
        if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.7) is None:
            if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.7) is not None:
                print("found eyes")
                eyes = True
    return False

def stopFoxy():
    # Change to west hall
    westHall()
    pirateCove()

# Bot plays
def autoPlay():
    global bonnie

    # Stalling at the beginning
    toggleCam()  # up
    time.sleep(0.3)
    pirateCove()
    time.sleep(0.3)
    toggleCam()  # down
    time.sleep(3)
    toggleCam()  # up
    time.sleep(0.3)
    toggleCam()  # down
    time.sleep(3)
    toggleCam()  # up
    time.sleep(0.3)
    toggleCam()  # down

    while not keyboard.is_pressed('x'):  # Change to while not seeing 5% power
        if not chica:
            rightDoor()

        toggleCam()
        time.sleep(0.6)
        # If Foxy left cove, change to west hall and close left door (if open)
        if checkFoxy():
            stopFoxy()
            toggleCam()
            if not bonnie:
                leftDoor()
                bonnie = True
        else:
            toggleCam()
            if not chica:
                rightDoor()
            checkChica()
        checkBonnie()
        time.sleep(0.5)


# Other controls for playing/testing
while not keyboard.is_pressed('x'):
    if keyboard.is_pressed('s'):
        toggleCam()
    if keyboard.is_pressed('a'):
        leftLightOn()
    if keyboard.is_pressed('d'):
        rightLightOn()
    if keyboard.is_pressed('q'):
        leftDoor()
    if keyboard.is_pressed('e'):
        rightDoor()
    if keyboard.is_pressed('o'):
        autoPlay()
    if keyboard.is_pressed('n'):
        pirateCove()
    if keyboard.is_pressed('m'):
        westHall()
    if keyboard.is_pressed('f'):
        if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.4):
            print("found")
        else:
            print("not found")

