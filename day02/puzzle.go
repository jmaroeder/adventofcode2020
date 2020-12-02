package main

import (
	"github.com/jmaroeder/adventofcode2020/pkg/execute"
)

var tests = execute.TestCases{
	{
		Input: `1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc`,
		ExpectedPart1: 2,
		ExpectedPart2: ``,
	},
}
