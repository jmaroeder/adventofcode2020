import contextlib
import textwrap
from pathlib import Path
from typing import Any
from typing import Tuple

import advent
from day08.handheld_vm import HandheldVM
from day08.handheld_vm import Operation

CORRUPTABLE_OPS = {Operation.nop, Operation.jmp}


def main(s: str) -> Tuple[Any, Any]:
    part2 = None

    vm = HandheldVM.from_code(s)
    vm.run_until_infinite_loop()
    part1 = vm.acc

    base_code = vm.code

    for idx, instruction in enumerate(base_code):
        if instruction.operation == Operation.acc:
            continue
        variant = base_code.copy()
        if instruction.operation == Operation.nop:
            # TODO
            pass
        # TODO: run vm, check for infinite loop

    return part1, part2





SAMPLE_INPUT = textwrap.dedent(
    r"""
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
    """
).strip()


if __name__ == "__main__":
    advent.setup()
    advent.test(
        main,
        advent.TestCase(
            input=SAMPLE_INPUT,
            expected_part_1=5,
            expected_part_2=8,
        ),
    )

    advent.execute(
        main,
        Path(__file__).parent.absolute() / "input.txt",
    )
