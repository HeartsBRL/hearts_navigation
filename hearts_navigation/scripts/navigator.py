#!/usr/bin/env python

import rospy
import tf
from actionlib import SimpleActionClient
from geometry_msgs.msg import PoseStamped, Pose, Pose2D
from actionlib_msgs.msg import GoalStatusArray, GoalID
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
from std_msgs.msg import UInt8
#from roah_rsb_comm_ros import BenchmarkState

class Navigator():

    def __init__(self):

        self.isNavigating = False
        #self.statusNeeded = 0 #TODO consider removing, seriously
        self.currentGoal = Pose2D()
        self.lastGoal = Pose2D()


        self.pubGoal = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
        self.cancel_move = rospy.Publisher("move_base/cancel", GoalID, queue_size=1)

        self.moveAC = SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("Waiting for Move Base Action Server")
        self.moveAC.wait_for_server()

        #self.pubGoal = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=1)

        self.pubStatus = rospy.Publisher('/hearts/navigation/status', String, queue_size=1)
        self.pubPose = rospy.Publisher('/hearts/navigation/current', String, queue_size=1)

        self.previous_state = ""
        self.t = PoseStamped()
        rospy.Subscriber('move_base/status', GoalStatusArray, self.StatusCallback)   # Get status of plan

        rospy.Subscriber('hearts/navigation/goal_shortcut', PoseStamped, self.goalCallback2)
        rospy.Subscriber('hearts/navigation/goal', Pose2D, self.goalCallback)
        rospy.Subscriber('hearts/navigation/stop', String, self.stopCallback)

    def goalCallback(self, data):

        rospy.loginfo("Navigator: goal Callback")

        # Make sure the robot isn't already trying to go somewhere
        if(self.isNavigating == True):
            rospy.loginfo("Navigator: currently navigating, can't continue at the moment.")
        else:
            rospy.loginfo("Navigator: sending new goal pose")
            self.isNavigating = True
            # @TODO add some form of checking to data:

            self.currentGoal = data

            # Convert Pose2D to PoseStamped
            self.t = PoseStamped()
            self.t.header.frame_id = "/erl_frame"
            self.t.pose.position.x = data.x
            self.t.pose.position.y = data.y
            #t.pose.orientation.w = data.theta
            quaternion = tf.transformations.quaternion_from_euler(0, 0, data.theta)
            self.t.pose.orientation.x = quaternion[0]
            self.t.pose.orientation.y = quaternion[1]
            self.t.pose.orientation.z = quaternion[2]
            self.t.pose.orientation.w = quaternion[3]
            # = createQuaternionMsgFromYaw(data.theta)
            rospy.loginfo(str(data.x)+ str(data.y)+ str(data.theta))

            self.pubGoal.publish(self.t)
            self.isNavigating = True

    def goalCallback2(self, data):

            self.goal = MoveBaseGoal()
            self.goal.target_pose = self.t
            rospy.loginfo(self.goal)

            self.moveAC.send_goal(self.goal)
            print("move goal sent")
            #TODO change duration for real thing
            self.wait_result = self.moveAC.wait_for_result(timeout=rospy.Duration(60))
            print("wait done")
            print self.wait_result
            if self.wait_result:
                print(self.moveAC.get_result())
                print("yp")
                #self.statusNeeded = 1
            self.isNavigating = False


        rospy.loginfo("Navigator: goal Callback (shortcut)")

        # Make sure the robot isn't already trying to go somewhere
        if(self.isNavigating == True):
            rospy.loginfo("Navigator: currently navigating, can't continue at the moment.")
        else:
            rospy.loginfo("Navigator: sending new goal pose")

            self.pubGoal.publish(data)
            self.isNavigating = True

    def stopCallback(self, data):
        #clear all navigation goals
        msg = GoalID()
        self.cancel_move.publish(msg)
        self.isNavigating = False
        rospy.loginfo("Cleared navigation stack")

    def StatusCallback(self, data):
        #rospy.loginfo("Naughty naughty")
        if True: #self.statusNeeded == 1:
            length_status = len(data.status_list)

            if length_status > 0:
                status = data.status_list[length_status-1].status
                status_msg = String()
                if status == 4 or status == 5 or status == 9:
                    status_msg.data = 'Fail'
                    self.isNavigating = False
                elif status==3:
                    status_msg.data = 'Success'
                    self.lastGoal = self.currentGoal
                    self.currentGoal = Pose2D()
                    self.isNavigating = False
                    self.repeat = False
                elif status==1:
                    status_msg.data = 'Active'
                    rospy.loginfo("Navigating is active, so it is")
                    self.isNavigating = True
                #else:
                    #rospy.loginfo("I No Naaaffin")


                if self.previous_state != status_msg.data:
                    self.pubStatus.publish(status_msg)
                    self.previous_state = status_msg.data
                    rospy.loginfo('status: ' + str(status))
            self.statusNeeded = 0



if __name__ == '__main__':
        rospy.init_node('Navigator', anonymous=False)
        rospy.loginfo("Navigator has started")
        n = Navigator()
        rospy.spin()
