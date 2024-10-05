from utils import iter_lines
from collections import namedtuple
# from functools import lru_cache
import itertools

ValveDetails = namedtuple("ValveDetails", "ValveFlow ConnectingValves")


valve_distances = dict()

def get_distances(node_name, puzzle_details, distances, distance):
    for valve in puzzle_details[node_name].ConnectingValves:
        if not valve in distances or distance < distances[valve]:
            distances[valve] = distance
            get_distances(valve, puzzle_details, distances, distance + 1)

def _position_value(valves_left, valve_distances, minutes_left, puzzle_details):
    
    pos_value = 0
    for valve in valves_left:
        if valve_distances[valve] < minutes_left - 1:
            pos_value += (minutes_left - valve_distances[valve] - 1) * puzzle_details[valve].ValveFlow

    return pos_value

def find_highest_flow(current_valve, valves_to_visit, puzzle_details, minutes_left, depth):
    global valve_distances

    # if depth == 1:
    #     print(f"{current_valve}")

    # calculate the remaining total flow
    # total_flow_left = sum([det.ValveFlow for k, det in puzzle_details.items() if k not in visited_valves])
    l_valves_to_visit = valves_to_visit.difference([current_valve])
    distances = dict()

    if not valves_to_visit or minutes_left <= 1:
        return 0
    
    # determine the distances to all the valves
    if current_valve in valve_distances:
        distances = valve_distances[current_valve]
    else:
        get_distances(current_valve, puzzle_details, distances, 1)
        valve_distances[current_valve] = distances

    highest_flow = 0

    for valve in l_valves_to_visit:
        distance = distances[valve]
        l_minutes_left = minutes_left - (distance + 1)
        if l_minutes_left <= 0 or puzzle_details[valve].ValveFlow == 0:
            continue

        flow = l_minutes_left * puzzle_details[valve].ValveFlow
        flow += find_highest_flow( 
            valve, l_valves_to_visit, puzzle_details, l_minutes_left, depth + 1 )
        if flow > highest_flow:
            highest_flow = flow

    return highest_flow


def find_highest_flow_part2(
        current_valve1, current_valve2,
        minutes_left1, minutes_left2,
        valves_to_visit, puzzle_details, depth):
    global valve_distances

    if depth == 1:
        print(f"{current_valve1}/{current_valve2}")

    l_valves_to_visit = valves_to_visit.difference([current_valve1, current_valve2])

    if not valves_to_visit or (minutes_left1 <= 1 and minutes_left2 <= 1):
        return 0
    
    # determine the distances to all the valves
    for current_valve in (current_valve1, current_valve2):
        if not current_valve in valve_distances:
            distances = dict()
            get_distances(current_valve, puzzle_details, distances, 1)
            valve_distances[current_valve] = distances

    highest_flow = 0

    for valve1, valve2  in itertools.permutations(sorted(l_valves_to_visit), 2):
        distance1 = valve_distances[current_valve1][valve1]
        l_minutes_left1 = minutes_left1 - (distance1 + 1)
        distance2 = valve_distances[current_valve2][valve2]
        l_minutes_left2 = minutes_left2 - (distance2 + 1)

        if puzzle_details[valve1].ValveFlow == 0 or l_minutes_left1 < 1 or \
            puzzle_details[valve2].ValveFlow == 0 or l_minutes_left2 < 1:
            continue

        flow = 0
        flow += l_minutes_left1 * puzzle_details[valve1].ValveFlow
        flow += l_minutes_left2 * puzzle_details[valve2].ValveFlow
        flow += find_highest_flow_part2( 
            valve1, valve2, l_minutes_left1, l_minutes_left2, l_valves_to_visit, puzzle_details, depth + 1 )
        if flow > highest_flow:
            highest_flow = flow

    return highest_flow

def solve():
    puzzle_details = dict()
    for line in iter_lines(__file__, '_puzzle.txt'):
        part1, part2 = line.split(';')
        valve_name = part1[6:8]
        valve_flow = int(part1.split('=')[1])
        valve_list = part2.split('valves')
        if len(valve_list) > 1:
            lead_to_valves = valve_list[1]
        else:
            lead_to_valves = part2.split('valve')[1]
        
        list_of_valves = [v.strip() for v in lead_to_valves.split(',') if v.strip()]
        puzzle_details[valve_name] = ValveDetails(valve_flow, list_of_valves)
    
    first_valve = 'AA'

    visit_valves = set([k for k, v in puzzle_details.items() if v.ValveFlow > 0])
    # highest_flow = find_highest_flow(first_valve, visit_valves, puzzle_details, 30, 0)
    highest_flow = find_highest_flow_part2(first_valve, first_valve, 26, 26, visit_valves, puzzle_details,  0)
    print(highest_flow)



if __name__ == '__main__':
    solve()
