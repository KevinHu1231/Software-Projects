#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import numpy as np
import re
import sys, select, os

if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

def getKey():
    if os.name == 'nt':
      return msvcrt.getch()
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


class BayesLoc:

    def __init__(self, P0, colourCodes, colourMap, transProbBack, transProbForward):
        self.colour_sub = rospy.Subscriber('camera_rgb', String, self.colour_callback)
        self.line_sub = rospy.Subscriber('line_idx', String, self.line_callback)
        self.cmd_pub= rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.state_pub= rospy.Publisher('bay_state', String, queue_size=1)
        self.curState = P0 ## initial state probability is equal for all states
        self.colourCodes = colourCodes
        self.colourMap = colourMap
        self.transProbBack = transProbBack
        self.transProbForward = transProbForward
        self.numStates = len(P0)
        self.predState = np.zeros(np.shape(P0))

        self.CurColour = None ##most recent measured colour
        self.measuModel = np.matrix('0.60 0.20 0.05 0.05;0.20 0.60 0.05 0.05;0.05 0.05 0.65 0.20;0.05 0.05 0.15 0.60;0.10 0.10 0.10 0.10') #print(measuModel[2,3])
        self.stateModel = np.matrix('0.85 0.05 0.05; 0.10 0.90 0.10; 0.05 0.05 0.85') #print(stateModel[0,0])

 
    def colour_callback(self, msg):
        '''
        callback function that receives the most recent colour measurement from the camera.
        '''
        rgb = msg.data.replace('r:','').replace('b:','').replace('g:','').replace(' ','')
        r,g,b = rgb.split(',')
        r,g,b=(float(r), float(g),float(b))
        self.CurColour = [r,g,b]

    def line_callback(self, msg):
        '''
        TODO: Complete this with your line callback function from lab 3.
        '''
        return
    

    def waitforcolour(self):
        while(1):
            if self.CurColour is not None:
                break

    def measurement_model(self):
        if self.CurColour is None:
            self.waitforcolour()
        prob=np.zeros(len(self.colourCodes))
        for i in range(0,5):
            prob[i] = math.sqrt((self.CurColour[0]-self.colourCodes[i][0])**2+(self.CurColour[1]-self.colourCodes[i][1])**2+(self.CurColour[2]-self.colourCodes[i][2])**2)
        '''
        Measurement model p(z_k | x_k = colour) - given the pixel intensity, what's the probability that  
        TODO: You need to compute the probability of states. You should return a 1x5 np.array
        Hint: find the euclidean distance between the measured RGB values (self.CurColour) 
            and the reference RGB values of each color (self.ColourCodes).
        '''
        return np.argmin(prob)

    def statePredict(self):
        u=1
        self.predState = np.zeros(11)
        for i,val in enumerate(self.predState):
            self.predState[i] += self.stateModel[2,u+1]*self.curState[i-1]
            self.predState[i] += self.stateModel[1,u+1]*self.curState[i]
            if i == len(self.curState)-1:
                self.predState[i] += self.stateModel[0,u+1]*self.curState[0]
            else:
                self.predState[i] += self.stateModel[0,u+1]*self.curState[i+1]

    def stateUpdate(self,z):
        updatedState = np.zeros(11)
        summation = 0
        for i in range(0,len(self.predState)):
            summation += self.measuModel[z,self.colourMap[i]]*self.predState[i]
        for i in range(0,len(self.predState)):
            updatedState[i] = (self.measuModel[z,self.colourMap[i]] * self.predState[i])/summation
        self.curState = updatedState




if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    # 0: Blue, 1: Green, 2: Yellow, 3: Orange, 4: Line   
    color_maps = [2, 1, 0, 3, 3, 1, 0, 3, 2, 1, 0] #color_maps = [3, 0, 1, 2, 2, 0, 1, 2, 3, 0, 1] ## current map starting at cell#2 and ending at cell#12
    color_codes = [[206,206,255], #blue 145,145,255
                    [107, 255, 102], #green 72, 255, 72
                    [255, 255, 0], #yellow 
                    [255, 205, 0], #orange 255, 144, 0
                    [223.35,223.35,223.35]] #line 133,133,133

    desired_state = [5,7,2]
    offset = 2
    trans_prob_fwd = [0.1,0.9]
    trans_prob_back = [0.2,0.8]
                 
    rospy.init_node('final_project')
    bayesian=BayesLoc([1.0/len(color_maps)]*len(color_maps), color_codes, color_maps, trans_prob_back,trans_prob_fwd)
    prob = []
    rospy.sleep(0.5)    
    state_count = 0
    prev_state=None
    try:
        
        while (1):
            key = getKey()
            if (key == '\x03'): 
                rospy.loginfo('Finished!')
                rospy.loginfo(prob)
                break
            likelycol = bayesian.measurement_model()
            if likelycol != 4:
                bayesian.statePredict()
                bayesian.stateUpdate(likelycol)
                state_count += 1
                rospy.loginfo(np.argmax(bayesian.curState)+offset)
                if state_count>=4:
                    bayesian.state_pub.publish(str(np.argmax(bayesian.curState)+offset))
                    if np.argmax(bayesian.curState)+offset == desired_state[0] or np.argmax(bayesian.curState)+offset == desired_state[1] or np.argmax(bayesian.curState)+offset == desired_state[2]:
                        rospy.sleep(7)
                rospy.sleep(6)

            #rospy.loginfo("TODO: complete this main loop by calling functions from BayesLoc, and adding your own high level and low level planning + control logic")

    except Exception as e:
        print("comm failed:{}".format(e))

    finally:
        rospy.loginfo(bayesian.curState)
        cmd_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        twist = Twist()
        cmd_publisher.publish(twist)