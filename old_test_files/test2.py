import cv2 as cv


if __name__ == "__main__":
    img = cv.imread("accounts.png")
    
    if img is None:
        print('Image not found')
        
    cv.imshow("Window",img)
    k = cv.waitKey(0)
    if k == ord("q"):
        cv.imwrite("accounts.png",img)