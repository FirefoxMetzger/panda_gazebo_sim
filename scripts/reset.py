import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

import numpy as np
# END_SUB_TUTORIAL


STARTING_POS = np.array([
    1.5144076375347826,
    -0.6726638697722728,
    0.18543326279796127,
    -2.9585892121572526,
    0.12056011035042515,
    2.3006689352724274,
    0.7933720851335472
])


def all_close(goal, actual, tolerance):
    """
    Convenience method for testing if a list of values are within a tolerance of
    their counterparts in another list
    @param: goal       A list of floats, a Pose or a PoseStamped
    @param: actual     A list of floats, a Pose or a PoseStamped
    @param: tolerance  A float @returns: bool
    """
    all_equal = True
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False

    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

    return True


class MoveGroupPythonIntefaceTutorial(object):
    """MoveGroupPythonIntefaceTutorial"""

    def __init__(self):
        super(MoveGroupPythonIntefaceTutorial, self).__init__()

        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('move_group_python_interface_tutorial',
                        anonymous=True)

        # Instantiate a `RobotCommander`_ object. This object is the outer-level
        # interface to the robot:
        robot = moveit_commander.RobotCommander()

        # Instantiate a `PlanningSceneInterface`_ object.  This object is an
        # interface to the world surrounding the robot:
        scene = moveit_commander.PlanningSceneInterface()

        # Instantiate a `MoveGroupCommander`_ object.  This object is an
        # interface to one group of joints.  In this case the group is the
        # joints in the Panda arm so we set ``group_name = panda_arm``. If you
        # are using a different robot, you should change this value to the name
        # of your robot arm planning group. This interface can be used to plan
        # and execute motions on the Panda:
        group_name = "panda_arm"
        group = moveit_commander.MoveGroupCommander(group_name)

        # We create a `DisplayTrajectory`_ publisher which is used later to
        # publish trajectories for RViz to visualize:
        display_trajectory_publisher = rospy.Publisher(
            '/move_group/display_planned_path',
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20
        )

        # END_SUB_TUTORIAL

        # BEGIN_SUB_TUTORIAL basic_info
        ##
        # Getting Basic Information
        # ^^^^^^^^^^^^^^^^^^^^^^^^^
        # We can get the name of the reference frame for this robot:
        planning_frame = group.get_planning_frame()
        print "============ Reference frame: %s" % planning_frame

        # We can also print the name of the end-effector link for this group:
        eef_link = group.get_end_effector_link()
        print "============ End effector: %s" % eef_link

        # We can get a list of all the groups in the robot:
        group_names = robot.get_group_names()
        print "============ Robot Groups:", robot.get_group_names()

        # Sometimes for debugging it is useful to print the entire state of the
        # robot:
        print "============ Printing robot state"
        print robot.get_current_state()
        print ""
        # END_SUB_TUTORIAL

        # Misc variables
        self.box_name = ''
        self.robot = robot
        self.scene = scene
        self.group = group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names

    def go_to_joint_state(self):
        # Copy class variables to local variables to make the web tutorials more
        # clear. In practice, you should use the class variables directly unless
        # you have a good reason not to.
        group = self.group

        # BEGIN_SUB_TUTORIAL plan_to_joint_state
        ##
        # Planning to a Joint Goal
        # ^^^^^^^^^^^^^^^^^^^^^^^^
        # The Panda's zero configuration is at a `singularity
        # <https://www.quora.com/Robotics-What-is-meant-by-kinematic-singularity>`_
        # so the first thing we want to do is move it to a slightly better
        # configuration. We can get the joint values from the group and adjust
        # some of the values:
        joint_goal = group.get_current_joint_values()
        joint_goal[0] = 0
        joint_goal[1] = -pi / 4
        joint_goal[2] = 0
        joint_goal[3] = -pi / 2
        joint_goal[4] = 0
        joint_goal[5] = pi / 3
        joint_goal[6] = 0

        # The go command can be called with joint values, poses, or without any
        # parameters if you have already set the pose or joint target for the
        # group
        group.go(joint_goal, wait=True)

        # Calling ``stop()`` ensures that there is no residual movement
        group.stop()

        # END_SUB_TUTORIAL

        # For testing: Note that since this section of code will not be included
        # in the tutorials we use the class variable rather than the copied
        # state variable
        current_joints = self.group.get_current_joint_values()
        return all_close(joint_goal, current_joints, 0.01)

    def go_to_pose_goal(self):
        # Copy class variables to local variables to make the web tutorials more
        # clear. In practice, you should use the class variables directly unless
        # you have a good reason not to.
        group = self.group

        # BEGIN_SUB_TUTORIAL plan_to_pose
        ##
        # Planning to a Pose Goal
        # ^^^^^^^^^^^^^^^^^^^^^^^
        # We can plan a motion for this group to a desired pose for the
        # end-effector:
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = 1.0
        pose_goal.position.x = 0.4
        pose_goal.position.y = 0.1
        pose_goal.position.z = 0.4
        group.set_pose_target(pose_goal)

        # Now, we call the planner to compute the plan and execute it.
        plan = group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement
        group.stop()
        # It is always good to clear your targets after planning with poses.
        # Note: there is no equivalent function for clear_joint_value_targets()
        group.clear_pose_targets()

        # END_SUB_TUTORIAL

        # For testing: Note that since this section of code will not be included
        # in the tutorials we use the class variable rather than the copied
        # state variable
        current_pose = self.group.get_current_pose().pose
        return all_close(pose_goal, current_pose, 0.01)

    def execute_plan(self, plan):
        # Copy class variables to local variables to make the web tutorials more
        # clear. In practice, you should use the class variables directly unless
        # you have a good reason not to.
        group = self.group

        # BEGIN_SUB_TUTORIAL execute_plan
        ##
        # Executing a Plan
        # ^^^^^^^^^^^^^^^^
        # Use execute if you would like the robot to follow the plan that has
        # already been computed:
        group.execute(plan, wait=True)

        # **Note:** The robot's current joint state must be within some
        # tolerance of the first waypoint in the `RobotTrajectory`_ or
        # ``execute()`` will fail END_SUB_TUTORIAL

    def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
        # Copy class variables to local variables to make the web tutorials more
        # clear. In practice, you should use the class variables directly unless
        # you have a good reason not to.
        box_name = self.box_name
        scene = self.scene

        # BEGIN_SUB_TUTORIAL wait_for_scene_update
        ##
        # Ensuring Collision Updates Are Receieved
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If the Python node dies before publishing a collision object update
        # message, the message could get lost and the box will not appear. To
        # ensure that the updates are made, we wait until we see the changes
        # reflected in the ``get_known_object_names()`` and
        # ``get_known_object_names()`` lists. For the purpose of this tutorial,
        # we call this function after adding, removing, attaching or detaching
        # an object in the planning scene. We then wait until the updates have
        # been made or ``timeout`` seconds have passed
        start = rospy.get_time()
        seconds = rospy.get_time()
        while (seconds - start < timeout) and not rospy.is_shutdown():
            # Test if the box is in attached objects
            attached_objects = scene.get_attached_objects([box_name])
            is_attached = len(attached_objects.keys()) > 0

            # Test if the box is in the scene. Note that attaching the box will
            # remove it from known_objects
            is_known = box_name in scene.get_known_object_names()

            # Test if we are in the expected state
            if (box_is_attached == is_attached) and (box_is_known == is_known):
                return True

            # Sleep so that we give other threads time on the processor
            rospy.sleep(0.1)
            seconds = rospy.get_time()

        # If we exited the while loop without returning then we timed out
        return False
        # END_SUB_TUTORIAL


def main():
    try:
        moveit_commander.roscpp_initialize(sys.argv)
        move_group = moveit_commander.MoveGroupCommander("panda_arm")
        move_group.go(STARTING_POS, wait=True)
        group.stop()
    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
