package main

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	os.Exit(m.Run())
}

func TestParseBoardingPass(t *testing.T) {
	var tests = []struct {
		pass         string
		row, col, id int
	}{
		{"FBFBBFFRLR", 44, 5, 357},
		{"BFFFBBFRRR", 70, 7, 567},
		{"FFFBBBFRRR", 14, 7, 119},
		{"BBFFBBFRLL", 102, 4, 820},
	}

	for _, tt := range tests {
		parsedPass := parseBoardingPass(tt.pass)
		assert.Equal(t, tt.row, parsedPass.Row, "%s.row fail", tt.pass)
		assert.Equal(t, tt.col, parsedPass.Col, "%s.col fail", tt.pass)
		assert.Equal(t, tt.id, parsedPass.ID, "%s.id fail", tt.pass)
	}
}
