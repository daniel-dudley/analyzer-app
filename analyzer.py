#######################################
# import libraries and useful modules #
#######################################
from PIL import Image, ImageFilter, ImageStat
import cv2
from pillow_heif import register_heif_opener
from pyzbar import pyzbar


def analyze():
    ####################################
    # convert from HEIC to PNG to JPEG #
    ####################################
    register_heif_opener()

    im_heic = Image.open(r"images/assay.HEIC")
    im_heic.save(r"images/assay.jpg", "JPEG")


    ###################################
    # find image bounds & crop points #
    ###################################
    im = cv2.imread(r"images/assay.jpg")

    # find the QR codes in the image
    QR_code = pyzbar.decode(im) #gives x & y of top left point, w, h location for each barcode

    # assign the QR code parameters to variables
    # x & y are the coordinates of top left corner of the QR code while w & h are its width and height
    x1 = QR_code[0].rect[0]
    y1 = QR_code[0].rect[1]
    w1 = QR_code[0].rect[2]
    h1 = QR_code[0].rect[3]
    QR1_data = QR_code[0].data.decode("utf-8")

    x2 = QR_code[1].rect[0]
    y2 = QR_code[1].rect[1]
    w2 = QR_code[1].rect[2]
    h2 = QR_code[1].rect[3]
    QR2_data = QR_code[1].data.decode("utf-8")

    # error checking to make sure QR codes are in the correct position
    if QR1_data == "http://akirapid.com/":
        QR_top = [QR1_data, x1, y1, w1, h1]
        QR_bottom = [QR2_data, x2, y2, w2, h2]
    elif QR2_data == "http://akirapid.com/":
        QR_top = [QR2_data, x2, y2, w2, h2]
        QR_bottom = [QR1_data, x1, y1, w1, h1]
    elif QR1_data == "ALB-A01-B001":
        QR_top = [QR2_data, x2, y2, w2, h2]
        QR_bottom = [QR1_data, x1, y1, w1, h1]
    elif QR2_data == "ALB-A01-B001":
        QR_top = [QR1_data, x1, y1, w1, h1]
        QR_bottom = [QR2_data, x2, y2, w2, h2]


    ################
    # filter image #
    ################
    im_2 = Image.open(r"images/assay.jpg")
        
    # apply median filter 
    # note: increasing size adjusts the kernal size and increases filter intensity
    im_2.filter(ImageFilter.MedianFilter(size = 7)).save(r"images/assay_filtered.jpg")


    ############################
    # find regions of interest #
    ############################
    im_3 = Image.open(r"images/assay_filtered.jpg")

    # find bounding box of assay using QR codes
    top_left = [QR_top[1], QR_top[2]]
    bottom_right = [QR_bottom[1] + QR_bottom[3], QR_bottom[2] + QR_bottom[4]]

    # crop image at bounding box
    im_3.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1])).save(r"images/assay_cropped.jpg")
    
    # get cropped image size
    im_4 = Image.open(r"images/assay_cropped.jpg")
    width, height = im_4.size

    # note: im.crop(x-left, y-top, x-right, y-bottom)
    # crop left region and rgb color swatches
    testing_region = im_4.crop((0.55*width, 0.15*height, 0.78*width, 0.28*height)).save(r"images/testing_region.jpg")
    control_region = im_4.crop((0.23*width, 0.74*height, 0.41*width, 0.87*height)).save(r"images/control_region.jpg")
    r_swatch = im_4.crop((0.074*width, 0.51*height, 0.26*width, 0.55*height)).save(r"images/r_swatch.jpg")
    g_swatch = im_4.crop((0.42*width, 0.50*height, 0.61*width, 0.55*height)).save(r"images/g_swatch.jpg")
    b_swatch = im_4.crop((0.77*width, 0.51*height, 0.96*width, 0.55*height)).save(r"images/b_swatch.jpg")


    #################
    # rgb averaging #
    #################
    def average(image_path):
        im_5 = Image.open(image_path)
        stat = ImageStat.Stat(im_5)
        rgb = stat.mean
        
        r, g, b = rgb
        r = round(r)
        g = round(g)
        b = round(b)
        rgb_average = [r, g, b]
        
        return rgb_average

    testing_region_avg = average(r"images/testing_region.jpg") #region_left_avg
    control_region_avg = average(r"images/control_region.jpg") #r_swatch_left_avg
    r_swatch_avg = average(r"images/r_swatch.jpg") #r_swatch_left_avg
    g_swatch_avg = average(r"images/g_swatch.jpg") #g_swatch_left_avg
    b_swatch_avg = average(r"images/b_swatch.jpg") #b_swatch_left_avg

    #print("testing region avg: ", testing_region_avg)
    #print("control region avg: ", control_region_avg)
    #print(r_swatch_avg, g_swatch_avg, b_swatch_avg)


    ####################
    # color correction #
    ####################
    # pure rgb values within the color gamut of a cmyk printer
    r_pure = [237, 32, 36]
    g_pure = [106, 189, 69]
    b_pure = [57, 83, 164]

    # calculate rgb weights (% difference from pure) of left test
    r_correction_coefficient = 1 + ((r_pure[0] - r_swatch_avg[0]) / r_pure[0]) #r_weight_left
    g_correction_coefficient = 1 + ((g_pure[1] - g_swatch_avg[1]) / g_pure[1])
    b_correction_coefficient = 1 + ((b_pure[2] - b_swatch_avg[2]) / b_pure[2])

    # calculate rgb weights of right test
    #r_weight_right = 1 + ((r_pure[0] - r_swatch_right_avg[0]) / r_pure[0])
    #g_weight_right = 1 + ((g_pure[1] - g_swatch_right_avg[1]) / g_pure[1])
    #b_weight_right = 1 + ((b_pure[2] - b_swatch_right_avg[2]) / b_pure[2])

    # print(r_weight_left, g_weight_left, b_weight_left)
    # print(r_weight_right, g_weight_right, b_weight_right)


    #####################################
    # calculate biomarker concentration #
    #####################################
    # CysC calibration curve data
    #r_int_CysC = 313.4999999999999
    #r_slope_CysC = -167.49999999999991
    #g_int_CycC = 376.8571428571427
    #g_slope_CysC = -193.57142857142847
    #b_int_CysC = 346.07142857142856
    #b_slope_CysC = -133.21428571428572

    # Alb calibration curve data
    r_int_Alb = 286.4285714285713
    r_slope_Alb = -5.028571428571422
    g_int_Alb = 229.7142857142855
    g_slope_Alb = -1.214285714285704
    b_int_Alb = 174.9999999999999
    b_slope_Alb = -1.8999999999999952

    # calculate the concentration of left uPAD (CysC) and apply color correction
    #r_concentration_left = ((r_weight_left * region_left_avg[0]) - r_int_CysC) / r_slope_CysC
    #g_concentration_left = ((g_weight_left * region_left_avg[1]) - g_int_CycC) / g_slope_CysC
    #b_concentration_left = ((b_weight_left * region_left_avg[2]) - b_int_CysC) / b_slope_CysC

    # calculate the concentration of right uPAD (Alb) and apply color correction
    r_concentration = ((r_correction_coefficient * testing_region_avg[0]) - r_int_Alb) / r_slope_Alb
    g_concentration = ((g_correction_coefficient * testing_region_avg[1]) - g_int_Alb) / g_slope_Alb
    b_concentration = ((b_correction_coefficient * testing_region_avg[2]) - b_int_Alb) / b_slope_Alb

    # calculate average conentration of all color bands
    rgb_concentration = (r_concentration + g_concentration + b_concentration) / 3
    #rgb_concentration_right = (r_concentration_right + g_concentration_right + b_concentration_right) / 3

    #return str(rgb_concentration)
    print(rgb_concentration)

    # display [biomarker] values
    #print("\n")
    #print("The concentraiton of cystatin C in mg/dL = ")
    #print(rgb_concentration_left)
    #print("The concentraiton of albumin in mg/g = ")
    #print(str(rgb_concentration_right))

'''
rgb_concentration_left, rgb_concentration_right = analyze()

print(rgb_concentration_left)
print(rgb_concentration_right)
'''

analyze()
