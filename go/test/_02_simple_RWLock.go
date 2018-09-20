package main

import (
	"fmt"
	"sync/atomic"
)

type SimpleRWLock struct {
	readLock  int32
	writeLock int32
}

func (lock *SimpleRWLock) RLock() (success bool) {
	// can not get writeLock --> return false
	if !atomic.CompareAndSwapInt32(&lock.writeLock, 0, 0) {
		return false
	}
	atomic.AddInt32(&lock.readLock, 1)
	return true
}

func (lock *SimpleRWLock) RUnlock() {
	atomic.AddInt32(&lock.readLock, -1)
}

func (lock *SimpleRWLock) WLock() (success bool) {
	// can not lock writeLock --> return false
	if !atomic.CompareAndSwapInt32(&lock.writeLock, 0, 1) {
		return false
	}

	// spin while readLock unlock
	for {
		if lock.readLock < 1 {
			return true
		}
	}
}

func (lock *SimpleRWLock) WUnlock() (success bool) {
	return atomic.CompareAndSwapInt32(&lock.readLock, 1, 0)
}

var lock SimpleRWLock
var x = 1

func printAndAddX(tr int32) {
	for i := 0; i < 20; i++ {
		if !lock.RLock() {
			continue
		}
		fmt.Printf("thread %d: read x = %d\n", tr, x)
		lock.RUnlock()

		if !lock.WLock() {
			continue
		}
		x++
		fmt.Printf("thread %d: add x to %d\n", tr, x)
		lock.WUnlock()
	}
	endChan <- 0

}

var endChan = make(chan int)

func main() {
	for i := 0; i < 10; i++ {
		go printAndAddX(int32(i))
	}

	for i := 0; i < 10; i++ {
		<-endChan
	}

}

