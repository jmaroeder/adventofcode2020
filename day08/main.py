import contextlib
import textwrap
from dataclasses import replace
from pathlib import Path
from typing import Any
from typing import Tuple

import advent
from day08.handheld_vm import HandheldVM
from day08.handheld_vm import Operation

SWAP_OPS = {
    Operation.nop: Operation.jmp,
    Operation.jmp: Operation.nop,
}


def main(s: str) -> Tuple[Any, Any]:
    part2 = None

    vm = HandheldVM.from_code(s)
    vm.run_until_infinite_loop()
    part1 = vm.acc

    for idx, instruction in enumerate(vm.code):
        if instruction.operation == Operation.acc:
            continue
        variant_code = vm.code.copy()
        variant_code[idx] = replace(instruction, operation=SWAP_OPS[instruction.operation])
        variant_vm = HandheldVM(code=variant_code)
        variant_vm.run_until_infinite_loop()
        if variant_vm.completed:
            part2 = variant_vm.acc
            break

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
