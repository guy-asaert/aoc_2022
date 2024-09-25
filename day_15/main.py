from utils import iter_lines
import re
from collections import namedtuple, defaultdict

SensorData = namedtuple('SensorData', 's_x s_y, b_x, b_y, md')
pattern = 'x=-?\d+, y=-?\d+'


class CaveBase:

    def __init__(self, sensor_data):
        self.sensor_data = sensor_data


class Cave(CaveBase):
    def __init__(self, sensors):
        super().__init__(sensors)
        self.layout = defaultdict(dict)
        # self._sensors = sensors

        self._process()

    def _process(self):
        # set beacons and sensors
        for sensor in self.sensor_data:
            self.layout[sensor.s_y][sensor.s_x] = 'S'
            self.layout[sensor.b_y][sensor.b_x] = 'B'

        # set the location where there cannot be a beacon
        for sensor in self.sensor_data:
            for manhattan_distance in range(1, sensor.md+1):
                for x_dist in range(0, manhattan_distance+1):
                    y_dist = manhattan_distance - x_dist
                    self.setat(sensor.s_y + y_dist, sensor.s_x + x_dist, '#')
                    self.setat(sensor.s_y + y_dist, sensor.s_x - x_dist, '#')
                    self.setat(sensor.s_y - y_dist, sensor.s_x + x_dist, '#')
                    self.setat(sensor.s_y - y_dist, sensor.s_x - x_dist, '#')

    def setat(self, y, x, what):
        """ only set the what if nothing is set at x,y """
        if y not in self.layout or x not in self.layout[y]:
            self.layout[y][x] = what

    def answer(self, row):
        return list(self.layout[row].values()).count('#')


class CaveEfficient(CaveBase):

    def __int__(self, sensor_data):
        super().__init__(sensor_data)

    def answer(self, row):
        # row_details = []
        beacon_cannot_be_present = 0
        for column in range(self.min_col, self.max_col):
            rc = self.get(row, column)
            if rc == '#':
                beacon_cannot_be_present += 1

        return beacon_cannot_be_present

    @property
    def min_col(self):
        min_beacon = [m.s_x - m.md for m in self.sensor_data]
        return min(min_beacon)

    @property
    def max_col(self):
        max_beacon = [m.s_x + m.md for m in self.sensor_data]
        return max(max_beacon)

    def get(self, row, col):
        """Position row, col can be either a sensor (S), a beacon (B), not a beacon (#) or undefined (.)"""
        for sensor_details in self.sensor_data:
            if (sensor_details.s_x, sensor_details.s_y) == (col, row):
                return 'S'
            elif (sensor_details.b_x, sensor_details.b_y) == (col, row):
                return 'B'
            elif abs(sensor_details.s_x - col) + abs(sensor_details.s_y - row) <= sensor_details.md:
                return '#'

        return '.'


def solve():
    # inputs = ['_sample.txt', 10]
    inputs = ['_puzzle.txt', 20000]

    sensor_data = []
    for line in iter_lines(__file__, inputs[0]):
        matches = re.findall(pattern, line)
        sensor_coords = re.findall('-?\d+', matches[0])
        beacon_coords = re.findall('-?\d+', matches[1])
        sensor_data.append(
            SensorData(
                int(sensor_coords[0]),
                int(sensor_coords[1]),
                int(beacon_coords[0]),
                int(beacon_coords[1]),
                abs(int(beacon_coords[0]) - int(sensor_coords[0])) + abs(int(beacon_coords[1]) - int(sensor_coords[1]))
            ))

    cave = CaveEfficient(sensor_data)
    print(cave.answer(inputs[1]))


if __name__ == '__main__':
    solve()
