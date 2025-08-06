import pyautogui as py
from mouseinfo import MouseInfoWindow
from time import sleep

# MouseInfoWindow()
sleep(10)
for i in range(61489, 62000):
    sleep(2)
    py.click(214,117)
    sleep(1.5)
    py.click(195,182)
    sleep(1.5)
    py.write(str(i))
    sleep(1.5)
    py.click(203,287)
    sleep(1.5)
    py.click(187,332)
    sleep(1.5)
    py.click(214,117)