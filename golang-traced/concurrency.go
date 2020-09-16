package main

import (
	"log"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {

	log.Println("ingrese")
	data := r.URL.Query()
	//var1 := data["var1"]

}

func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe(":80", nil)
}
