#!/usr/bin/env python
#currently best working code, but it uses angular velocities directly, however the 2nd code is trying to integrate -
# - angular velocities over time using Euler integration
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



# #Euler tranformation of angular velocities over time
# import rospy
# from sensor_msgs.msg import Imu
# from geometry_msgs.msg import Quaternion
# from tf.transformations import quaternion_multiply, quaternion_from_euler

# # Define initial orientation
# current_orientation = quaternion_from_euler(0, 0, 0)
# last_update_time = None

# def imu_callback(data, imu_corrected_publisher):
#     global current_orientation, last_update_time

#     # Initialize the time if it hasn't been initialized yet
#     if last_update_time is None:
#         last_update_time = rospy.Time.now()
#         return

#     # Extract angular velocity data
#     angular_velocity = data.angular_velocity

#     # Calculate the time interval (dt) since the last update
#     current_time = rospy.Time.now()
#     dt = (current_time - last_update_time).to_sec()
#     last_update_time = current_time

#     # Compute the change in orientation using Euler integration and the time interval (dt)
#     delta_q = quaternion_from_euler(angular_velocity.x * dt, angular_velocity.y * dt, angular_velocity.z * dt)

#     # Update the current orientation
#     current_orientation = quaternion_multiply(current_orientation, delta_q)

#     # Publish the corrected orientation Quaternion
#     imu_corrected_publisher.publish(Quaternion(*current_orientation))

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














#other tries below




# import rospy
# from sensor_msgs.msg import Imu
# from tf.transformations import euler_from_quaternion, quaternion_multiply
# import tf2_ros
# from tf2_msgs.msg import TFMessage
# from geometry_msgs.msg import TransformStamped
# import numpy as np  # Add numpy library for angle conversion

# # Initialize the orientation quaternion as an identity quaternion
# current_orientation = np.array([0.0, 0.0, 0.0, 1.0])

# def imu_callback(data):
#     global current_orientation

#     # Extract angular velocity data
#     angular_velocity = data.angular_velocity

#     # Convert angular velocity from degrees per second to radians per second
#     angular_velocity_rad = np.deg2rad([angular_velocity.x, angular_velocity.y, angular_velocity.z])

#     # Create a quaternion from angular velocity in radians per second
#     delta_orientation = np.array([angular_velocity_rad[0], angular_velocity_rad[1], angular_velocity_rad[2], 0.0])

#     # Normalize the delta quaternion
#     norm = np.linalg.norm(delta_orientation)
#     delta_orientation /= norm

#     # Update the current orientation by multiplying with the incremental rotation
#     current_orientation = quaternion_multiply(current_orientation, delta_orientation)

#     # Create and broadcast the TF transformation
#     transform_broadcaster = tf2_ros.TransformBroadcaster()
#     transform_stamped = TransformStamped()

#     transform_stamped.header.stamp = rospy.Time.now()
#     transform_stamped.header.frame_id = "base_link"  # Parent frame
#     transform_stamped.child_frame_id = "orientation_frame"  # Child frame

#     # Set the translation to the identity (no translation)
#     transform_stamped.transform.translation.x = 0.0
#     transform_stamped.transform.translation.y = 0.0
#     transform_stamped.transform.translation.z = 0.0

#     # Set the rotation from the orientation
#     transform_stamped.transform.rotation.x = current_orientation[0]
#     transform_stamped.transform.rotation.y = current_orientation[1]
#     transform_stamped.transform.rotation.z = current_orientation[2]
#     transform_stamped.transform.rotation.w = current_orientation[3]

#     transform_broadcaster.sendTransform(transform_stamped)

# if __name__ == '__main__':
#     rospy.init_node('imu_subscriber')

#     # Subscribe to the quaternion data topic
#     quaternion_sub = rospy.Subscriber('/imu/data', Imu, imu_callback)

#     rospy.spin()






# #!/usr/bin/env python

# import rospy
# from sensor_msgs.msg import Imu
# from geometry_msgs.msg import Quaternion
# from tf.transformations import quaternion_from_euler, euler_from_quaternion

# # Initialize global variables for Euler angles
# roll = 0.0
# pitch = 0.0
# yaw = 0.0

# def imu_callback(data, imu_corrected_publisher):
#     global roll, pitch, yaw  # Declare as global to access the global variables

#     # Extract angular velocity data
#     angular_velocity = data.angular_velocity

#     # Convert angular velocities to radians per second
#     gyro_x = angular_velocity.x / 131.0 * 0.0174
#     gyro_y = angular_velocity.y / 131.0 * 0.0174
#     gyro_z = angular_velocity.z / 131.0 * 0.0174

#     # Integrate angular velocity to calculate Euler angles
#     roll += gyro_x * data.header.stamp.to_sec()
#     pitch += gyro_y * data.header.stamp.to_sec()
#     yaw += gyro_z * data.header.stamp.to_sec()

#     # Convert Euler angles to quaternion
#     orientation_quaternion = quaternion_from_euler(roll, pitch, yaw)

#     # Create a Quaternion message to store the corrected orientation
#     quaternion_msg = Quaternion()
#     quaternion_msg.x = orientation_quaternion[0]
#     quaternion_msg.y = orientation_quaternion[1]
#     quaternion_msg.z = orientation_quaternion[2]
#     quaternion_msg.w = orientation_quaternion[3]

#     # Publish the corrected orientation Quaternion on the /imu/imu_corrected topic
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
