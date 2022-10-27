'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
*  Created:				
*  Last Modified:		8/10/2022
*  Author:				e-Yantra Team
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
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
# 					[ Comma separated list of functions in this file ]
# Global variables:
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
from json import detect_encoding
import string
import sys
import traceback
import time
import os
import math
from turtle import distance
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################


def turn_left():
    rightjoint = sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
    sim.setJointTargetVelocity(rightjoint, 0.5)
    leftjoint = sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
    sim.setJointTargetVelocity(leftjoint, -0.5)

    time.sleep(2.5)
    sim.setJointTargetVelocity(rightjoint, 0.5)
    sim.setJointTargetVelocity(leftjoint, 0.5)


def turn_right():
    rightjoint = sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
    sim.setJointTargetVelocity(rightjoint, -0.5)
    leftjoint = sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
    sim.setJointTargetVelocity(leftjoint, 0.5)

    time.sleep(2.5)
    sim.setJointTargetVelocity(rightjoint, 0.5)
    sim.setJointTargetVelocity(leftjoint, 0.5)


def control_logic(sim):
    """
    Purpose:
    ---
    This function should implement the control logic for the given problem statement
    You are required to actuate the rotary joints of the robot in this function, such that
    it traverses the points in given order

    Input Arguments:
    ---
    `sim`    :   [ object ]
            ZeroMQ RemoteAPI object

    Returns:
    ---
    None

    Example call:
    ---
    control_logic(sim)
    """
    ##############  ADD YOUR CODE HERE  ##############
    front_distance = 0.2000000
    temp_front=0.28000
    frontd=0.20000
    rightlower = 0.17663122713565826
    leftlower = 0.2486077845096588
    corr = 0.02
    rightjoint = sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
    sim.setJointTargetVelocity(rightjoint, 0)
    leftjoint = sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
    sim.setJointTargetVelocity(leftjoint, 0)

    sim.setJointTargetVelocity(leftjoint, 0.5)
    sim.setJointTargetVelocity(rightjoint, 0.5)

    right_sensor = sim.getObjectHandle('/Diff_Drive_Bot/distance_sensor_2')
    front_sensor = sim.getObjectHandle('/Diff_Drive_Bot/distance_sensor_1')
    left_sensor = sim.getObjectHandle('/Diff_Drive_Bot/distance_sensor_3')
    flag = 0
    cp=0
    
    while (True):
        result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
            front_sensor)
        result1, distance1, detectedPoint1, detectedObjectHandle1, detectedSurfaceNormalVector1 = sim.readProximitySensor(
            right_sensor)
        result2, distance2, detectedPoint2, detectedObjectHandle2, detectedSurfaceNormalVector2 = sim.readProximitySensor(
            left_sensor)

        if (not flag):
            if (distance1 < rightlower and result1):
                sim.setJointTargetVelocity(leftjoint, 0.5-corr)
                sim.setJointTargetVelocity(rightjoint, 0.5+corr)
                print("left correction")
            elif (distance1 > rightlower and result1):
                sim.setJointTargetVelocity(leftjoint, 0.5+corr)
                sim.setJointTargetVelocity(rightjoint, 0.5-corr)
                print("right correction")

        else:
            if (distance2 < leftlower and result2):
                sim.setJointTargetVelocity(leftjoint, 0.5+corr)
                sim.setJointTargetVelocity(rightjoint, 0.5-corr)
                print("right correction")
            elif (distance2 > leftlower and result2):
                sim.setJointTargetVelocity(leftjoint, 0.5-corr)
                sim.setJointTargetVelocity(rightjoint, 0.5+corr)
                print("left correction")

        # print(f"{distance1}  {distance2}")
        if (distance < front_distance and result):
            if (result1):
                turn_left()
                cp+=1
                if(cp==5):
                    front_distance=temp_front
                    print('changed.........')
                else:
                    front_distance=frontd
                    print('not changed.........')


                flag = 0
                result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
                    front_sensor)
                result1, distance1, detectedPoint1, detectedObjectHandle1, detectedSurfaceNormalVector1 = sim.readProximitySensor(
                    right_sensor)
                result2, distance2, detectedPoint2, detectedObjectHandle2, detectedSurfaceNormalVector2 = sim.readProximitySensor(
                    left_sensor)
                if (result1):
                    rightlower = distance1
                if (result2):
                    leftlower = distance2
                if (result):
                    # print("breaking..........................")
                    turn_right()
                    sim.setJointTargetVelocity(rightjoint, 0)
                    sim.setJointTargetVelocity(leftjoint, 0)

                    return
            else:
                turn_right()
                cp+=1
                if(cp==5):
                    front_distance=temp_front
                    print('changed.........')

                else:
                    front_distance=frontd
                    print('not changed.........')

                flag = 1
                result1, distance1, detectedPoint1, detectedObjectHandle1, detectedSurfaceNormalVector1 = sim.readProximitySensor(
                    right_sensor)
                result2, distance2, detectedPoint2, detectedObjectHandle2, detectedSurfaceNormalVector2 = sim.readProximitySensor(
                    left_sensor)
                result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
                    front_sensor)
                if (result1):
                    rightlower = distance1
                if (result2):
                    leftlower = distance2
                if (result):
                    # print("breaking..........................")
                    turn_left()
                    sim.setJointTargetVelocity(rightjoint, 0)
                    sim.setJointTargetVelocity(leftjoint, 0)

                    return

    ##################################################


def detect_distance_sensor_1(sim):
    """
    Purpose:
    ---
    Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

    Input Arguments:
    ---
    `sim`    :   [ object ]
            ZeroMQ RemoteAPI object

    Returns:
    ---
    distance  :  [ float ]
        distance of obstacle from sensor

    Example call:
    ---
    distance_1 = detect_distance_sensor_1(sim)
    """
    distance = None
    ##############  ADD YOUR CODE HERE  ##############
    front_sensor = sim.getObjectHandle('/Diff_Drive_Bot/distance_sensor_1')
    result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
        front_sensor)

    ##################################################
    return distance


def detect_distance_sensor_2(sim):
    """
    Purpose:
    ---
    Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

    Input Arguments:
    ---
    `sim`    :   [ object ]
            ZeroMQ RemoteAPI object

    Returns:
    ---
    distance  :  [ float ]
        distance of obstacle from sensor

    Example call:
    ---
    distance_2 = detect_distance_sensor_2(sim)
    """
    distance = None
    ##############  ADD YOUR CODE HERE  ##############
    right_sensor = sim.getObjectHandle('/Diff_Drive_Bot/distance_sensor_2')
    result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(
        right_sensor)

    ##################################################
    return distance

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########


if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')

    try:

        # Start the simulation using ZeroMQ RemoteAPI
        try:
            return_code = sim.startSimulation()
            if sim.getSimulationState() != sim.simulation_stopped:
                print('\nSimulation started correctly in CoppeliaSim.')
            else:
                print('\nSimulation could not be started correctly in CoppeliaSim.')
                sys.exit()

        except Exception:
            print('\n[ERROR] Simulation could not be started !!')
            traceback.print_exc(file=sys.stdout)
            sys.exit()

        # Runs the robot navigation logic written by participants
        try:
            control_logic(sim)
            time.sleep(5)

        except Exception:
            print(
                '\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
            print('Stop the CoppeliaSim simulation manually if required.\n')
            traceback.print_exc(file=sys.stdout)
            print()
            sys.exit()

        # Stop the simulation using ZeroMQ RemoteAPI
        try:
            return_code = sim.stopSimulation()
            time.sleep(0.5)
            if sim.getSimulationState() == sim.simulation_stopped:
                print('\nSimulation stopped correctly in CoppeliaSim.')
            else:
                print('\nSimulation could not be stopped correctly in CoppeliaSim.')
                sys.exit()

        except Exception:
            print('\n[ERROR] Simulation could not be stopped !!')
            traceback.print_exc(file=sys.stdout)
            sys.exit()

    except KeyboardInterrupt:
        # Stop the simulation using ZeroMQ RemoteAPI
        return_code = sim.stopSimulation()
        time.sleep(0.5)
        if sim.getSimulationState() == sim.simulation_stopped:
            print('\nSimulation interrupted by user in CoppeliaSim.')
        else:
            print('\nSimulation could not be interrupted. Stop the simulation manually .')
            sys.exit()
