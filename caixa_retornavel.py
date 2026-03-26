import pyautogui as py
from mouseinfo import MouseInfoWindow
from time import sleep
import pandas as pd

df = pd.read_excel('end.xlsx')


# MouseInfoWindow()
sleep(10)
for i in range(64879, 65000):
    sleep(1)
    py.click(214,117)
    sleep(1)
    py.write(str(i))
    sleep(0.7)
    py.click(203,287)
    sleep(0.7)
    py.click(187,332)
    sleep(0.7)
    py.click(214,117)