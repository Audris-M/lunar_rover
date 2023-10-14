#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler

def imu_callback(data, imu_corrected_publisher):
    # Extract angular velocity data
    angular_velocity = data.angular_velocity

    # Create a Quaternion message to store the corrected orientation
    quaternion_msg = Quaternion()

    # Compute corrected angular velocity values and store them in the Quaternion message
    gyro_x = angular_velocity.x / 131.0
    gyro_y = angular_velocity.y / 131.0
    gyro_z = angular_velocity.z / 131.0

    quaternion_msg.x = gyro_x * 0.0174 * 1000
    quaternion_msg.y = gyro_y * 0.0174 * 1000
    quaternion_msg.z = gyro_z * 0.0174 * 1000

    # You can compute and set the orientation quaternion here, assuming you have the Euler angles
    # For example, if you have roll, pitch, and yaw angles
    roll = angular_velocity.x  # Replace with your actual roll angle
    pitch = angular_velocity.y  # Replace with your actual pitch angle
    yaw = angular_velocity.z  # Replace with your actual yaw angle

    orientation_quaternion = quaternion_from_euler(roll, pitch, yaw)
    quaternion_msg.x = orientation_quaternion[0]
    quaternion_msg.y = orientation_quaternion[1]
    quaternion_msg.z = orientation_quaternion[2]
    quaternion_msg.w = orientation_quaternion[3]

    # Publish the corrected orientation Quaternion on the /imu/imu_corrected topic
    imu_corrected_publisher.publish(quaternion_msg)
    
def imu_subscriber():
    rospy.init_node('imu_subscriber', anonymous=True)

    # Create a publisher for the corrected data
    imu_corrected_publisher = rospy.Publisher('/imu/imu_corrected', Quaternion, queue_size=10)
    
    rospy.Subscriber('/imu/data', Imu, imu_callback, callback_args=imu_corrected_publisher)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        imu_subscriber()
    except rospy.ROSInterruptException:
        pass






# #!/usr/bin/env python

# import rospy
# from sensor_msgs.msg import Imu
# from geometry_msgs.msg import Quaternion
# from tf.transformations import quaternion_from_euler

# def imu_callback(data, imu_corrected_publisher):
#     # Extract angular velocity data
#     angular_velocity = data.angular_velocity
#     orientation_quaternion = data.orientation

#     # Create a new Imu message to publish the corrected data
#     #imu_corrected_msg = Imu()
    
#     quaternion_msg = Quaternion()

#     # Compute corrected angular velocity values and store them in the new message
#     gyro_x = angular_velocity.x / 131.0
#     gyro_y = angular_velocity.y / 131.0
#     gyro_z = angular_velocity.z / 131.0
    
#     imu_corrected_msg.angular_velocity.x = gyro_x * 0.0174 * 1000
#     imu_corrected_msg.angular_velocity.y = gyro_y * 0.0174 * 1000
#     imu_corrected_msg.angular_velocity.z = gyro_z * 0.0174 * 1000

#     # Extract linear acceleration data
#     linear_acceleration = data.linear_acceleration

#     # Compute corrected linear acceleration values and store them in the new message
#     accel_x = linear_acceleration.x / 16384.0
#     accel_y = linear_acceleration.y / 16384.0
#     accel_z = linear_acceleration.z / 16384.0
    
#     imu_corrected_msg.linear_acceleration.x = accel_x * 9.8 * 1000
#     imu_corrected_msg.linear_acceleration.y = accel_y * 9.8 * 1000
#     imu_corrected_msg.linear_acceleration.z = accel_z * 9.8 * 1000

#     # You can compute and set the orientation quaternion here, assuming you have the Euler angles
#     # For example, if you have roll, pitch, and yaw angles
#     roll = angular_velocity.x  # Replace with your actual roll angle
#     pitch = angular_velocity.y  # Replace with your actual pitch angle
#     yaw = angular_velocity.z  # Replace with your actual yaw angle
#     orientation_quaternion = quaternion_from_euler(roll, pitch, yaw)

#     # imu_corrected_msg.orientation.x = orientation_quaternion[0]
#     # imu_corrected_msg.orientation.y = orientation_quaternion[1]
#     # imu_corrected_msg.orientation.z = orientation_quaternion[2]
#     # imu_corrected_msg.orientation.w = orientation_quaternion[3]
    
#     quaternion_msg = Quaternion()
#     quaternion_msg.x = orientation_quaternion[0]
#     quaternion_msg.y = orientation_quaternion[1]
#     quaternion_msg.z = orientation_quaternion[2]
#     quaternion_msg.w = orientation_quaternion[3]

#     # Publish the corrected data on the /imu/imu_corrected topic
#     #imu_corrected_publisher.publish(imu_corrected_msg.orientation.x,imu_corrected_msg.orientation.y,imu_corrected_msg.orientation.z,imu_corrected_msg.orientation.w)

#     imu_corrected_publisher.publish(quaternion_msg)
    
# def imu_subscriber():
#     rospy.init_node('imu_subscriber', anonymous=True)

#     # Create a publisher for the corrected data
#     imu_corrected_publisher = rospy.Publisher('/imu/imu_corrected', Quaternion, queue_size=10)
    
#     rospy.Subscriber('/imu/data', Imu, imu_callback, callback_args=imu_corrected_publisher)
    
#     rospy.spin()

# if __name__ == '__main__':
#     try:
#         imu_subscriber()
#     except rospy.ROSInterruptException:
#         pass
