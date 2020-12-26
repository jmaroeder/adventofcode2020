import contextlib
import enum
import logging
import re
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import List
from typing import Set

LOG = logging.getLogger(__name__)


class Operation(str, enum.Enum):
    acc = "acc"
    jmp = "jmp"
    nop = "nop"


@dataclass(frozen=True)
class Instruction:
    operation: Operation
    argument: int

    instruction_re: ClassVar[re.Pattern] = re.compile(r"(?P<operation>acc|jmp|nop) (?P<argument>[+-]\d+)")

    @classmethod
    def parse(cls, line: str) -> "Instruction":
        match = cls.instruction_re.match(line)
        if match is None:
            raise Exception(f"Unable to parse line: {line}")
        return cls(Operation(match.group("operation")), int(match.group("argument")))


class VMException(Exception):
    def __init__(self, vm: "HandheldVM") -> None:
        self.vm = vm


class InfiniteLoop(VMException):
    pass


@dataclass
class HandheldVM:
    code: List[Instruction]

    acc: int = 0
    iptr: int = 0
    ticked_iptrs: Set[int] = field(default_factory=set)

    @classmethod
    def from_code(cls, code: str) -> "HandheldVM":
        return cls([Instruction.parse(line) for line in code.splitlines()])

    @property
    def instruction(self) -> Instruction:
        return self.code[self.iptr]

    def __repr__(self) -> str:
        return f"HandheldVM<iptr={self.iptr}, acc={self.acc}>"

    @property
    def completed(self) -> bool:
        return self.iptr == len(self.code)

    def tick(self) -> None:
        if self.completed:
            return

        if self.iptr in self.ticked_iptrs:
            LOG.info(f"Infinite loop detected ({self})")
            raise InfiniteLoop(self)

        self.ticked_iptrs.add(self.iptr)
        LOG.debug(f"Executing instruction {self.iptr}: {self.instruction}")

        if self.instruction.operation == Operation.acc:
            self.acc += self.instruction.argument
            self.iptr += 1
            return

        if self.instruction.operation == Operation.nop:
            self.iptr += 1
            return

        if self.instruction.operation == Operation.jmp:
            self.iptr += self.instruction.argument
            return

    def run_until_infinite_loop(self) -> None:
        with contextlib.suppress(InfiniteLoop):
            self.run_until_completion()

    def run_until_completion(self) -> None:
        while not self.completed:
            self.tick()
