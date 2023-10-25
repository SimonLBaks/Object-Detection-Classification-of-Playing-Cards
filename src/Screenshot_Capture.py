from utils import shm, Monitor_Info, capture_utils
from ctypes import c_int8
import multiprocessing as mp
import numpy as np
import keyboard
import time
import mss
import os
import cv2

# Profiler
import cProfile

# List interpolation modes
interpol_modes = [cv2.INTER_AREA,
                  cv2.INTER_CUBIC,
                  cv2.INTER_NEAREST,
                  cv2.INTER_LINEAR,
                  cv2.INTER_LANCZOS4]

# Output directory
folder_path = "C:\\Users\\simon\\Downloads\\images"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("Folder created\n")

# List to store drawed area
boxes = []
            
if __name__ == "__main__":
    display = Monitor_Info.selectMonitor(3)
    capture_utils.draw_area(display,boxes, interpol_modes[2])
    
    # If the boxes list includes more than 1 drawed area, exit program
    if len(boxes) > 2:
        print("Error!\nYou can only capture 1 area at a time!")
        exit()
    
    # Initialize shared memory object
    shm_obj,shm_np_arr = shm.shm_block(boxes)
   
    # Create a new process to run the getimg function
    stop_flag = mp.Value(c_int8, 0)
    p = mp.Process(target=capture_utils.getimg, args=(display,shm_obj.name,stop_flag,boxes))
    p.start()
    
    
    cv2.namedWindow("Cropped Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Cropped Frame", 800, 480)
    with mss.mss() as sct:
        xy = boxes[0]+boxes[1]
        i = 0
        while True:
            i += 1
            #keyboard.send('F2')
            
            # Retrieve image from shared memory, then save full resolution img and cropped version
            img = shm_np_arr
            image = os.path.join(folder_path, "FULL_img_{}.jpeg".format(i))
            cv2.imwrite(image, img)
            img = cv2.resize(img,(640, int(640/img.shape[1]*img.shape[0])),interpolation=interpol_modes[4])
            image = os.path.join(folder_path, "img_{}.jpeg".format(i))
            cv2.imwrite(image, img)
           
            cv2.imshow('Cropped Frame', img)
            key = cv2.waitKey(1)
            if key == ord('q') or key == 27:
                shm_obj.close()
                shm_obj.unlink()
                stop_flag.value = 1
                break
            
            # Take screenshot every 5 seconds
            #time.sleep(5) 
        p.terminate()
        cv2.destroyAllWindows()
