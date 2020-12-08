from typing import Tuple, List

from day08.puzzle import Op, parse_line


def step(instruction: Tuple[Op, int],
         pc: List[int] = None,
         acc: List[int] = None) -> Tuple[List[int], List[int]]:
    """
    >>> step(instruction=(Op.ACC, 2))
    ([0, 1], [0, 2])

    >>> step(instruction=(Op.JMP, -1), pc=[1], acc=[0])
    ([1, 0], [0, 0])


    :return: new pc, new acc
    """
    if not pc:
        _pc = [0]
    else:
        _pc = list(pc)
    if not acc:
        _acc = [0]
    else:
        _acc = list(acc)

    op, arg = instruction
    if op is Op.ACC:
        _acc.append(_acc[-1] + arg)
        _pc.append(_pc[-1] + 1)
    if op is Op.JMP:
        _acc.append(_acc[-1])
        _pc.append(_pc[-1] + arg)
    if op is Op.NOP:
        _acc.append(_acc[-1])
        _pc.append(_pc[-1] + 1)

    return _pc, _acc


def backtrack(program: List[Tuple[Op, int]],
              pc: List[int] = None,
              acc: List[int] = None,
              has_fix: bool = False):
    """
    Find final accumulator value of corrected program.
    - fix at most one instruction,
    - find correct program with backtracking

    NB! it is absolutely pointless to keep history of pc and acc
    - pc could be a set
    - acc could be a single number

    :param program: list of operator, operand tuples
    :param pc: list of program counters for each execution step
    :param acc: list of accumulator values for each execution step
    :param has_fix: flag if fixing an instruction is allowed
        should switch only one instruction in program
    :return: last accumulator value of corrected program
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

    if pc and pc[-1] == len(program):
        # reached instruction after last one, done
        return acc[-1]

    if pc and pc[-1] in pc[:-1]:
        # we have visited this line before, needs fix
        return None

    if pc is None and acc is None:
        pc = [0]
        acc = [0]

    _pc = pc[-1]
    _instruction = program[_pc]
    _op, _arg = _instruction

    next_pc, next_acc = step(_instruction, pc, acc)
    if _op is not Op.NOP and not has_fix:
        alt_instruction = switch(_instruction)
        alt_pc, alt_acc = step(alt_instruction, pc, acc)
        return backtrack(program=program, pc=alt_pc, acc=alt_acc, has_fix=True) or \
               backtrack(program=program, pc=next_pc, acc=next_acc, has_fix=False)
    else:
        return backtrack(program=program, pc=next_pc, acc=next_acc, has_fix=has_fix)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('input.txt', 'rt') as puzzle:
        program = [parse_line(line) for line in puzzle]

    accumulator = backtrack(program)
    print('Accumulator value after program finished: ', accumulator)
