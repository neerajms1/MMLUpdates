#!/usr/bin/python -u
#
# NB: the -u means do not buffer stdout, which means
# we get instant feedback to the web client when there
# is output generated by the script.

import rospy
import sys
import os
# report
print "[starting user script]"

# initialise ROS node
print "initialising ROS..."
rospy.init_node("client_web")


################################################################

# imports
import time
import miro2 as miro
import mml
import random

# definitions

colorIndex = None
ColorList = None
currentTime = None
startTime = None

"""When called it has a 20% chance of making MiRo Blink
"""
def Eye_movement():
  global j, colorIndex, ColorList, currentTime, startTime
  if random.randint(1, 5) == 1:
    robot.set_joint(miro.constants.JOINT_EYE_L, 1.0)
    robot.set_joint(miro.constants.JOINT_EYE_R, 1.0)
    robot.sleep(0.4)
    robot.set_joint(miro.constants.JOINT_EYE_L, 0.0)
    robot.set_joint(miro.constants.JOINT_EYE_R, 0.0)

"""Cycles through the colors and set MiRo colors
"""
def Colors(x=False):
  global colorIndex, ColorList, currentTime, startTime
  if x ==  False:
    for j in range(6):
      robot.control_led(j,ColorList[colorIndex] ,255)

    if len(ColorList) - 1 == colorIndex:
      colorIndex = 0
    else:
      colorIndex = colorIndex + 1
  if x == True:
    for j in range(6):
      robot.control_led(j,"#FFFFFF" ,255)

"""Describe this function...
"""
def Neck_Movement():
  global j, colorIndex, ColorList, currentTime, startTime
  robot.set_neck(miro.constants.JOINT_LIFT, (random.randint(-15, 15)))
  robot.set_neck(miro.constants.JOINT_YAW, (random.randint(-60, 60)))
  robot.set_neck(miro.constants.JOINT_PITCH, (random.randint(7, 15)))

"""When called it has a 20% chance of making MiRo Blink
"""
def Wag_tail_chance():
  global j, colorIndex, ColorList, currentTime, startTime
  if random.randint(1, 10) == 1:
    robot.wag_tail(2, 30)


# setup
robot = miro.interface.PlatformInterface()
time.sleep(1.0)

# control
import time

startTime = time.time()

currentTime = 0

mml.play("/home/miro/mdk/share/media/Head_Shoulders_Knees_and_Toes.mp3")
# Red
# Orange
# Yellow
# Green
# Blue
# Indigo
# Violet
ColorList = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
colorIndex = 0

def check_for_shutdown():
	resp = robot.read_head_touch_sensors()
	if resp[4] and resp[11]:
		ctime = time.time()
		print("Head Touched")
		while resp[4] and resp[11]:
			resp = robot.read_head_touch_sensors()
			if time.time() - ctime >= 2:
				os.system("rosnode kill mml_play")
				for j in range(6):
					robot.control_led(j,"#ffffff" ,255)
				os.remove("/tmp/running.state")
				os.system("rosnode kill client_web")
				
				sys.exit()
	
time.sleep(2)
while currentTime - startTime < 50:
	currentTime = time.time()
	Colors(False)
	check_for_shutdown()
	Eye_movement()
	check_for_shutdown()
	Neck_Movement()
	check_for_shutdown()
	Wag_tail_chance()
	check_for_shutdown()
	robot.set_turn_speed((random.randint(-70, 70)))
	check_for_shutdown()
	robot.sleep(1)
	
Colors(True)

robot.sleep(2)
robot.exit()
