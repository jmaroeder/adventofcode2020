package main

import (
	"github.com/jmaroeder/adventofcode2020/pkg/execute"
)

var tests = execute.TestCases{
	{
		Input: `abc

a
b
c

ab
ac

a
a
a
a

b
`,
		ExpectedPart1: 11,
		ExpectedPart2: 6,
	},
}
