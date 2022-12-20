'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
#


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2
import numpy
from numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
import math
from cv2 import aruco
#from pyzbar import pyzbar
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################



def find_centres(image, arr):
    M = cv2.moments(arr)
    orx = int(M["m10"]/M["m00"])
    ory = int(M["m01"]/M["m00"])
    return [orx, ory]


def get_aruco_centers(image, centres):

    img = image
    ans = {}
    corners = {}
    idlist = []
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{5}X{5}_{250}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, _ = aruco.detectMarkers(
        imgray, arucoDict, parameters=arucoParam)
    if ids is None:
        pass
    else:
        for id in ids:
            idlist.append(int(id[0]))
        if (True):
            aruco.drawDetectedMarkers(img, bboxs)

        for i in range(0, len((bboxs))):
            ans[idlist[i]] = []
            corners[idlist[i]] = None
            list_temp = []
            x1 = int((((bboxs[i])[0])[0])[0])
            y1 = int((((bboxs[i])[0])[0])[1])
            x1s = str(x1)
            y1s = str(y1)
            # cv2.putText(img, (x1s+' '+y1s), (x1, y1),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3, cv2.LINE_AA)
            x2 = int((((bboxs[i])[0])[1])[0])
            y2 = int((((bboxs[i])[0])[1])[1])

            for it1, it2 in (bboxs[i])[0]:
                extemp = []
                extemp.append(it1)
                extemp.append(it2)
                list_temp.append(extemp)

            corners[idlist[i]] = list_temp

            centre = find_centres(img, ((bboxs[i])[0]))
            ans[idlist[i]].append(centre)
            centres.append(centre)
    return centres
#####################################################################################


def perspective_transform(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.
    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.
    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 
    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    Example call:
    ---
    warped_image = perspective_transform(image)
    """
    warped_image = []
#################################  ADD YOUR CODE HERE  ###############################
    centres = []
    global flag
    global top_left_x
    global top_left_y 
    global bot_right_x
    global bot_right_y
    ori = image
    if (not flag):
        get_aruco_centers(image, centres)
    # top_left_x = 1000000
    # top_left_y = 1000000
    # bot_right_x = -10000
    # bot_right_y = -10000

    if (len(centres) >= 3 and flag == False):

        flag = True
        for x, y in centres:
            top_left_x = min(top_left_x, x)
            top_left_y = min(top_left_y, y)
            bot_right_x = max(bot_right_x, x)
            bot_right_y = max(bot_right_y, y)
    if (flag):
        imt = ori[top_left_y:bot_right_y-2, top_left_x:bot_right_x-2]
        warped_image.append(imt)
######################################################################################
    return warped_image


def transform_values(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.
    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera
    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    Example call:
    ---
    scene_parameters = transform_values(image)
    """
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    g = []
    centre5 = get_aruco_centers(image, g)
    # print(centre5)
    if (len(centre5)):
        x, y = centre5[0]
        y = ((y*(1.91/512))-0.955)
        x = ((-(x*(1.91/512)))+0.955)
        # handle = sim.getObjectHandle('/aruco_5')
        # pos = sim.getObjectPosition(handle, -1)
        # print(pos)
        # sim.setObjectPosition(handle, -1, [x, y, 0.1])
        scene_parameters.append(x)
        scene_parameters.append(y)
######################################################################################

    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.
    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function
    Returns:
    ---
    None
    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    Example call:
    ---
    set_values(scene_parameters)
    """
    # aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################
    if len(scene_parameters) > 0:
        x = scene_parameters[0]
        y = scene_parameters[1]
        handle = sim.getObjectHandle('/aruco_5')
        pos = sim.getObjectPosition(handle, -1)
        print(pos)
        sim.setObjectPosition(handle, -1, [x, y, 0.1])
######################################################################################

    return None



if __name__ == "__main__":
    
    flag = False
    top_left_x = 0
    top_left_y = 0
    bot_right_x = 0
    bot_right_y = 0
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
#################################  ADD YOUR CODE HERE  ################################
    cap = cv2.VideoCapture(1)
    while (True):
        _, frame0 = cap.read()
        frame = perspective_transform(frame0)
        if (len(frame)):
            frame1 = cv2.resize(frame[0], (512, 512),
                                interpolation=cv2.INTER_CUBIC)
            cv2.imshow('img', frame1)
            cv2.waitKey(1)
            scene_param=transform_values(frame1)
            set_values(scene_param)
        else:
            cv2.imshow('img', frame0)
            cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
#######################################################################################
