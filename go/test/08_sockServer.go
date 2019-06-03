package main

import (
	"log"
	"net"
	"net/http"
	"net/http/fcgi"
	"os"
)

const (
	sockType = "unix"
	scoPath = "/__path__/nginx.sock"
)


func ServeHTTP(w http.ResponseWriter, r *http.Request) {
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
	ls, err := net.Listen(sockType, scoPath)
	if err != nil {
		log.Fatal("unix sock error: ", err)
		os.Exit(-1)
	}

	// fcgi
	http.HandleFunc("/", ServeHTTP)
	err = fcgi.Serve(ls, nil)
	if err != nil {
		log.Fatal("http server start err: ", err)
		os.Exit(-1)
	}

	// http
	/*
	http.HandleFunc("/", ServeHTTP)
	server := http.Server{}

	err = server.Serve(ls)
	if err != nil {
		log.Fatal("http server start err: ", err)
		os.Exit(-1)
	}
	*/
}
