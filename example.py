import yarp
import numpy
import time
from pyquaternion import Quaternion

def go_to_pose(cart, position, orientation):

    position_yarp = yarp.Vector(3)
    for i in range(3):
        position_yarp[i] = position[i]

    tmp_quaternion = Quaternion(matrix = orientation)
    tmp_axis = tmp_quaternion.axis
    tmp_angle = tmp_quaternion.angle

    axis_angle_yarp = yarp.Vector(4)
    for i in range(3):
        axis_angle_yarp[i] = tmp_axis[i]
    axis_angle_yarp[3] = tmp_angle

    cart.goToPoseSync(position_yarp, axis_angle_yarp)


def main():

    laterality = 'right'
    robot_name = 'icubSim'

    props = yarp.Property()
    props.put('device', 'cartesiancontrollerclient');
    props.put('local', '/example/' + laterality + '_arm')
    props.put('remote', '/' + robot_name + '/cartesianController/' + laterality + '_arm')
    cart_driver = yarp.PolyDriver(props)
    cart = cart_driver.viewICartesianControl()
    cart.setTrajTime(2.0)

    initial_position = [-0.32, 0.16, 0.1]
    initial_orientation = Quaternion(axis = [0.0, 1.0, 0.0], angle = numpy.pi).rotation_matrix

    steps = 10
    sweep = 120.0
    for i in range(steps):

        # Write a rotation matrix representing a perturbation
        angle = (-sweep / 2.0 + sweep / steps * i) * numpy.pi / 180.0
        delta_orientation_fixed_axes = Quaternion(axis = [0.0, 0.0, 1.0], angle = angle).rotation_matrix

        # Left-multiply in order to apply the perturbation with respect to the inertial reference frame
        orientation = delta_orientation_fixed_axes.dot(initial_orientation)

        # Send the pose
        print("Step " + str(i + 1) + "/" + str(steps) + "...")
        go_to_pose(cart, initial_position, orientation)
        time.sleep(3.0)


if __name__ == '__main__':
    main()
