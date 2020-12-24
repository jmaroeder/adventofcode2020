package main

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	os.Exit(m.Run())
}

func TestCanContain(t *testing.T) {
	testCases := []struct {
		rules string
		cases []struct {
			outer, inner string
		}
	}{
		{
			`light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.`,
			[]struct {
				outer, inner string
			}{
				{"bright white", "shiny gold"},
				{"muted yellow", "shiny gold"},
				{"dark orange", "bright white"},
				{"dark orange", "muted yellow"},
				{"dark orange", "shiny gold"},
				{"light red", "bright white"},
				{"light red", "muted yellow"},
				{"light red", "shiny gold"},
			},
		},
	}

	for _, tt := range testCases {
		bagTree := parseRules(tt.rules)
		for _, ttt := range tt.cases {
			assert.Equal(t, true, canContain(bagTree, ttt.outer, ttt.inner), "%s:%s fail", ttt.outer, ttt.inner)
		}
	}
}
