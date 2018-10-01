package main

import (
	"fmt"
	"runtime"
)

// const sleepTime  = 100 * time.Millisecond

var ch = make(chan int)

func t1() {
	for i := 0; i < 100; i++ {
		fmt.Print(i)
		// time.Sleep(sleepTime)
	}
	fmt.Println("")
	ch <- 0
}

func main() {
	runtime.GOMAXPROCS(1)

	go t1()
	go t1()
	<-ch
	<-ch
}

