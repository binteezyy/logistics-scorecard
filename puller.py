import os,sys
import time
from time import sleep

os.system("cls")
os.system("git checkout development")
t = (2018, 12, 28, 8, 44, 4, 4, 362, 0)
curtime = time.asctime(t)

while True:
    print("\bPULLING FROM REPOSITORY", curtime)
    os.system("git pull")
    print("\n")
    sleep(2)
