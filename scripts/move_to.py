import sys
import moveit_commander
import numpy as np
import rospy


STARTING_POS = np.array([
    1.5144076375347826,
    -0.6726638697722728,
    0.18543326279796127,
    -2.9585892121572526,
    0.12056011035042515,
    2.3006689352724274,
    0.7933720851335472
])

GOALS = {
    "blue1": np.array([0.1409447106, 0.1639815799, 0.06989041156, -2.712633573, 0.1428424252, 2.860975177, -0.8557920371]),
    "blue2": np.array([0.498051003, 0.1843897182, -0.2707988077, -2.704178653, 0.03824007027, 2.852824763, -0.6874390045]),
    "blue3": np.array([0.5892901589, 0.4606513663, 0.02096505987, -2.409281471, -1.05241235, 1.91614986, 0.5328634008]),
    "blue4": np.array([0.01677850176, 0.3454656497, -0.09475766412, -2.533252329, 1.257536801, 2.179532234, 1.076728215]),
    "blue5": np.array([0.5111703293, 0.1869657054, -0.2621775617, -2.709319314, 0.27661888, 2.87005221, -0.900165307]),
    "green1": np.array([0.04828069357, 0.321198491, -0.09149035608, -2.445509451, 0.0339262541, 2.766537249, -0.7381757918]),
    "green2": np.array([1.816872462, -0.8203449981, -2.173989994, -2.33774102, 0.2990857285, 2.543709462, 1.755722001]),
    "red1": np.array([0.4973887075, 0.3626231152, -0.1262784644, -2.353311054, 0.1667072496, 2.697354126, -0.9114452175])
}

STARTING_POS_HAND = np.array([
    0.0,
    0.0
])

if __name__ == '__main__':
    pos = sys.argv[1]
    if pos in GOALS:
        pos = GOALS[pos]
    else:
        pos = np.fromstring(sys.argv[1], sep=', ')
        print(pos)
    if pos.size != 7:
        print("Pose doesn't specify all 7 DoFs")
        exit(1)
    moveit_commander.roscpp_initialize([sys.argv[0]])
    rospy.init_node("move_node", anonymous=True)
    panda_arm = moveit_commander.MoveGroupCommander("panda_arm")
    panda_arm.go(pos, wait=True)
    panda_arm.stop()

    pose = panda_arm.get_current_pose().pose
    print("Current Pose: ", pose.x, pose.y, pose.z)


    # panda_hand = moveit_commander.MoveGroupCommander("panda_hand")
    # panda_hand.go(STARTING_POS_HAND, wait=True)
    # panda_hand.stop()
