import cv2
import numpy as np

def get_avatar_maxcontour(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,100,255, cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("Number of contours detected:", len(contours))

    if len(contours) != 0:
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        img = img[y:y+h, x:x+w]
        return img
    return None
def get_avatar(image_path):
    # Read image.
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    img = img[:,:img.shape[1]//2]
    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))
    
    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                param2 = 30, minRadius = 1, maxRadius = 40)
    
    # Draw circles that are detected.
    if detected_circles is not None:
    
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        detected_circles = detected_circles[0, :]
        # print(detected_circles)
        sorted(detected_circles,key=lambda x: x[2], reverse=True)
        pt = detected_circles[0]
        a, b, r = pt[0], pt[1], pt[2]

        # Draw the circumference of the circle.
        # cv2.circle(img, (a, b), r, (0, 255, 0), 2)

        # Draw a small circle (of radius 1) to show the center.
        avatar = img[b-r:b+r, a-r:a+r]
        return avatar
    print(image_path)
    return get_avatar_maxcontour(img)