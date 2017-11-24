#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://robotcontrolit.com/documentation/gui_jpos

import rospy                        #for interacting with ROS topics and parameters
import sys, getopt                  #for parameters and sys.exit()
from Tkinter import *               #for GUI elements
from std_msgs.msg import Float64MultiArray, MultiArrayDimension
import re                           #for findall()
import string                       #for split()
from controlit_core.srv import *    #for indices service (used to sort joint indices)

# --- IMPORTS AND INITIALIZATION ---

#initialize ROS node
rospy.init_node('GUIControl', anonymous=True)

#Get the GUI width from the user
#width = input("Please input the number of columns desired:")
width = 1;  # Solo una columna

# initialize Tkinter master
master = Tk()
master.title("Control GUI")

# --- PUBLISHER ---

#initialize publisher
goalPublisher = rospy.Publisher(publishTopic, Float64MultiArray)

# --- CREATING THE JOINT CLASS ---
#The joint class will create the scale and entry elements in the GUI for each DOF
class Joint:
    nameList = []
    jointList = [] # contains all of the joint elements
    def __init__(self,Label,Min,Max,outFrame):
        self.frame = Frame(outFrame)
        self.scale = Scale(self.frame, from_=Min, to=Max, orient = HORIZONTAL, resolution = 0.05)
        self.scale.config(length = 200, label = Label)
        self.scale.bind()
        self.scale.pack(side = LEFT)
        self.en = Entry(self.frame)
        self.en.bind("<return>", lambda e: self.setSlider()) #hitting ENTER in the entry box will run setSlider() on the joint
        self.en.config(width = 3)
        self.en.pack(side = LEFT)
        self.frame.pack(side = LEFT)
        Joint.nameList.append(Label)
        Joint.jointList.append(self)
    def getVal(self):
        return self.scale.get() # will return the scale value
    def setSlider(Joint):
        Joint.scale.set(float(Joint.en.get())) # get the entry value and set the slider to it
        Joint.en.delete(0,END) # clear the entry box

# --- GATHER THE JOINT DATA ---
def getArray():
    tempArray=[]
    for el in joint.jointlist:
        tempArray.append(el.getVal())
    return tempArray


initArray = getArray()

#create the MultiArray to be published
dim = MultiArrayDimension()
dim.size = len(initArray)
dim.label = "posMsg"
dim.stride = len(initArray)

goalArray = Float64MultiArray()
goalArray.data = initArray
goalArray.layout.dim.append(dim)
goalArray.layout.data_offset = 0

def updateGoal():
    goalArray.data = getArray()
    goalPublisher.publish(goalArray)
    master.after(50,updateGoal)

master.after(50,updateGoal) # update the goal every 50 ms (20 Hz)
mainloop()
