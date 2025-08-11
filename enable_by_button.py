#!/usr/bin/env python
'''
Rosnode to listen to DriverInput (button presses on steering wheel) and publishes a /vehicle/enable message upon receiving the Cruise-Decel button command. This will enable the vehicle "put it into autonomous mode" if the vehicle is ready, this code replacing running the command $ rostopic pub /vehicle/enable std_msgs/Empty "{}"
'''
import rospy
from std_msgs.msg import Empty
from raptor_dbw_msgs.msg import DriverInputReport

class VehicleEnableNode:
    def __init__(self):
        rospy.init_node("vehicle_enabler_node")

        self.pub_activate = rospy.Publisher("/vehicle/enable", Empty)

        rospy.Subscriber(
            "/vehicle/driver_input_report",
            DriverInputReport,
            self.driver_input_report_callback,
            queue_size=1
        )

        rospy.loginfo("Vehicle Enable Node running.")
        rospy.spin()

    def driver_input_report_callback(self, msg):
        if msg.cruise_decel_button:
            rospy.loginfo("Button push received - sending enable command")
            self.pub_activate.publish(Empty())

if __name__ == "__main__":
    try:
        VehicleEnableNode()
    except rospy.ROSInterruptException:
        pass

