#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
from os import listdir


# In[2]:


# Folder name where the images are kept
image_dir = "Images"
list_dir = listdir(image_dir)


# In[3]:


# Global values store
contours_all = []
images = []
for image_num in list_dir:   # For each item in folder
    if image_num[-3:] == "png":  # if it is a PNG
        # Read file and add to list
        image = cv2.imread(image_dir + "/" + image_num)  
        images.append(image)
        
        # Convert image to gray than to black
        grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, blackAndWhiteImage = cv2.threshold(grey_image,  200, 255, cv2.THRESH_BINARY)  # 200 threshold for lighter pictures
        blackAndWhiteImage = 255 - blackAndWhiteImage  # get the negative of the image
        
        # Get the contours of the image and add to list
        contours, _ = cv2.findContours(blackAndWhiteImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_all.append(contours)


# In[4]:


def run_and_display(img_a_name, img_b_name, contours, images):
    '''
    This function compares the contours of images and prints the matching contour between the two
    INPUTS: img_a_name, imag_b_name Strings of the file name that the image is to compare
            contours: the list of all contours
            images: the list of all images
    OUTPUTS: Produce the two images with their matching contours highlighted
    RETURNS: None
    '''
    img_a_index = 0
    img_b_index = 0
    # Find the index of the img in the list (as the index will be from its input order)
    for row, file_name in  enumerate(list_dir):
        tester = file_name[:-4]  # Remove ".png"
        if tester == img_a_name:
            img_a_index = row
        if tester == img_b_name:
            img_b_index = row
            
    # set the images        
    img_a = images[img_a_index].copy()
    img_b = images[img_b_index].copy()
    
    cnt_img_a = []
    cnt_img_b = []
    
    min_match = 10 # set a minimum match value to compare to (matches close to 0 are stronger)
    
    # Threshold area is created as to not use small artifacts
    threshold_area_min = 1500      
    threshold_area_max = 200000
    
    # compare all contours to one another
    for a in contours[img_a_index]:
        area_a = cv2.contourArea(a)  # find the area for each contour and test to see if it is relevant
        if  area_a > threshold_area_min and area_a < threshold_area_max :
            for b in contours[img_b_index]:
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


# In[5]:


def run_all():
    '''
    This function will run through every combination of the shapes, including with themselves
    INPUTS: none
    OUTPUTS: output of the run_and_display function  (Produce the two images with their matching contours highlighted)
    RETURNS: none
    '''
    for i in range(len(images)):
        for j in range(i, len(images)):
            run_and_display(str(i), str(j), contours_all, images)


# In[6]:


# run_all()


# In[7]:


# Ask for two images to be compares
image_a = input("Image name 1? ")
image_b = input("Image name 2? ")
run_and_display(image_a, image_b, contours_all, images)

