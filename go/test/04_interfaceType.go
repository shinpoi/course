package main

import (
	"fmt"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"log"
	"reflect"
)

func main() {
	var vInt interface{} = 123
	var vString interface{} = "123456"
	var vArrFloat = []interface{}{1.1, 2.2, 3.3}

	fmt.Printf("v_int: %v\nv_string: %v\nv_arr_float: %v\nv_arr_float[0]: %v\n",
		reflect.TypeOf(vInt).Kind() == reflect.Int,
		reflect.TypeOf(vString).Kind() == reflect.String,
		reflect.TypeOf(vArrFloat).Kind() == reflect.Slice,
		reflect.TypeOf(vArrFloat).Kind() == reflect.Float64)

	fmt.Println("interface test over ----------------------------")

	// test yaml lib
	data, err := ioutil.ReadFile("04_interfaceType.yaml")
	if err != nil{
		log.Fatal(err)
	}

	m := make(map[string]interface{})
	err = yaml.Unmarshal([]byte(data), &m)
	if err != nil {
		log.Fatalln(err)
	}

	fmt.Println("yaml ----------------------------")
	for key := range m {
		fmt.Printf("%v: %v\n", key, reflect.TypeOf(m[key]))
	}


	fmt.Println("arr ----------------------------")
	arr := m["array"].([]interface{})
	for i:=0; i< len(arr); i++ {
		fmt.Printf("- %v\n", reflect.TypeOf(arr[i]))
	}

	mp := m["map"].(map[interface{}]interface{})
	fmt.Println("map ----------------------------")
	for key := range mp {
		fmt.Printf("%v: %v\n", key, reflect.TypeOf(mp[key]))
	}

	multiArr := m["multi"].([]interface{})
	fmt.Println("multiArr ----------------------------")
	for i:=0; i< len(multiArr); i++ {
		fmt.Printf("- %v\n", reflect.TypeOf(multiArr[i]))
	}

}
