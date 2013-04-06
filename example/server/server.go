// Copyright (c) 2013 Mathieu Turcotte
// Licensed under the MIT license.

package main

import (
	"flag"
	"github.com/MathieuTurcotte/go-browserchannel/bc"
	"log"
	"net/http"
)

var public = flag.String("public_directory", "", "path to public directory")

func HandleChannel(channel *bc.Channel) {
	log.Printf("Handlechannel (%q)\n", channel.Sid)

	for {
		m, ok := channel.ReadMap()
		if !ok {
			log.Printf("%s: returned with no data, closing\n", channel.Sid)
			break
		}

		log.Printf("%s: map: %#v\n", channel.Sid, *m)
		channel.SendArray([]interface{}{"a", "b", "c"})
	}
}

func main() {
	flag.Parse()

	handler := bc.NewHandler()
	handler.SetCrossDomainPrefix("hpenvy.local:8080", "bc0")
	handler.Init()

	http.Handle("/channel/", handler)
	http.Handle("/", http.FileServer(http.Dir(*public)))

	// TODO: If no one reads from the handler, new channels won't be
	// served and the whole server will block. This is a problem.
	go func() {
		for {
			channel, err := handler.Accept()
			if err != nil {
				log.Fatal("handler.Accept: ", err)
			}
			go HandleChannel(channel)
		}
	}()

	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
