package main

import (
	"log"
	"net"
	"net/http"
	"os"
)

const sockPath = "/path_to/proxy_nginx.sock"

type myHandle struct{}

func (myHandle) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		_, err := w.Write([]byte("hello, nginx!"))
		if err != nil {
			log.Print("http handle err: ", err)
			return
		}
	}
}

func main() {
	log.Println("Starting http server")
	ls, err := net.Listen("unix", sockPath)
	if err != nil {
		log.Fatal("unix sock error: ", err)
		os.Exit(-1)
	}

	handle := myHandle{}
	server := http.Server{
		Handler: handle,
	}

	err = server.Serve(ls)
	if err != nil {
		log.Fatal("http server start err: ", err)
		os.Exit(-1)
	}
}
