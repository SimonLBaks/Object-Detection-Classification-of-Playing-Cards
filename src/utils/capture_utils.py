from multiprocessing import shared_memory
import numpy as np
import cv2
import mss

# Callback function for drawing area
def on_mouse(event, x, y, flags, params):
    img, boxes = params
    if event == cv2.EVENT_LBUTTONDOWN:
        #print('Start Mouse Position: '+str(x)+', '+str(y))
        sbox = [x, y]
        boxes.append(sbox)

    elif event == cv2.EVENT_LBUTTONUP:
        #print('End Mouse Position: '+str(x)+', '+str(y))
        ebox = [x, y]
        boxes.append(ebox)
        img[boxes[-2][1]:boxes[-1][1],boxes[-2][0]:boxes[-1][0]]
        
    return img

# Function to draw a specific area on a captured image
def draw_area(disp, boxes, interpol_mode):
    cv2.namedWindow("resize", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("resize", 800, 480)
    with mss.mss() as sct:
        while True:
            # Take screenshot, resize image and draw area to capture
            img = np.array(sct.grab(disp),dtype='uint8')[...,:3]
            img2 = cv2.resize(img, (0, 0), fx=1, fy=1, interpolation=interpol_mode)
            cv2.setMouseCallback("resize", on_mouse, (img2,boxes))
            
            # draw a rectangle 
            for i in range(0, len(boxes), 2):
                if i+1 < len(boxes):
                    xy1 = boxes[i]
                    xy2 = boxes[i+1]
                    cv2.rectangle(img2, (xy1[0], xy1[1]), (xy2[0], xy2[1]), (0, 0, 255), 5)
            
            cv2.imshow("resize",img2)
            
            key = cv2.waitKey(1)
            if key == 27: # ESC to exit
                cv2.destroyAllWindows()
                exit()
            elif key == 13: # Enter to continue program
                break
            elif key == ord('z'): # Undo last drawing
                boxes = boxes[:-2]
        cv2.destroyAllWindows()

# Function to take a screenshot and save in shared memory
def getimg(display,shm_name,stop_flag,boxes):
    with mss.mss() as sct:
        xy = boxes[0]+boxes[1]
        shm_obj = shared_memory.SharedMemory(name=shm_name)
        shm_np_arr =np.ndarray((xy[3]-xy[1],xy[2]-xy[0],3),dtype=np.uint8, buffer=shm_obj.buf)
        while True:
            img = np.array(sct.grab(display),dtype=np.uint8)[...,:3]
            img = img[xy[1]:xy[3],xy[0]:xy[2]]
            np.copyto(shm_np_arr, img)
            
            if stop_flag.value == 1:
                shm_obj.close()
                shm_obj.unlink()
                exit()