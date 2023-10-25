from utils import shm, Monitor_Info, capture_utils, detection_utils
from concurrent.futures import Future, ThreadPoolExecutor
from ctypes import c_int8
import multiprocessing as mp
import time
import mss
import cv2

# Ultralytics imports
from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator
import supervision as sv

# Profiler
import cProfile


           
# List interpolation modes 
interpol_modes = [cv2.INTER_AREA,
                    cv2.INTER_CUBIC,
                    cv2.INTER_NEAREST,
                    cv2.INTER_LINEAR,
                    cv2.INTER_LANCZOS4]

# Load in model
model = YOLO("best.pt")

# Set confidence threshold
conf_threshold = 0.1

# List to store drawed area
boxes = []
    
if __name__ == "__main__":
    display = Monitor_Info.selectMonitor(3)
    
    # Draw area to monitor
    capture_utils.draw_area(display)
    
    # Get the process ID of the current Python process
    #pid = psutil.Process()
    
    # Create a queue to receive the array from the child process
    #queue = mp.Queue()
    #print(boxes)
    
    # Create shm block
    shm_obj,shm_np_arr = shm.shm_block(boxes)
   
    # Create a new process to run the getimg function
    stop_flag = mp.Value(c_int8, 0)
    p = mp.Process(target=capture_utils.getimg, args=(display,shm_obj.name,stop_flag,boxes))
    p.start()
    
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("frame", 800, 480)
    with mss.mss() as sct:
        # fps calculation variables
        start_time = time.time()
        #num_frames = 0
        prev_frame_time = 0
        new_frame_time = 0
        xy = boxes[0]+boxes[1]
        pool = ThreadPoolExecutor(max_workers=1)
        time.sleep(5)
        while True:
            # Get the memory usage information
            #memory_info = pid.memory_info()
            #print("Memory usage:", memory_info.rss / 1024 / 1024, "MB")
            img = shm_np_arr
           
            #frame = queue.get()
            
            # Working
            future = pool.submit(detection_utils.predict, model, img, conf_threshold)
            results = future.result()
            detection_utils.find_boxes(results, img)
            
            
            #if threads.done():
            #    print("running")
            #    results = threads.result() 
            #    find_boxes(results,frame) 
                
            # Draw FPS text on image
            num_frames += 1
            if num_frames > 10:
                elapsed_time = time.time() - start_time
                fps = (num_frames / elapsed_time)
                print(text)
                num_frames = 0
            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time) 
            prev_frame_time = new_frame_time   
            text = f'FPS: {int(fps)}'
            #print(text)
            cv2.putText(img, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            cv2.putText(img, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                

            # update fps calculation variables
            num_frames = 1
            start_time = time.time()

            
            # Display the resulting frame
            cv2.imshow('frame', img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                shm_obj.close()
                shm_obj.unlink()
                stop_flag.value = 1
                break
            elif key == 27:
                shm_obj.close()
                shm_obj.unlink()
                stop_flag.value = 1
                break
            #num_frames += 1
        p.terminate()
        cv2.destroyAllWindows()
