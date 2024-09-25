from utils import iter_lines
from collections import namedtuple
from functools import lru_cache

ValveDetails = namedtuple("ValveDetails", "ValveFlow ConnectingValves")


valve_distances = dict()

def get_distances(node_name, puzzle_details, distances, distance):
    for valve in puzzle_details[node_name].ConnectingValves:
        if not valve in distances or distance < distances[valve]:
            distances[valve] = distance
            get_distances(valve, puzzle_details, distances, distance + 1)


def calc_highest_flow(current_valve, visited_valves, puzzle_details, minutes_left, depth):

    if len(visited_valves) == len(puzzle_details):
        return 0
    # if depth > 3:
    #     return 0
    
    highest_flow = 0
    distances = dict()

    global valve_distances
    if current_valve in valve_distances:
        distances = valve_distances[current_valve]
    else:
        get_distances(current_valve, puzzle_details, distances, 1)
        valve_distances[current_valve] = distances

    for valve, distance in distances.items():
        l_minutes_left = minutes_left - (distance + 1)
        if l_minutes_left <= 0:
            continue

        flow = l_minutes_left * puzzle_details[valve].ValveFlow
        if not valve in visited_valves:
            flow += calc_highest_flow( 
                valve, visited_valves + [valve], puzzle_details, l_minutes_left, depth + 1 )
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
    
    current_location = 'AA'
    visited_valves = [current_location]
    highest_flow = calc_highest_flow(current_location, visited_valves, puzzle_details, 30, 0)
    print(highest_flow)



if __name__ == '__main__':
    solve()
