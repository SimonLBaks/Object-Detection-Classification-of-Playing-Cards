import keyboard
import time

count = 0
while True:
    keyboard.send("F2")
    count += 1
    print("count:",count)
    if count == 15:
        break
    time.sleep(4.5)