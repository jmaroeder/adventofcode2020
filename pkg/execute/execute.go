// https://github.com/kindermoumoute/adventofcode/blob/master/pkg/execute/execute.go

package execute

import (
	"fmt"
	"time"
)

func Run(run func(string) (interface{}, interface{}), tests TestCases, puzzle string, verbose bool) {
	if tests != nil {
		tests.Run(run, !verbose)
	}

	start := time.Now()
	part1, part2 := run(puzzle)
	elapsed := time.Since(start)

	fmt.Printf("PART1: %v\nPART2: %v\n", part1, part2)
	fmt.Printf("Program took %s", elapsed)
}
