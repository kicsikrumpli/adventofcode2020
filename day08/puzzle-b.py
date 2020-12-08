from typing import Tuple, List

from day08.puzzle import Op, parse_line


def step(instruction: Tuple[Op, int],
         pc: int = 0,
         acc: int = 0) -> Tuple[int, int]:
    """
    >>> step(instruction=(Op.ACC, 2))
    (1, 2)

    >>> step(instruction=(Op.JMP, -1), pc=1, acc=0)
    (0, 0)


    :return: new pc, new acc
    """
    op, arg = instruction
    if op is Op.ACC:
        _acc = acc + arg
        _pc = pc + 1
    elif op is Op.JMP:
        _acc = acc
        _pc = pc + arg
    elif op is Op.NOP:
        _acc = acc
        _pc = pc + 1
    else:
        raise Exception("unknown instruction")

    return _pc, _acc


def backtrack(program: List[Tuple[Op, int]],
              pc: List[int] = None,
              acc: int = 0,
              has_fix: bool = False):
    """
    Find final accumulator value of corrected program.
    - fix at most one instruction,
    - find correct program with backtracking

    :param program: list of operator, operand tuples
    :param pc: list of program counters for each execution step
    :param acc: accumulator value
    :param has_fix: flag if fixing an instruction is allowed
        should switch only one instruction in program
    :return: accumulator value of corrected program
    """
    def switch(_instr: Tuple[Op, int]) -> Tuple[Op, int]:
        """
        switch jmp to nop, nop to jmp.
        """
        o, a = _instr
        if o is Op.JMP:
            return Op.NOP, a
        elif o is Op.NOP:
            return Op.JMP, a
        else:
            return o, a

    if pc is None:
        pc = [0]

    if pc[-1] == len(program):
        # reached instruction after last one, done
        return acc

    if pc[-1] in pc[:-1]:
        # we have visited this line before, needs fix
        return None

    _pc = pc[-1]
    _instruction = program[_pc]
    _op, _ = _instruction

    next_pc, next_acc = step(_instruction, _pc, acc)
    if _op is not Op.NOP and not has_fix:
        alt_instruction = switch(_instruction)
        alt_pc, alt_acc = step(alt_instruction, _pc, acc)
        return backtrack(program=program, pc=[*pc, alt_pc], acc=alt_acc, has_fix=True) or \
               backtrack(program=program, pc=[*pc, next_pc], acc=next_acc, has_fix=False)
    else:
        return backtrack(program=program, pc=[*pc, next_pc], acc=next_acc, has_fix=has_fix)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        program = [parse_line(line) for line in puzzle]

    accumulator = backtrack(program)
    print('Accumulator value after program finished: ', accumulator)
