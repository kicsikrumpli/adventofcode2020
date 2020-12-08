from enum import Enum
from typing import Tuple, List


class Op(Enum):
    ACC = 'acc'
    JMP = 'jmp'
    NOP = 'nop'


class Cpu:
    def __init__(self,
                 program: List[Tuple[Op, int]],
                 acc_init: int = 0
                 ):
        self.accumulator = acc_init
        self.program = program
        self.pc = 0

    def step(self, pc) -> int:
        """
        execute op at pc.
        :param pc: program counter, pointer into self.program
        :return: next pc
        """
        op, arg = self.program[pc]
        if op is Op.ACC:
            self.accumulator += arg
        if op is Op.JMP:
            return self.pc + arg
        if op is Op.NOP:
            pass

        pc += 1
        return pc

    def run_detect_loop(self):
        """
        run program until pc is visited twice.

        :return: accumulator value before duplicate execution
        """
        history = set()
        acc = 0
        while self.pc not in history:
            acc = self.accumulator
            history.add(self.pc)
            self.pc = self.step(self.pc)

        return acc


def parse_line(line: str) -> Tuple[Op, int]:
    """
    >>> parse_line("nop 42")
    (<Op.NOP: 'nop'>, 42)

    :param line:
    :return:
    """
    op, arg = line.split()
    return Op[op.upper()], int(arg)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        program = [parse_line(line) for line in puzzle]

    cpu = Cpu(program)
    acc = cpu.run_detect_loop()
    print('accumulator before 2nd execution of same line: ', acc)
