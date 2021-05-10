#!/usr/bin/env python

import rospy
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
        self.pos_sub = rospy.Subscriber('state', String, self.pos_callback, queue_size=1)
        self.pixel = 320
        self.pos = 0
        '''
        complete the function
        '''


    def camera_callback(self, data):
        self.pixel = int(data.data)
        rospy.loginfo("pixel: %s", data.data)
        '''
        complete the function
        '''
        pass

    def pos_callback(self, data):
        self.pos = float(data.data)
        rospy.loginfo("pos: %s", data.data)
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
        rospy.loginfo(abs(self.pos-5.5))
        if abs(self.pos-2.1) < 0.01 or abs(self.pos-3.2) < 0.01 or abs(self.pos-5.5) < 0.01:
            twist.linear.x = 0
            self._cmd_pub.publish(twist)
            rospy.sleep(4)    
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



