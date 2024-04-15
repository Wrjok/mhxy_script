import time

import pyautogui


time.sleep(3)
pyautogui.failSafeCheck()
pyautogui.FAILSAFE = False
print(pyautogui.position())

pyautogui.moveTo(10, 10)

print(pyautogui.position())