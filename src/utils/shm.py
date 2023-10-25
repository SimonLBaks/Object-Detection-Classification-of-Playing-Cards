import numpy as np
from multiprocessing import shared_memory

# Function to create a shared memory block
def shm_block(box):
    # Create img region
    np_arr = np.ndarray((box[1][1]-box[0][1],box[1][0]-box[0][0],3),dtype=np.uint8)
    #print("shm",np_arr.shape)
    
    # Create shared memory block and copy to numpy array
    shm = shared_memory.SharedMemory(create=True,size=np_arr.nbytes)
    shm_np_arr =np.ndarray(np_arr.shape,dtype=np.uint8,buffer=shm.buf)
    np.copyto(shm_np_arr, np_arr)
    
    return shm, shm_np_arr