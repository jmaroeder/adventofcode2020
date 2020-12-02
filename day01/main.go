package main

import (
	"github.com/jmaroeder/adventofcode2020/pkg"
	"github.com/jmaroeder/adventofcode2020/pkg/execute"
)

// returns part1 and part2
func run(input string) (interface{}, interface{}) {
	part1, part2 := 0, 0

	expenseValues := pkg.ParseIntList(input, ",")

	for i := 0; i < len(expenseValues); i++ {
		for j := i; j < len(expenseValues); j++ {
			if expenseValues[i]+expenseValues[j] == 2020 {
				part1 = expenseValues[i] * expenseValues[j]

			}
			for k := j; k < len(expenseValues); k++ {
				if expenseValues[i]+expenseValues[j]+expenseValues[k] == 2020 {
					part2 = expenseValues[i] * expenseValues[j] * expenseValues[k]
				}
			}
			if part1 != 0 && part2 != 0 {
				break
			}
		}
		if part1 != 0 && part2 != 0 {
			break
		}
	}

	return part1, part2
}

func main() {
	execute.Run(run, tests, puzzle, true)
}
