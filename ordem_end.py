import pyautogui as py
from mouseinfo import MouseInfoWindow
from time import sleep


end = [157618,
151055,
160226,
157619,
157620,
157621,
157622,
157623,
157624,
157625,
157626,
151056,
157627,
157628,
157630,
157631,
157629,
157632,
160227,
157633,
157634]

ordem = [46792]

sleep(10)

for i in end:
    sleep(2)
    py.click(1451,121)
    sleep(2)
    py.write(str(i))
    sleep(2)
    py.press('enter')
    sleep(2)
    py.click(629,582)
    sleep(2)
    py.write(str(ordem))
    sleep(2)
    py.click(528,114)
      

