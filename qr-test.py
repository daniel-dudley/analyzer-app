from PIL import Image
from pillow_heif import register_heif_opener
import cv2
from pyzbar import pyzbar

register_heif_opener()

im_heic = Image.open(r"images/tests/assay_redesign2.HEIC")
im_heic.save(r"images/tests/assay_redesign2.jpg", "JPEG")

im1 = cv2.imread(r"images/tests/assay_redesign2.jpg")

# thresholds image to white in back then invert it to black in white
#   try to just the BGR values of inRange to get the best result
mask = cv2.inRange(im1,(0,0,0),(200,200,200))
thresholded = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
edges = cv2.Canny(mask,100,200)
#inverted = 255-thresholded # black-in-white





cv2.imwrite(r"images/tests/assay_redesign2_inverted2.jpg", edges)



'''
im2 = cv2.imread(r"images/tests/assay_redesign2_inverted2.jpg")

barcodes = pyzbar.decode(im2) #gives x & y of top left point, w, h location for each barcode

for barcode in barcodes:
        x,y,w,h = barcode.rect # give location of rectangle
        cv2.rectangle(im2,(x,y),(x+w,y+h),(0,0,255),4)
        bdata = barcode.data.decode("utf-8")
        btype = barcode.type
        text = f"{bdata},{btype}"
        cv2.putText(im2,text,(x,y-10),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.5,(0,255,0),2) # put text above rectangle
'''


cv2.imshow("img", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()


'''
if bdata1 == "http://akirapid.com/":
    QR_top = [bdata1, left1, top1, width1, height1]
    QR_bottom = [bdata2, left2, top2, width2, height2]
elif bdata2 == "http://akirapid.com/":
    QR_top = [bdata2, left2, top2, width2, height2]
    QR_bottom = [bdata1, left1, top1, width1, height1]
elif bdata1 == "ALB-A01-B001":
    QR_top = [bdata2, left2, top2, width2, height2]
    QR_bottom = [bdata1, left1, top1, width1, height1]
elif bdata2 == "ALB-A01-B001":
    QR_top = [bdata1, left1, top1, width1, height1]
    QR_bottom = [bdata2, left2, top2, width2, height2]
'''

#print(QR_top, QR_bottom)

