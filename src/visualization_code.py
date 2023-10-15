#!/usr/bin/env python

#!/usr/bin/env python

# import rospy
# from geometry_msgs.msg import Quaternion
# from visualization_msgs.msg import Marker, MarkerArray
# from geometry_msgs.msg import Point

# object_orientation = Quaternion()  # Stores the orientation of the object

# def imu_callback(orientation):
#     global object_orientation

#     # Create a MarkerArray to hold the markers for the main object and the axes
#     marker_array = MarkerArray()

#     # Create a main marker for the rectangle
#     marker = Marker()
#     marker.header.frame_id = "base_link"
#     marker.header.stamp = rospy.Time.now()
#     marker.id = 0  # ID for the main object
#     marker.type = Marker.CUBE
#     marker.action = Marker.ADD
#     marker.scale.x = 0.7  # Set a fixed size for the rectangle
#     marker.scale.y = 0.2  # Adjust the size as needed
#     marker.scale.z = 0.05  # Adjust the size as needed
#     marker.color.a = 1.0
#     marker.color.r = 1.0
#     marker.color.g = 0.0
#     marker.color.b = 0.0
#     marker.pose.position = Point(0, 0, 0)  # Keep the position fixed
#     marker.pose.orientation = orientation
#     marker_array.markers.append(marker)

#     # Create axes markers with the same orientation as the object
#     axis_length = 0.5  # Length of the axes

#     # Create the X-axis marker
#     x_axis_marker = Marker()
#     x_axis_marker.header.frame_id = "base_link"
#     x_axis_marker.header.stamp = rospy.Time.now()
#     x_axis_marker.id = 1  # ID for the X-axis
#     x_axis_marker.type = Marker.ARROW
#     x_axis_marker.action = Marker.ADD
#     x_axis_marker.scale.x = 0.02  # Width of the axis
#     x_axis_marker.scale.y = 0.02  # Height of the axis
#     x_axis_marker.scale.z = axis_length
#     x_axis_marker.color.a = 1.0
#     x_axis_marker.color.r = 1.0  # Red color
#     x_axis_marker.pose.position = Point(0, 0, 0)  # Keep the position fixed
#     x_axis_marker.pose.orientation = orientation  # Set the same orientation as the object
#     marker_array.markers.append(x_axis_marker)

#     # Create the Y-axis marker
#     y_axis_marker = Marker()
#     y_axis_marker.header.frame_id = "base_link"
#     y_axis_marker.header.stamp = rospy.Time.now()
#     y_axis_marker.id = 2  # ID for the Y-axis
#     y_axis_marker.type = Marker.ARROW
#     y_axis_marker.action = Marker.ADD
#     y_axis_marker.scale.x = 0.02  # Width of the axis
#     y_axis_marker.scale.y = 0.02  # Height of the axis
#     y_axis_marker.scale.z = axis_length
#     y_axis_marker.color.a = 1.0
#     y_axis_marker.color.g = 1.0  # Green color
#     y_axis_marker.pose.position = Point(0, 0, 0)  # Keep the position fixed
#     y_axis_marker.pose.orientation = orientation  # Set the same orientation as the object
#     marker_array.markers.append(y_axis_marker)

#     # Create the Z-axis marker
#     z_axis_marker = Marker()
#     z_axis_marker.header.frame_id = "base_link"
#     z_axis_marker.header.stamp = rospy.Time.now()
#     z_axis_marker.id = 3  # ID for the Z-axis
#     z_axis_marker.type = Marker.ARROW
#     z_axis_marker.action = Marker.ADD
#     z_axis_marker.scale.x = 0.02  # Width of the axis
#     z_axis_marker.scale.y = 0.02  # Height of the axis
#     z_axis_marker.scale.z = axis_length
#     z_axis_marker.color.a = 1.0
#     z_axis_marker.color.b = 1.0  # Blue color
#     z_axis_marker.pose.position = Point(0, 0, 0)  # Keep the position fixed
#     z_axis_marker.pose.orientation = orientation  # Set the same orientation as the object
#     marker_array.markers.append(z_axis_marker)

#     # Publish the MarkerArray
#     marker_pub.publish(marker_array)

# if __name__ == '__main__':
#     rospy.init_node('imu_visualization_node')

#     # Create a publisher for the MarkerArray
#     marker_pub = rospy.Publisher('imu_marker_array', MarkerArray, queue_size=10)

#     # Subscribe to the quaternion data topic
#     quaternion_sub = rospy.Subscriber('/imu/imu_corrected', Quaternion, imu_callback)

#     rospy.spin()



import rospy
from geometry_msgs.msg import Quaternion, TransformStamped
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import tf

# Define a function to apply a 90-degree rotation around the Z-axis
def apply_90_degree_rotation(quaternion):
    # Create a Quaternion message for a 90-degree Z-axis rotation
    rotation_quaternion = Quaternion()
    rotation_quaternion.x = 0.0
    rotation_quaternion.y = 0.0
    rotation_quaternion.z = 0.7071  # This is the sine of 45 degrees
    rotation_quaternion.w = 0.7071  # This is the cosine of 45 degrees

    # Convert the orientation and rotation quaternions to lists
    orientation_list = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
    rotation_list = [rotation_quaternion.x, rotation_quaternion.y, rotation_quaternion.z, rotation_quaternion.w]

    # Multiply the orientation quaternion by the rotation quaternion
    rotated_orientation = tf.transformations.quaternion_multiply(orientation_list, rotation_list)

    # Convert the result back to a Quaternion message
    rotated_quaternion = Quaternion()
    rotated_quaternion.x = rotated_orientation[0]
    rotated_quaternion.y = rotated_orientation[1]
    rotated_quaternion.z = rotated_orientation[2]
    rotated_quaternion.w = rotated_orientation[3]

    return rotated_quaternion

def imu_callback(orientation):
    # Apply the 90-degree rotation to the orientation
    rotated_orientation = apply_90_degree_rotation(orientation)

    # Create a Marker message for visualization
    marker = Marker()
    marker.header.frame_id = "base_link"  # Keep the frame ID as "base_link"
    marker.header.stamp = rospy.Time.now()
    marker.type = Marker.CUBE
    marker.action = Marker.ADD
    marker.scale.x = 0.7
    marker.scale.y = 0.2
    marker.scale.z = 0.05
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0
    marker.pose.position = Point(0, 0, 0)
    
    # Use the rotated orientation for tilting the rectangle
    marker.pose.orientation = rotated_orientation

    # Publish the marker
    marker_pub.publish(marker)

    # Create and broadcast the TF transformation
    transform_broadcaster = tf.TransformBroadcaster()
    transform_stamped = TransformStamped()

    transform_stamped.header.stamp = rospy.Time.now()
    transform_stamped.header.frame_id = "base_link"  # Keep the frame ID as "base_link"
    transform_stamped.child_frame_id = "orientation_frame"

    # Set the translation to the identity (no translation)
    transform_stamped.transform.translation.x = 0.0
    transform_stamped.transform.translation.y = 0.0
    transform_stamped.transform.translation.z = 0.0

    # Set the rotation from the rotated orientation
    transform_stamped.transform.rotation = rotated_orientation

    # Broadcast the transformation
    transform_broadcaster.sendTransform(
        (transform_stamped.transform.translation.x, transform_stamped.transform.translation.y, transform_stamped.transform.translation.z),
        (transform_stamped.transform.rotation.x, transform_stamped.transform.rotation.y, transform_stamped.transform.rotation.z, transform_stamped.transform.rotation.w),
        rospy.Time.now(),
        transform_stamped.child_frame_id,
        transform_stamped.header.frame_id
    )

if __name__ == '__main__':
    rospy.init_node('imu_visualization_node')

    marker_pub = rospy.Publisher('imu_marker', Marker, queue_size=10)
    quaternion_sub = rospy.Subscriber('/imu/imu_corrected', Quaternion, imu_callback)

    rospy.spin()


# # this little piggy code 2
# import rospy
# from geometry_msgs.msg import Quaternion, TransformStamped
# from visualization_msgs.msg import Marker
# from geometry_msgs.msg import Point
# import tf2_ros
# import tf2_geometry_msgs

# def imu_callback(orientation):
#     # Create a Marker message for visualization
#     marker = Marker()
#     marker.header.frame_id = "base_link"
#     marker.header.stamp = rospy.Time.now()
#     marker.type = Marker.CUBE
#     marker.action = Marker.ADD
#     marker.scale.x = 0.7  # Set a fixed size for the rectangle
#     marker.scale.y = 0.2  # Adjust the size as needed
#     marker.scale.z = 0.05  # Adjust the size as needed
#     marker.color.a = 1.0
#     marker.color.r = 1.0
#     marker.color.g = 0.0
#     marker.color.b = 0.0
#     marker.pose.position = Point(0, 0, 0)  # Keep the position fixed

#     # Use the orientation quaternion from the callback for tilting the rectangle
#     marker.pose.orientation = orientation

#     # Publish the marker
#     marker_pub.publish(marker)

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
#     transform_stamped.transform.rotation = orientation

#     transform_broadcaster.sendTransform(transform_stamped)

# if __name__ == '__main__':
#     rospy.init_node('imu_visualization_node')

#     # Create a publisher for the Marker message
#     marker_pub = rospy.Publisher('imu_marker', Marker, queue_size=10)

#     # Subscribe to the quaternion data topic
#     quaternion_sub = rospy.Subscriber('/imu/imu_corrected', Quaternion, imu_callback)

#     rospy.spin()

# import rospy
# from geometry_msgs.msg import Quaternion, TransformStamped
# from visualization_msgs.msg import Marker
# from geometry_msgs.msg import Point
# import tf2_ros
# import tf2_geometry_msgs
# import math  # Add math library for angle conversions

# def imu_callback(orientation):
#     # Convert the quaternion to Euler angles
#     roll, pitch, yaw = tf.transformations.euler_from_quaternion((orientation.x, orientation.y, orientation.z, orientation.w))

#     # Create a Marker message for visualization
#     marker = Marker()
#     marker.header.frame_id = "base_link"
#     marker.header.stamp = rospy.Time.now()
#     marker.type = Marker.CUBE
#     marker.action = Marker.ADD
#     marker.scale.x = 0.7  # Set a fixed size for the rectangle
#     marker.scale.y = 0.2  # Adjust the size as needed
#     marker.scale.z = 0.05  # Adjust the size as needed
#     marker.color.a = 1.0
#     marker.color.r = 1.0
#     marker.color.g = 0.0
#     marker.color.b = 0.0
#     marker.pose.position = Point(0, 0, 0)  # Keep the position fixed

#     # Use the converted Euler angles for tilting the rectangle
#     marker.pose.orientation = tf.transformations.quaternion_from_euler(roll, pitch, 0.0)

#     # Publish the marker
#     marker_pub.publish(marker)

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

#     # Set the rotation from the converted Euler angles
#     transform_stamped.transform.rotation = orientation

#     transform_broadcaster.sendTransform(transform_stamped)

# if __name__ == '__main__':
#     rospy.init_node('imu_visualization_node')

#     # Create a publisher for the Marker message
#     marker_pub = rospy.Publisher('imu_marker', Marker, queue_size=10)

#     # Subscribe to the quaternion data topic
#     quaternion_sub = rospy.Subscriber('/imu/imu_corrected', Quaternion, imu_callback)

#     rospy.spin()




# #!/usr/bin/env python
# #this little piggy is getting something
# import rospy
# from geometry_msgs.msg import Quaternion
# from visualization_msgs.msg import Marker
# from geometry_msgs.msg import Point
# import tf.transformations as tf_trans

# def imu_callback(orientation):
#     # Create a Marker message for visualization
#     marker = Marker()
#     marker.header.frame_id = "base_link"
#     marker.header.stamp = rospy.Time.now()
#     marker.type = Marker.CUBE
#     marker.action = Marker.ADD
#     marker.scale.x = 0.7  # Set a fixed size for the rectangle
#     marker.scale.y = 0.2  # Adjust the size as needed
#     marker.scale.z = 0.05  # Adjust the size as needed
#     marker.color.a = 1.0
#     marker.color.r = 1.0
#     marker.color.g = 0.0
#     marker.color.b = 0.0
#     marker.pose.position = Point(0, 0, 0)  # Keep the position fixed

#     # Use the orientation quaternion from the callback for tilting the rectangle
#     marker.pose.orientation = orientation

#     # Publish the marker
#     marker_pub.publish(marker)

# if __name__ == '__main__':
#     rospy.init_node('imu_visualization_node')

#     # Create a publisher for the Marker message
#     marker_pub = rospy.Publisher('imu_marker', Marker, queue_size=10)

#     # Subscribe to the quaternion data topic
#     quaternion_sub = rospy.Subscriber('/imu/imu_corrected', Quaternion, imu_callback)

#     rospy.spin()




# #!/usr/bin/env python

# import rospy
# from sensor_msgs.msg import Imu
# from visualization_msgs.msg import Marker
# from geometry_msgs.msg import Point, Quaternion
# import tf.transformations as tf_trans

# def imu_callback(imu_data):
#     # Extract orientation from IMU data
#     orientation = imu_data.orientation

#     # Check if the orientation is uninitialized (all zeros)
#     if orientation.x == 0.0 and orientation.y == 0.0 and orientation.z == 0.0 and orientation.w == 0.0:
#         rospy.logwarn("calculating quaternion values")
#         #publish_imu(orientation)  # Set identity quaternion
        
#     def publish_imu(imu_corrected):
#         imu_msg = Imu()
#         imu_msg.header.frame_id = IMU_FRAME

#         # Read the acceleration vals
#         accel_x = read_word_2c(ACCEL_XOUT_H) / 16384.0
#         accel_y = read_word_2c(ACCEL_YOUT_H) / 16384.0
#         accel_z = read_word_2c(ACCEL_ZOUT_H) / 16384.0
        
#         # Calculate a quaternion representing the orientation
#         '''accel = accel_x, accel_y, accel_z
#         ref = np.array([0, 0, 1])
#         acceln = accel / np.linalg.norm(accel)
#         axis = np.cross(acceln, ref)
#         angle = np.arccos(np.dot(acceln, ref))
#         orientation = quaternion_about_axis(angle, axis)'''

#         # Read the gyro vals
#         gyro_x = read_word_2c(GYRO_XOUT_H) / 131.0
#         gyro_y = read_word_2c(GYRO_YOUT_H) / 131.0
#         gyro_z = read_word_2c(GYRO_ZOUT_H) / 131.0
        
#         # Load up the IMU message
#         '''o = imu_msg.orientation
#         o.x, o.y, o.z, o.w = orientation'''

#         imu_msg.linear_acceleration.x = accel_x*9.8
#         imu_msg.linear_acceleration.y = accel_y*9.8
#         imu_msg.linear_acceleration.z = accel_z*9.8

#         imu_msg.angular_velocity.x = gyro_x*0.0174
#         imu_msg.angular_velocity.y = gyro_y*0.0174
#         imu_msg.angular_velocity.z = gyro_z*0.0174

#         imu_msg.header.stamp = rospy.Time.now()

#         imu_pub.publish(imu_msg)

#     # Create a Marker message for visualization
#     marker = Marker()
#     marker.header.frame_id = "base_link"
#     marker.header.stamp = rospy.Time.now()
#     marker.type = Marker.CUBE
#     marker.action = Marker.ADD
#     marker.scale.x = 0.7  # Set a fixed size for the rectangle
#     marker.scale.y = 0.2  # Adjust the size as needed
#     marker.scale.z = 0.05  # Adjust the size as needed
#     marker.color.a = 1.0
#     marker.color.r = 1.0
#     marker.color.g = 0.0
#     marker.color.b = 0.0
#     marker.pose.position = Point(0, 0, 0)  # Keep the position fixed

#     # Use the orientation from IMU data for tilting the rectangle
#     marker.pose.orientation = orientation

#     # Publish the marker
#     marker_pub.publish(marker)

# if __name__ == '__main__':
#     rospy.init_node('imu_visualization_node')
    
#     # Create a publisher for the Marker message
#     marker_pub = rospy.Publisher('imu_marker', Marker, queue_size=10)

#     # Subscribe to the IMU data topic
#     imu_sub = rospy.Subscriber('/imu/imu_corrected', Quaternion, imu_callback)

#     rospy.spin()
