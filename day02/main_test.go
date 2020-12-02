package main

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	os.Exit(m.Run())
}

type CheckPassTestCase struct {
	Min            int
	Max            int
	Letter         string
	Password       string
	ExpectedResult bool
}

func TestCheckPass1(t *testing.T) {
	testCases := []CheckPassTestCase{
		{1, 3, "a", "abcde", true},
		{1, 3, "b", "cdefg", false},
		{2, 9, "c", "ccccccccc", true},
	}
	for _, tt := range testCases {
		assert.Equal(t, tt.ExpectedResult, checkPass1(tt.Min, tt.Max, tt.Letter, tt.Password), "%s fail", tt)
	}
}

func TestCheckPass2(t *testing.T) {
	testCases := []CheckPassTestCase{
		{1, 3, "a", "abcde", true},
		{1, 3, "b", "cdefg", false},
		{2, 9, "c", "ccccccccc", false},
	}
	for _, tt := range testCases {
		assert.Equal(t, tt.ExpectedResult, checkPass2(tt.Min, tt.Max, tt.Letter, tt.Password), "%s fail", tt)
	}
}
