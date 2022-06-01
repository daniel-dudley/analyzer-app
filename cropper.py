import cv2
import numpy as np
import matplotlib.pyplot as plt


from pyzbar.pyzbar import decode
  
# Make one method to decode the barcode
def BarcodeReader(image):
     
    # read the image in numpy array using cv2
    img = cv2.imread(image)
      
    # Decode the barcode image
    detectedBarcodes = decode(img)
      
    # If not detected then print the message
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:
       
          # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes: 
           
            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect
             
            # Put the rectangle in image using
            # cv2 to heighlight the barcode
            cv2.rectangle(img, (x-10, y-10),
                          (x + w+10, y + h+10),
                          (255, 0, 0), 2)
             
            if barcode.data!="":
               
            # Print the barcode data
                print(barcode.data)
                print(barcode.type)
                 
    #Display the image
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 
if __name__ == "__main__":
  # Take the image from user
    image="Img.jpg"
    BarcodeReader('images/cv2-test.jpg')

'''
# Load the image
img = cv2.imread('images/cv2-test.jpg')

# convert to grayscale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

edged = cv2.Canny(img, 170, 490)
# Apply adaptive threshold
thresh = cv2.adaptiveThreshold(edged, 255, 1, 1, 11, 2)
thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

# apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
thresh = cv2.dilate(thresh,None,iterations = 2)
thresh = cv2.erode(thresh,None,iterations = 15)

# Find the contours
contours,hierarchy = cv2.findContours(thresh,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)

# For each contour, find the bounding rectangle and draw it
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,
                    (x,y),(x+w,y+h),
                    (0,255,0),
                    2)

# Filename
filename = 'cv2-test1.jpg'
  
# Using cv2.imwrite() method
# Saving the image
cv2.imwrite('cv2-test1', img)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''


'''
# Code Source: https://docs.opencv.org/master/df/dd2/tutorial_py_surf_intro.html

# Read the image
img = cv.imread('images/cv2-test.jpg')
 
# Find the features (i.e. keypoints) and feature descriptors in the image
surf = cv.xfeatures2d.SURF_create(400)
kp, des = sift.detectAndCompute(img,None)
 
# Draw circles to indicate the location of features and the feature's orientation
img=cv.drawKeypoints(gray,kp,img,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Save the image
cv.imwrite('surf_with_features_chessboard.jpg',img)




filepath = "images/cv2-test.jpg"
australia = cv2.imread(filepath)
australia_grey = cv2.cvtColor(australia, cv2.COLOR_BGR2GRAY)

australia_thresh = cv2.threshold(australia_grey,226,255,cv2.THRESH_BINARY)[1]
australia_binary = cv2.bitwise_not(australia_thresh)

plt.imshow(australia_binary, cmap="gray", vmin=0, vmax=255)

# Generate variables
x1,y1,w,h = cv2.boundingRect(australia_binary)
x2 = x1+w
y2 = y1+h

# Draw bounding rectangle
start = (x1, y1)
end = (x2, y2)
colour = (255, 0, 0)
thickness = 1
rectangle_img = cv2.rectangle(australia, start, end, colour, thickness)
print("x1:", x1, "x2:", x2, "y1:", y1, "y2:", y2)
plt.imshow(rectangle_img, cmap="gray")





image = cv2.imread('images/cv2-test.jpg')
original = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)
    ROI = original[y:y+h, x:x+w]
    cv2.imwrite('Image_{}.png'.format(ROI_number), ROI)
    ROI_number += 1

cv2.imshow('image', image)
cv2.imshow('Thresh',thresh)
cv2.waitKey()
'''

