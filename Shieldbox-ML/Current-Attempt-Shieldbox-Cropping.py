from torchvision.utils import ImageFont
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
from torchvision.io import read_image
from pathlib import Path
from sympy import solve, symbols
img_dir = './shieldbox/' #wherever photos from visual inspection are stored

def rotate_image(image, angle): #I wonder what this does
    height, width = image.shape[:2] #get image dimensions
    
    rotation_matrix = cv.getRotationMatrix2D((width / 2, height / 2), angle, 1) #calculate the rotation matrix
    
    rotated_image = cv.warpAffine(image, rotation_matrix, (width, height)) #apply the rotation to the image
    
    return rotated_image #I wonder what this is

for full_image in os.listdir(img_dir): #for every image taken
    if full_image == '.ipynb_checkpoints': #bypass error with JupyterLab
        continue
    else:
        image_local = full_image #make variables unrelated to for loop
        path_local = os.path.join(img_dir, image_local)
        image_color = cv.imread(path_local) #open the image
        img = cv.imread(path_local, cv.IMREAD_GRAYSCALE) #make the image black and white
        assert img is not None, "file could not be read, check with os.path.exists()"  #catch if image doesn't open
        img = img[1000:3000, 0:6000] #crop surrounding powerboards out
        img2 = img.copy() #make a new image, not a cropped image
        assert img is not None, "file could not be read, check with os.path.exists()" #catch if cropping didn't work
        template = cv.imread('./pm.jpg', cv.IMREAD_GRAYSCALE) #open regular fiducial image from same location as visual inspeciton folder
        assert template is not None, "file could not be read, check with os.path.exists()" #catch if fiducial didn't open
        img = img2.copy() #return to using img variable instead of img2 for convenience
        method = eval('cv.TM_CCORR_NORMED') #what method we'll use to find fiducials

        res = cv.matchTemplate(img,template,cv.TM_CCOEFF_NORMED) #how close is the fiducial template to actual fiducials
        threshold = 0.85 #high enough to remove false fiducials, low enough to account for variation
        loc = np.where( res >= threshold) #record locations of matched fiducials

        appxloc = [] #initiate list of fiducial coordinate pairs
        priorpt = (0,0) #initiate as upperleft corner of image
        for pt in zip(*loc[::-1]): #for every located fiducial
            if 600 < pt[0] < 2000: #if it's in the range of the shieldbox (where there should be no fiducials),
                continue #skip
            elif pt[0] > 5500: #if it's way to the right of the far-right fiducial,
                continue #skip
            elif abs(priorpt[0] - pt[0]) > 100: #if the located fiducial is far enough away from the prior pt to not be the same one
                overlap = 0 #initiate variable
                if len(appxloc) == 0: #if there's no prior pts
                    appxloc.append(pt) #add it to the fiducial coordinate pairs list
                for i in range(len(appxloc)): #for every pair in the list
                    if abs(pt[0] - appxloc[i][0]) < 50: #if the current pt and the iterated pt in the list are close enough
                        overlap += 1 #increase variable
                if overlap == 0: #if the current pt doesn't already exists in the list i.e. is far enough from preexisting pts
                    appxloc.append(pt) #add it to the list
            priorpt = pt #update the current pt to prior pt
        appxloc.sort(key=lambda a: a[0]) #sort the list by x coordinates
        
        if len(appxloc) < 5: #if fewer than five fiducials are found
            template = cv.imread('./dark-pm.png', cv.IMREAD_GRAYSCALE) #open discolored fiducial image from same location as visual inspeciton folder
            assert template is not None, "file could not be read, check with os.path.exists()" #catch if fiducial didn't open
            method = eval('cv.TM_CCORR_NORMED') #what method we'll use to find fiducials


            res = cv.matchTemplate(img,template,cv.TM_CCOEFF_NORMED) #how close is the fiducial template to actual fiducials
            threshold = 0.7 #high enough to remove false fiducials, low enough to account for variation
            loc = np.where( res >= threshold) #record locations of matched fiducials

            priorpt = (0,0) #initiate as upperleft corner of image
            for pt in zip(*loc[::-1]): #for every located fiducial
                if 600 < pt[0] < 2000: #if it's in the range of the shieldbox (where there should be no fiducials),
                    continue #skip
                elif pt[0] > 5500: #if it's way to the right of the far-right fiducial,
                    continue #skip
                elif abs(priorpt[0] - pt[0]) > 100: #if the located fiducial is far enough away from the prior pt to not be the same one
                    overlap = 0 #initiate variable
                    for i in range(len(appxloc)): #for all potential fiducials
                        if abs(pt[0] - appxloc[i][0]) < 50: #if the current pt and the iterated pt in the list are close enough
                            overlap += 1 #increase variable
                    if overlap == 0: #if the current pt doesn't already exists in the list i.e. is far enough from preexisting pts
                        appxloc.append(pt) #add it to the list
                priorpt = pt #update the current pt to prior pt
        appxloc.sort(key=lambda a: a[0]) #sort the list by x coordinates
        
    
    x1 = appxloc[0][0] #x coordinate of first pair in list
    y1 = appxloc[0][1] #y coordinate of first pair in list
    x2 = appxloc[1][0] #x coordinate of second pair in list
    y2 = appxloc[1][1] #y coordinate of second pair in list
    dy = y2 - y1 #distance between two pairs' y coordinates
    dx = x2 - x1 #distance between two pairs' x coordinates

    if x1/y1 < 1.5 and ((1.5 < x2/y2 < 3 and x2 < 3500) or (y1/y2 < 1 and x2 < 3500)): #if it's the first and second fiducials
        delta_x = 2385 #determined manually
        delta_y = 174 #determined manually
        
        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt

        rotated_image = rotate_image(img, rotation_angle)
        
    elif x1/y1 < 1.5 and (x2/y2 > 3 and x2 < 3500): #if it's the first and third fiducials
        delta_x = 2826 #determined manually
        delta_y = -155 #determined manually
        
        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt

        rotated_image = rotate_image(img, rotation_angle)

    elif x1/y1 < 1.5 and (x2/y2 < 5 and x2 > 3500 ): #if it's the first and fourth fiducials
        delta_x = 3727 #determined manually
        delta_y = 270 #determined manually

        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt

        rotated_image = rotate_image(img, rotation_angle)
        
    elif x1/y1 < 1.5 and (x2/y2 > 5 and x2 > 3500): #if it's the first and fifth fiducials
        delta_x = 4752 #determined manually
        delta_y = -73 #determined manually
        
        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt
        
        rotated_image = rotate_image(img, rotation_angle)
        
    elif (1.5 < x1/y1 < 3 and x1 < 3500) and (x2/y2 > 3 and x2 < 3500): #if it's the second and third fiducials
        delta_x = 442 #determined manually
        delta_y = -326 #determined manually

        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt

        rotated_image = rotate_image(img, rotation_angle)
        
    elif (1.5 < x1/y1 < 3 and x1 < 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the second and fourth fiducials
        delta_x = 1343 #determined manually
        delta_y = 96 #determined manually
        
        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt

        rotated_image = rotate_image(img, rotation_angle)
        
    elif (1.5 < x1/y1 < 3 and x1 < 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the second and fifth fiducials
        delta_x = 2368 #determined manually
        delta_y = -247 #determined manually

        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt
        
        rotated_image = rotate_image(img, rotation_angle)
        
    elif (x1/y1 > 3 and x1 < 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the third and fourth fiducials
        delta_x = 902 #determined manually
        delta_y = 423 #determined manually
        
        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt
        
        rotated_image = rotate_image(img, rotation_angle)
        
    elif (x1/y1 > 3 and x1 < 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the third and fifth fiducials
        delta_x = 1926 #determined manually
        delta_y = 80 #determined manually

        dx_original = delta_x #yes all these variables were already defined, don't remind me
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt

        rotated_image = rotate_image(img, rotation_angle)
        
    elif (x1/y1 > 5 and x1 > 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the fourth and fifth fiducials
        delta_x = 1024 #determined manually
        delta_y = -341 #determined manually
        
        dx_original = delta_x
        dy_original = delta_y
        dx_rotated_scaled = dx
        dy_rotated_scaled = dy
        
        dot_product = dx_original * dx_rotated_scaled + dy_original * dy_rotated_scaled
        cross_product = dx_original * dy_rotated_scaled - dy_original * dx_rotated_scaled
        rotation_angle = np.arctan2(cross_product, dot_product)*180/np.pi #thank you chatgpt

        rotated_image = rotate_image(img, rotation_angle)
        
    scale_factor = np.sqrt(dx_original**2 + dy_original**2) / np.sqrt(dx_original**2 + dy_original**2)

    new_width = int(image_color.shape[1] * scale_factor) #use the scale to scale
    new_height = int(image_color.shape[0] * scale_factor)

    resized_image = cv.resize(rotated_image, (new_width, new_height))
    plt.imshow(resized_image)
