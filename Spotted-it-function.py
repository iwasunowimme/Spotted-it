import cv2
from os import listdir
import zipfile
import sys

file_name = input()
with zipfile.ZipFile(file_name, 'r') as zip_ref:
    zip_ref.extractall('temp')
temp_dir = "temp"
list_temp_dir = listdir(temp_dir)
contours_to_compare = []
images_to_compare = []
for image_num in list_temp_dir:   # For each item in folder
    if image_num[-3:] == "png":  # if it is a PNG
        # Read file and add to list
        image = cv2.imread(temp_dir + "/" + image_num)  
        images_to_compare.append(image)
        
        # Convert image to gray than to black
        grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, blackAndWhiteImage = cv2.threshold(grey_image,  200, 255, cv2.THRESH_BINARY)  # 200 threshold for lighter pictures
        blackAndWhiteImage = 255 - blackAndWhiteImage  # get the negative of the image
        
        # Get the contours of the image and add to list
        contours, _ = cv2.findContours(blackAndWhiteImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_to_compare.append(contours)
        
img_a_index = 0
img_b_index = 1
# set the images        
img_a = images_to_compare[img_a_index].copy()
img_b = images_to_compare[img_b_index].copy()
    
cnt_img_a = []
cnt_img_b = []
    
min_match = 10 # set a minimum match value to compare to (matches close to 0 are stronger)
    
# Threshold area is created as to not use small artifacts
threshold_area_min = 1500      
threshold_area_max = 200000
    
# compare all contours to one another
for a in contours_to_compare[img_a_index]:
    area_a = cv2.contourArea(a)  # find the area for each contour and test to see if it is relevant
    if  area_a > threshold_area_min and area_a < threshold_area_max :
        for b in contours_to_compare[img_b_index]:
            area_b = cv2.contourArea(b)  # find the area for each contour and test to see if it is relevant
            if  area_b > threshold_area_min and area_b < threshold_area_max :
                match = cv2.matchShapes(a,b,1,0.0)  # match shape using method '1'
                # check if match is new best
                if match < min_match:
                    min_match = match
                    cnt_img_a = a
                    cnt_img_b = b
                        
# Draw the contours and print each image
cv2.drawContours(img_a,[cnt_img_a],0,(200,100,0),10)
cv2.imshow("Image a",img_a)
cv2.drawContours(img_b,[cnt_img_b],0,(200,100,0),10)
cv2.imshow("Image b",img_b)
cv2.waitKey(0)
cv2.destroyAllWindows()
