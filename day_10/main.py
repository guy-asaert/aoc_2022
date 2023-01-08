from utils import read_lines

NOOP_COMMAND = 'noop'
ADDC_COMMAND_NOOP = 'addx1'
ADDX_COMMAND = 'addx2'


class Program:

    def __init__(self, instructions):
        self._instructions = instructions

    def __iter__(self):
        for instruction in self._instructions:
            if instruction == 'noop':
                yield NOOP_COMMAND, None
            else:
                yield ADDC_COMMAND_NOOP, None
                yield ADDX_COMMAND, int(instruction.split(' ')[1])


class CPU:
    def __init__(self, instructions):
        self._clock_cycle = 0
        self._register = 1
        self._program = Program(instructions)
        self._signal_strength = 0

    def run_program(self):

        screen = [40 * ['.'] for i in range(6)]
        for instr, param in self._program:
            # print(instr)
            self._clock_cycle += 1

            row = self._clock_cycle // 40
            column = (self._clock_cycle - 1) % 40
            if self._register - 1 <= column <= self._register + 1:
                screen[row][column] = '#'

            print(f'{self._clock_cycle: >3} {instr: <5} {str(param): >4} {self._register: >3}')
            if (self._clock_cycle + 20) % 40 == 0:
                self._signal_strength += (self._clock_cycle * self._register)

            if instr == ADDX_COMMAND:
                self._register += param

        for row in screen:
            print(''.join(row))

    @property
    def signal_strength(self):
        return self._signal_strength


def part1():
    cpu = CPU(read_lines(__file__, False))
    cpu.run_program()
    print(cpu.signal_strength)


if __name__ == '__main__':
    part1()
