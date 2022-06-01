#######################################
# import libraries and useful modules #
#######################################
from PIL import Image, ImageStat #ImageFilter
import numpy as np
import matplotlib.pyplot as plt

'''
################
# filter image #
################
im = Image.open(r"images/image.jpg")
     
# apply median filter 
# note: increasing size adjusts the kernal size and increases filter intensity
im_filtered = im.filter(ImageFilter.MedianFilter(size = 7)).save(r"images/image_filtered.jpg")
'''

#################
# rgb averaging #
#################
def average(image_path):
    im = Image.open(image_path)
    stat = ImageStat.Stat(im)
    rgb = stat.mean
    
    r, g, b = rgb
    r = round(r)
    g = round(g)
    b = round(b)
    rgb_average = [r, g, b]
    print(rgb_average)
    return rgb_average

# find rgb averages of low, medium and high [CysC]
#print("region_left_lowC_avg: ")
region_left_lowC_avg = average(r"calibrator_images/region_left_lowC.jpg")
#print("region_left_medC_avg: ")
region_left_medC_avg = average(r"calibrator_images/region_left_medC.jpg")
#print("region_left_highC_avg: ")
region_left_highC_avg = average(r"calibrator_images/region_left_highC.jpg")

# find rgb averages of low, medium and high [Alb]
#print("region_right_lowC_avg: ")
region_right_lowC_avg = average(r"calibrator_images/region_right_lowC.jpg")
#print("region_right_medC_avg: ")
region_right_medC_avg = average(r"calibrator_images/region_right_medC.jpg")
#print("region_right_highC_avg: ")
region_right_highC_avg = average(r"calibrator_images/region_right_highC.jpg")


##########################
# CysC calibration curve #
##########################
r_cysC = [region_left_highC_avg[0], region_left_medC_avg[0], region_left_lowC_avg[0]]
g_cysC = [region_left_highC_avg[1], region_left_medC_avg[1], region_left_lowC_avg[1]]
b_cysC = [region_left_highC_avg[2], region_left_medC_avg[2], region_left_lowC_avg[2]]
cysC_concentration = [1.6, 1.2, 1]

def calibrate(color_band, biomarker_concentration):
    # load data
    x = np.array(biomarker_concentration)
    y = np.array(color_band)

    # create plot
    plt.plot(x, y, 'o')

    # linear regression of degree 1
    m, b = np.polyfit(x, y, 1)

    # plot
    plt.plot(x, m*x + b)

    #axes = plt.add_subplot(100)
    #axes.set_ylabel('y')
    #axes.set_title('x')
    #plt.axes.Axes.set_xlabel('x')
    #plt.axes.Axes.set_ylabel('y')
    
    print("m = "), print(m)
    print("b = "), print(b)
    #print("\n")

    plt.show()

    return x, y, m, b

# R vs. [CysC], G vs. [CysC], B vs. [CysC]
print("R-band [CysC]: ")
calibrate(r_cysC, cysC_concentration)
print("G-band [CysC]: ")
calibrate(g_cysC, cysC_concentration)
print("B-band [CysC]: ")
calibrate(b_cysC, cysC_concentration)


#########################
# Alb calibration curve #
#########################
r_alb = [region_right_highC_avg[0], region_right_medC_avg[0], region_right_lowC_avg[0]]
g_alb = [region_right_highC_avg[1], region_right_medC_avg[1], region_right_lowC_avg[1]]
b_alb = [region_right_highC_avg[2], region_right_medC_avg[2], region_right_lowC_avg[2]]
alb_concentration = [35, 25, 20]

print("R-band [Alb]: ")
calibrate(r_alb, alb_concentration)
print("G-band [Alb]: ")
calibrate(g_alb, alb_concentration)
print("B-band [Alb]: ")
calibrate(b_alb, alb_concentration)


'''
https://stackoverflow.com/questions/33998364/crop-image-from-all-sides-after-edge-detection
https://www.geeksforgeeks.org/python-edge-detection-using-pillow/
https://www.adamsmith.haus/python/answers/how-to-plot-a-linear-regression-line-on-a-scatter-plot-in-python
'''