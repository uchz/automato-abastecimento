#%%
import pyautogui as py
from mouseinfo import MouseInfoWindow
from time import sleep
import pandas as pd

df = pd.read_csv('Enderecos.csv', sep=';')

df = df[['numEndereco', 'numPosto']]


df['Ordem'] = range(75001, 75001 + len(df))

end = df['numEndereco']

ordem = df['Ordem']

#%%

MouseInfoWindow()
# %%

sleep(10)
for i,n in zip(end, ordem):

    py.doubleClick(675,312)
    sleep(1)
    py.write(str(i))
    sleep(1)
    py.click(708,354)
    sleep(1)
    py.click(590,224)
    sleep(1)
    py.doubleClick(1506,250)
    sleep(1)
    py.write(str(n))
    sleep(1)
    py.click(1533,740)
    sleep(3)


# %%
