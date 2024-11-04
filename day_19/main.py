import time
import cProfile
import pstats
from collections import defaultdict
import copy
from enum import Enum       
import io
from utils import iter_lines


PUZZLE_INPUT_SAMPLE = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''

class EnumResources(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4
    UNDEFINED = 5

class EnumRobot(Enum):
    ORE_ROBOT = 1
    CLAY_ROBOT = 2
    OBSIDIAN_ROBOT = 3
    GEODE_ROBOT = 4

class EnumRobotBuildResult(Enum):
    SUCCESS = 1     # robot was built successfully 
    TOO_MANY_RESOURCES = 2  # we can build more than one of the robot type
    NOT_ENOUGH_RESOURCES = 3  # we have some but not all the resources to build the robot
    NO_RESOURCES = 4    # we don't have any resources to build the robot

ROBOT_RESOURCE_MAP = {
    EnumRobot.ORE_ROBOT: EnumResources.ORE,
    EnumRobot.CLAY_ROBOT: EnumResources.CLAY,
    EnumRobot.OBSIDIAN_ROBOT: EnumResources.OBSIDIAN,
    EnumRobot.GEODE_ROBOT: EnumResources.GEODE
}

RESOURCE_ROBOT_MAP = {
    EnumResources.ORE: EnumRobot.ORE_ROBOT,
    EnumResources.CLAY: EnumRobot.CLAY_ROBOT,
    EnumResources.OBSIDIAN: EnumRobot.OBSIDIAN_ROBOT,
    EnumResources.GEODE: EnumRobot.GEODE_ROBOT
}


MAX_MINUTES = 32

def try_make_robot(robot_type: EnumRobot,
                   resources: dict[EnumResources, int],
                   robots: dict[EnumRobot, int],
                   robot_costs: dict[EnumResources, int]) -> EnumRobotBuildResult:
    """
    Attempts to build a robot of the specified type.
    Returns EnumRobotBuildResult.SUCCESS if the robot was built successfully.
    """
    robot_resource = [resources.get(resource, 0) for resource, _ in robot_costs[robot_type].items()]

    # check if we have any resources to build the robot
    if sum(robot_resource) == 0:
        return EnumRobotBuildResult.NO_RESOURCES
    
    robot_resource_count = [resources.get(resource, 0)//int(cost) for resource, cost in robot_costs[robot_type].items()]

    # check if we have all the resources but not enough
    if min(robot_resource_count) == 0:
        return EnumRobotBuildResult.NOT_ENOUGH_RESOURCES
    elif min(robot_resource_count) >= 2:
        return EnumRobotBuildResult.TOO_MANY_RESOURCES

    return EnumRobotBuildResult.SUCCESS


def run_simulation(robot_type, time_passed, resources, robots, robot_costs, memo, max_resources):

    state = (robot_type, time_passed, tuple(resources.items()), tuple(robots.items()))
    if state in memo:
        return memo[state]

    # make robot
    result = try_make_robot(robot_type, resources, robots, robot_costs)

    memo[state] = result
    # if we can made more than 1 robot at a time, we can ignore this state
    if result == EnumRobotBuildResult.TOO_MANY_RESOURCES:
        return result
    
    # make resources with the robots we have
    for building_robot_type, count in robots.items():
        resources[ROBOT_RESOURCE_MAP[building_robot_type]] += count

    time_passed += 1

    if result != EnumRobotBuildResult.SUCCESS:
        # if we have the robots that can build the resources we need, we can wait for the resources to be built and try again
        if time_passed == MAX_MINUTES:
            for resource, count in resources.items():
                max_resources[resource] = max(max_resources.get(resource, 0), count)
            return result
        
        for resource, _ in robot_costs[robot_type].items():
            if not robots.get(RESOURCE_ROBOT_MAP[resource], 0):
                return result
        # try again after adding more resources
        return run_simulation(robot_type, time_passed, copy.copy(resources), copy.copy(robots), robot_costs, memo, max_resources)

    robots[robot_type] += 1
    for resource, cost in robot_costs[robot_type].items():
        resources[resource] -= int(cost)

    if time_passed == MAX_MINUTES:
        for resource, count in resources.items():
            max_resources[resource] = max(max_resources.get(resource, 0), count)
        return result
    
    for robot_type in [EnumRobot.ORE_ROBOT, EnumRobot.CLAY_ROBOT, EnumRobot.OBSIDIAN_ROBOT, EnumRobot.GEODE_ROBOT]:
        run_simulation(robot_type, time_passed, copy.copy(resources), copy.copy(robots), robot_costs, 
                        memo, max_resources)

    return result


def run():
    total_quality = 0

    for blueprint in PUZZLE_INPUT_SAMPLE.split('\n'):
    # for blueprint in list(iter_lines(__file__, '_puzzle.txt'))[:3]:
        bp_id, code = blueprint.split(': ')
        bp_no = int(bp_id[10:])
        robot_cost_codes = code.split('.')
        robot_costs = defaultdict(dict)
        for robot_cost_code in robot_cost_codes:
            robot_cost_words = robot_cost_code.strip().split(' ')
            for cost_index in range(4, len(robot_cost_words), 3):
                resource_name = robot_cost_words[cost_index + 1].upper()
                resource = EnumResources[resource_name.upper()]
                robot_name = robot_cost_words[1].upper()
                robot = EnumRobot[robot_name.upper() + "_ROBOT"]
                robot_costs[robot][resource] = robot_cost_words[cost_index]

        # we need to simlate al the ways the robots can be built and see how we can build the most 
        # number of geodes

        memo = {}
        max_resources = dict()
        robots = defaultdict(lambda: 0)
        robots[EnumRobot.ORE_ROBOT] = 1
        resources = defaultdict(lambda: 0)
        time_passed = 0
        run_simulation(EnumRobot.ORE_ROBOT, time_passed, resources, robots, robot_costs, memo, max_resources)

        # robots = defaultdict(lambda: 0)
        # robots[EnumRobot.ORE_ROBOT] = 1
        # resources = defaultdict(lambda: 0)
        # time_passed = 0
        # run_simulation(EnumRobot.CLAY_ROBOT, time_passed, resources, robots, robot_costs, memo, max_resources)

        print(f'Completed simulation {bp_id}. Max Geodes: {max_resources.get(EnumResources.GEODE, 0)}')
        total_quality += max_resources.get(EnumResources.GEODE, 0) * bp_no

    print(f'Total quality = {total_quality}')

if __name__ == '__main__':
    # pr = cProfile.Profile()
    # pr.enable()
    run()
    # pr.disable()
    # s = io.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())


# Completed simulation Blueprint 1. Max Geodes: 32
# Completed simulation Blueprint 2. Max Geodes: 21
# Completed simulation Blueprint 3. Max Geodes: 28
# Total quality = 158  -- 18,816