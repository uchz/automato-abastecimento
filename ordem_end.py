
import pyautogui as py
from mouseinfo import MouseInfoWindow
from time import sleep
import pandas as pd

df = pd.read_excel('end.xlsx')

end = df['End']

ordem = df['Ordem']

sleep(10)

for i,n in zip(end, ordem):
    sleep(1)
    py.click(1451,121)
    sleep(1)
    py.write(str(i))
    sleep(1.3)
    py.press('enter')
    sleep(1)
    py.click(629,582)
    sleep(1)
    py.write(str(n))
    sleep(1)
    py.click(528,114)
      

