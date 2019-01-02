package main

import (
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
)

func echoServer(conn net.Conn) {
	defer conn.Close()
	for {
		buf := make([]byte, 512)
		size, err := conn.Read(buf)
		if err != nil {
			log.Print("Server read: ", err)
			return
		}

		data := buf[0:size]
		println("Server got: ", string(data))
		_, err = conn.Write(data)
		if err != nil {
			log.Fatal("Writing client error: ", err)
		}
	}
}

func main() {
	log.Println("Starting echo server")

	ls, err := net.Listen("unix", sockAdress)
	if err != nil {
		log.Fatal("Listen error: ", err)
	}

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM, syscall.SIGINT)

	go func(listener net.Listener, ch chan os.Signal) {
		sig := <-ch
		log.Printf("Caught signal %s: shutting down.", sig)
		err := listener.Close()
		if err != nil {
			log.Fatal("close error: ", err)
		}
		os.Exit(0)
	}(ls, sigChan)

	for {
		fd, err := ls.Accept()
		if err != nil {
			log.Fatal("Accept error: ", err)
		}
		log.Print("accept a new connection: ", fd)
		go echoServer(fd)
	}
}
