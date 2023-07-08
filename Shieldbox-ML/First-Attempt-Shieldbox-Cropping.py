from torchvision.utils import ImageFont
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
from torchvision.io import read_image
from pathlib import Path

img_dir = './shieldbox/' #wherever photos from visual inspection are stored

##START CROPPING IMAGE
for full_image in os.listdir(img_dir): #for every image taken during visual inspection
    if full_image == '.ipynb_checkpoints': #bypass error with JupyterLab
        continue

    else:
        ##OPEN THE IMAGE
        image_local = full_image #make variables unrelated to for loop
        path_local = os.path.join(img_dir, image_local)
        image_color = cv.imread(path_local) #open the image
        img = cv.imread(path_local, cv.IMREAD_GRAYSCALE) #make the image black and white
        assert img is not None, "file could not be read, check with os.path.exists()"  #catch if image doesn't open
        img = img[1000:3000, 0:6000] #crop surrounding powerboards out
        img2 = img.copy() #make a new image, not a cropped image
        assert img is not None, "file could not be read, check with os.path.exists()" #catch if cropping didn't work

        ##OPEN THE TEMPLATE
        template = cv.imread('./pm.jpg', cv.IMREAD_GRAYSCALE) #open regular fiducial image from same location as visual inspection folder
        assert template is not None, "file could not be read, check with os.path.exists()" #catch if fiducial didn't open
        img = img2.copy() #return to using img variable instead of img2 for convenience

        ##LOCATE FIDUCIALS
        method = eval('cv.TM_CCORR_NORMED') #what method we'll use to find fiducials
        res = cv.matchTemplate(img,template,cv.TM_CCOEFF_NORMED) #how close is the fiducial template to actual fiducials
        threshold = 0.85 #high enough to remove false fiducials, low enough to account for variation
        loc = np.where( res >= threshold) #record locations of matched fiducials

        ##SORT AND REMOVE DUPLICATE FIDUCIALS
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
        
        ##LOCATE DISCOLORED FIDUCIALS
        if len(appxloc) < 5: #if fewer than five fiducials are found
            template = cv.imread('./dark-pm.png', cv.IMREAD_GRAYSCALE) #open discolored fiducial image from same location as visual inspection folder
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
                    for i in range(len(appxloc)): #if there's no prior pts
                        if abs(pt[0] - appxloc[i][0]) < 50: #if the current pt and the iterated pt in the list are close enough
                            overlap += 1 #increase variable

                    if overlap == 0: #if the current pt doesn't already exists in the list i.e. is far enough from preexisting pts
                        appxloc.append(pt) #add it to the list

                priorpt = pt #update the current pt to prior pt
                
        appxloc.sort(key=lambda a: a[0]) #sort the list by x coordinates
    
    ##DETERMINE PAIR OF FIDUCIALS AND CROP SHIELDBOX
    x1 = appxloc[0][0] #x coordinate of first pair in list
    y1 = appxloc[0][1] #y coordinate of first pair in list
    x2 = appxloc[1][0] #x coordinate of second pair in list
    y2 = appxloc[1][1] #y coordinate of second pair in list
    dy = y2 - y1 #distance between two pairs' y coordinates
    dx = x2 - x1 #distance between two pairs' x coordinates

    if x1/y1 < 1.5 and ((1.5 < x2/y2 < 3 and x2 < 3500) or (y1/y2 < 1 and x2 < 3500)): #if it's the first and second fiducials
        topleft_x_shield = int(x1 + 0.34*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 - 2.5*dy)
        bottomright_x_shield = int(x2 - 0.44*dx)
        bottomright_y_shield = int(y2 + 2.00*dy)

    elif x1/y1 < 1.5 and (x2/y2 > 3 and x2 < 3500): #if it's the first and third fiducials
        topleft_x_shield = int(x1 + 0.29*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 + 2.95*dy)
        bottomright_x_shield = int(x2 - 0.53*dx)
        bottomright_y_shield = int(y2 - 4.54*dy)
    
    elif x1/y1 < 1.5 and (x2/y2 < 5 and x2 > 3500 ): #if it's the first and fourth fiducials
        topleft_x_shield = int(x1 + 0.22*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 - 1.62*dy)
        bottomright_x_shield = int(x2 - 0.64*dx)
        bottomright_y_shield = int(y2 + 0.94*dy)
    
    elif x1/y1 < 1.5 and (x2/y2 > 5 and x2 > 3500): #if it's the first and fifth fiducials
        topleft_x_shield = int(x1 + 0.17*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 + 6.41*dy)
        bottomright_x_shield = int(x2 - 0.72*dx)
        bottomright_y_shield = int(y2 - 8.69*dy)
    
    elif (1.5 < x1/y1 < 3 and x1 < 3500) and (x2/y2 > 3 and x2 < 3500): #if it's the second and third fiducials
        topleft_x_shield = int(x1 - 3.58*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 + 1.89*dy)
        bottomright_x_shield = int(x2 - 3.39*dx)
        bottomright_y_shield = int(y2 - 2.08*dy)
    
    elif (1.5 < x1/y1 < 3 and x1 < 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the second and fourth fiducials
        topleft_x_shield = int(x1 - 1.17*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 - 6.45*dy)
        bottomright_x_shield = int(x2 - 1.78*dx)
        bottomright_y_shield = int(y2 + 2.69*dy)
    
    elif (1.5 < x1/y1 < 3 and x1 < 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the second and fifth fiducials
        topleft_x_shield = int(x1 - 0.67*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 - 0.15*dy)
        bottomright_x_shield = int(x2 - 1.44*dx)
        bottomright_y_shield = int(y2 - 2.44*dy)
    
    elif (x1/y1 > 3 and x1 < 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the third and fourth fiducials
        topleft_x_shield = int(x1 - 2.23*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 - 0.69*dy)
        bottomright_x_shield = int(x2 - 2.65*dx)
        bottomright_y_shield = int(y2 + 0.61*dy)
    
    elif (x1/y1 > 3 and x1 < 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the third and fifth fiducials
        topleft_x_shield = int(x1 - 1.05*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 - 3.61*dy)
        bottomright_x_shield = int(x2 - 1.77*dx)
        bottomright_y_shield = int(y2 + 7.41*dy)
    
    elif (x1/y1 > 5 and x1 > 3500) and (x2/y2 > 5 and x2 > 3500): #if it's the fourth and fifth fiducials
        topleft_x_shield = int(x1 - 2.84*dx) #find cropped range for shieldbox
        topleft_y_shield = int(y1 + 2.09*dy)
        bottomright_x_shield = int(x2 - 3.33*dx)
        bottomright_y_shield = int(y2 - 1.75*dy)
    
    #DISPLAY SHIELDBOX
    shield = img[topleft_y_shield:bottomright_y_shield,topleft_x_shield:bottomright_x_shield] #crop the range
    plt.imshow(shield) #display the crop
    plt.show()

