package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	countsMap := make(map[string]int)
	inputScan := bufio.NewScanner(os.Stdin)
	for inputScan.Scan() {
		countsMap[inputScan.Text()]++
	}

	for key, value := range countsMap {
		if value > 1 {
			fmt.Printf("%d\t%s\n",value, key)
		}
	}
}

// for inputScan.Scan(): read a line

