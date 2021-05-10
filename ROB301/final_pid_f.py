#!/usr/bin/env python

import rospy
import numpy as np
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys, select, os
if os.name == 'nt':
    import msvcrt
else:
    import tty, termios

e = """
Communications Failed
"""

def getKey(): #you can ignore this function. It's for stopping the robot when press 'Ctrl+C'
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



class PIDcontrol():
    def __init__(self):
        self._cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.color_sub = rospy.Subscriber('line_idx', String, self.camera_callback, queue_size=1)
        self.rgb_sub = rospy.Subscriber('camera_rgb', String, self.colour_callback)
        self.state_sub = rospy.Subscriber('bay_state', String, self.state_callback)
        self.pixel = 320
        self.CurColour = np.array([0,0,0])
        self.state = None
        self.desired_state = [5,7,2]
        '''
        complete the function
        '''


    def camera_callback(self, data):
        self.pixel = int(data.data)
        #rospy.loginfo("pixel: %s", data.data)
        '''
        complete the function
        '''
        pass

    def colour_callback(self, msg):
        '''
        callback function that receives the most recent colour measurement from the camera.
        '''
        rgb = msg.data.replace('r:','').replace('b:','').replace('g:','').replace(' ','')
        r,g,b = rgb.split(',')
        r,g,b=(float(r), float(g),float(b))
        self.CurColour = np.array([r,g,b])

    def state_callback(self, data):
        self.state = int(data.data)
        rospy.loginfo("state: %s", data.data)
        rospy.loginfo(self.state==self.desired_state[0] or self.state==self.desired_state[1] or self.state==self.desired_state[2])
        '''
        complete the function
        '''
        pass

    def follow_the_line(self):
        desired = 320
        integral = 0
        derivative = 0
        lasterror = 0
        kp = 1.6*0.6/320
        ki = 1.6*2.0/5/320
        kd = 1.6*0.125/5/320
        actual = self.pixel
        error = desired - actual
        integral = integral + error
        derivative = error - lasterror
        correction = kp*error + ki*integral + kd * derivative
        
        err = 10.0

        if abs(self.CurColour[0] - 223.35) < err and abs(self.CurColour[1] - 223.35) < err and abs(self.CurColour[2] - 223.35) < err:
            twist=Twist()
            twist.linear.x=0.1
            twist.linear.y=0
            twist.linear.z=0
            twist.angular.x=0
            twist.angular.y=0
            twist.angular.z=correction
            self._cmd_pub.publish(twist)
            rospy.sleep(0.01)
            lasterror = error
        elif self.state==self.desired_state[0] or self.state==self.desired_state[1] or self.state==self.desired_state[2]:
            twist=Twist()
            twist.linear.x=0.1
            twist.linear.y=0
            twist.linear.z=0
            twist.angular.x=0
            twist.angular.y=0
            twist.angular.z=0
            self._cmd_pub.publish(twist)
            rospy.sleep(2)

            twist.linear.x=0
            twist.angular.z=math.pi/4
            self._cmd_pub.publish(twist)
            rospy.sleep(2)

            twist.linear.x=0
            twist.angular.z=0
            self._cmd_pub.publish(twist)
            rospy.sleep(3)

            twist.angular.z=-math.pi/4
            self._cmd_pub.publish(twist)
            rospy.sleep(2)

            twist.angular.z=0
            self._cmd_pub.publish(twist)
            rospy.sleep(0.1)

            twist.linear.x=0.1
            self._cmd_pub.publish(twist)
            rospy.sleep(1)

            self.state = None

        else:
            twist=Twist()
            twist.linear.x=0.1
            twist.linear.y=0
            twist.linear.z=0
            twist.angular.x=0
            twist.angular.y=0
            twist.angular.z=0
            self._cmd_pub.publish(twist)
            rospy.sleep(0.01)
        '''
        complete the function
        '''
        pass


if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)
        
    rospy.init_node('Lab3')
    PID = PIDcontrol()
    try:
        while(1):
            key = getKey()
            PID.follow_the_line()
            if (key == '\x03'): #stop the robot when exit the program
                break
    except rospy.ROSInterruptException:
        print("comm failed")

