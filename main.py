import keyboard
import time
import pyautogui as pag

print(pag.FAILSAFE)  # Make sure failsafe is on
"""
USE THIS TO PRINT COORDS OF MOUSE
try:
     while True:
        time.sleep(1)

        x, y = pag.position()
        position = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(position + "\n", end="")
#         if keyboard.is_pressed('q'):
#             break
except KeyboardInterrupt:
     print("\n")
"""

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
facingLeft = True
bonnie = False
chica = False
eyes = False

# Opens or closes the camera
def toggleCam():
    pag.moveTo(640, 640)
    pag.moveTo(640, 670, 0.1)
    pag.moveTo(640, 640, 0.1)

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
    if tronic:
        global bonnie
        if bonnie:  # If Bonnie is already there before, check if still there
            while True:
                bonnieAtDoor = pag.locateOnScreen("bonnieOutside.png", grayscale=True, confidence=0.8) is not None
                if not bonnieAtDoor:
                    bonnieAtDoor = pag.locateOnScreen("bonnieOutside.png", grayscale=True, confidence=0.8) is not None
                    if not bonnieAtDoor:
                        break
                leftlightOff()
                time.sleep(0.2)
                leftLightOn()
                time.sleep(0.1)

        else:  # Check if Bonnie has just arrived at the door
            bonnieAtDoor = pag.locateOnScreen("bonnieAtDoor.png", grayscale=True, confidence=0.6) is not None
            if not bonnieAtDoor:
                bonnieAtDoor = pag.locateOnScreen("bonnieAtDoor.png", grayscale=True, confidence=0.6) is not None
        bonnie = bonnieAtDoor
        return bonnieAtDoor
    else:
        global chica
        if chica:  # If Chica is already there before, check if still there
            while True:
                chicaAtDoor = pag.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.6) is not None  # True is STILL THERE
                if not chicaAtDoor:
                    chicaAtDoor = pag.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.5) is not None
                    if not chicaAtDoor:
                        break
                rightLightOff()
                time.sleep(0.2)
                rightLightOn()
        else:  # Check if Chica has just arrived at the door
            chicaAtDoor = pag.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.6) is not None
            if not chicaAtDoor:
                chicaAtDoor = pag.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.6) is not None
        chica = chicaAtDoor
        time.sleep(0.1)  # Delay, the game doesn't like responses too fast for right door
        return chicaAtDoor


def checkBonnie():
    leftLightOn()
    if bonnie != checkTronic(BONNIE):
        leftDoor()
    leftlightOff()

def checkChica():
    rightLightOn()
    if chica != checkTronic(CHICA):
        rightDoor()
    rightLightOff()

def checkFoxy():
    # Foxy is there
    global eyes
    if eyes:
        # Check if Foxy is gone, after already seeing his second stage
        if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.6) is None:
            if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.6) is None:
                eyes = False
                return True
    else:
        # Check for Foxy's second stage, one before he's gone
        if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.6) is not None:
            if pag.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.5) is not None:
                eyes = True
    return False

def stopFoxy():
    # Change to west hall
    westHall()
    pirateCove()

# Bot plays
def autoPlay():
    global bonnie
    global chica
    global eyes
    stopped = False
    while True:
        bonnie = False
        chica = False
        eyes = False
        pag.moveTo(312, 631)  # Custom night button
        pag.click()
        time.sleep(2)
        pag.moveTo(1140, 656)  # Ready button
        pag.click()
        time.sleep(9)  # Wait for game to load
        # Stalling at the beginning
        time.sleep(3)
        lookRight()
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
        time.sleep(3)
        toggleCam()  # up
        time.sleep(0.3)
        toggleCam()  # down
        time.sleep(3)

        timeout = 435  # 7 min 15 s
        start = time.time()
        while time.time() < start + timeout:
            if not chica:
                rightDoor()
                if stopped:  # If foxy attacked, check Chica
                    chica = True
                    stopped = False
            toggleCam()
            time.sleep(0.4)
            # If Foxy left cove, change to west hall and close left door (if open)
            if checkFoxy():
                stopFoxy()
                toggleCam()
                if not chica:
                    rightDoor()
                    stopped = True
                if not bonnie:
                    leftDoor()
                    bonnie = True
                time.sleep(0.5)
            else:
                toggleCam()
                if not chica:
                    rightDoor()
                checkChica()
            checkBonnie()
            if not bonnie:
                time.sleep(0.6)
            if pag.locateOnScreen("stars.png", grayscale=True, confidence=0.5) is not None:  # We are on the title screen
                break
        # Stop everything
        time.sleep(0.1)
        if bonnie:
            leftDoor()
        if chica:
            leftDoor()
        # Restart game
        while True:
            if pag.locateOnScreen("stars.png", grayscale=True, confidence=0.5) is not None:  # We are on the title screen
                break
            time.sleep(3)
        # time.sleep(130)  # 130 + 430 is 9min 20s. Wait until game is definitely over


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
    if keyboard.is_pressed("p"):
        rightDoor()
        leftDoor()
        toggleCam()
        west = True
        while pag.locateOnScreen("5Left.png", confidence=0.4) is None:
            if west:
                westHall()
                west = False
            else:
                pirateCove()
                west = True
            time.sleep(1)
        print("5 is left")
