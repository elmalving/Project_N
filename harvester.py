import pyautogui as pt
import pydirectinput as pd
from time import sleep
from random import uniform
import emailSender


def rejoin_island():
    sleep(30)
    pd.press('/')
    pd.typewrite('hub')
    pd.press('enter')
    sleep(3)
    pd.press('/')
    pd.typewrite('is')
    pd.press('enter')
    sleep(1)


def correct_pos():
    pd.press('space')
    sleep(0.1)
    pd.press('space')
    pd.press('space')
    pt.keyDown('d')
    sleep(0.5)
    pt.keyUp('d')
    sleep(1)


def check_screen(case: int = 1):
    if pt.locateOnScreen('images/wart.png', confidence=.5):
        return 1
    if pt.locateOnScreen('images/wart1.png', confidence=.5):
        return 1
    if pt.locateOnScreen('images/wart2.png', confidence=.5):
        return 1
    if case == 1:
        pt.keyDown('a')
        sleep(0.5)
        pt.keyUp('a')
        if check_screen(case=2):
            return 1
    elif case == 2:
        rejoin_island()
        sleep(4)
        correct_pos()
        if check_screen(case=3):
            return 1
    elif case == 3:
        correct_pos()
        if check_screen(case=4):
            return 1


sleep(3)

while check_screen():
    pt.mouseDown(button='left')
    pt.keyDown('a')
    pt.moveRel(-8, 0, duration=.3)
    pt.moveRel(8, 0, duration=.3)
    sleep(uniform(14.5, 14.75))
    pt.keyUp('a')
    pt.mouseUp(button='left')
    pt.keyDown('w')
    sleep(uniform(.6, .7))
    pt.keyUp('w')
    pt.mouseDown(button='left')
    pt.keyDown('d')
    pt.moveRel(8, 0, duration=.3)
    pt.moveRel(-8, 0, duration=.3)
    sleep(uniform(14.5, 14.75))
    pt.keyUp('d')
    pt.mouseUp(button='left')
    pt.keyDown('w')
    sleep(uniform(.6, .7))
    pt.keyUp('w')

screenshot_name = 'screenshot.jpeg'
pt.screenshot().save(screenshot_name)

sender = emailSender.Sender(subject='У нас проблемы!', receiver='sjjsjdjd.sksksj@gmail.com',
                            file_path='screenshot.jpeg')

sender.send()
