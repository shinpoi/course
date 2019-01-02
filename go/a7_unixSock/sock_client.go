package main

import (
	"io"
	"log"
	"net"
	"time"
)

func reader(r io.Reader) {
	buf := make([]byte, 1024)
	for {
		n, err := r.Read(buf[:])
		if err != nil {
			log.Print("Client read: ", err)
			return
		}
		println("Client got:", string(buf[0:n]))
	}
}

func main() {
	conn, err := net.Dial("unix", sockAdress)
	if err != nil {
		log.Fatal("Dial error", err)
	}
	defer conn.Close()

	go reader(conn)
	for {
		msg := "hello, unix domain socket!"
		_, err := conn.Write([]byte(msg))
		if err != nil {
			log.Fatal("Write error:", err)
			break
		}
		println("Client sent:", msg)
		time.Sleep(10 * time.Second)
	}
}