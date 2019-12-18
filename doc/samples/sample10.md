# Web App Server

## Use golang to read module config

To start a golang server with parameters 
(DSN, port, folder, service name, ...) taken from module config 
you may create some functions like:


```golang
package main

import (
	"fmt"
	"os"
	"strconv"
	"encoding/json"
)

type dict map[string]interface{}  //webcfg dict
type cfdict map[string]dict       //webcfg data & fields

type WebCfg struct {
	Data	cfdict `json:"data"`
	Fields	cfdict `json:"fields"` //ignored in this application
}


func LoadConfiguration(file string) WebCfg {
    var config WebCfg
    configFile, err := os.Open(file)
    if err != nil {
        fmt.Println(err.Error())
		return WebCfg{}
    }
    defer configFile.Close()
    jsonParser := json.NewDecoder(configFile)
    jsonParser.Decode(&config)
    return config
}

func (cfg WebCfg) GetString(name string, _default string) string {
	var ret string = _default
	for _, v := range cfg.Data {
		if name == v["name"] {
			ret = v["value"].(string)
			break
		}
	}
	return ret
}

func (cfg WebCfg) GetInt(name string, _default int) int {
	var ret int = _default
	for _, v := range cfg.Data {
		if name == v["name"] {
			_ret, err := strconv.Atoi(v["value"].(string))
			if err == nil {
				ret = _ret
			}
			break
		}
	}
	return ret
}



```

and then use this in main function 

```golang

func main() {
	//load config file
	cfg := LoadConfiguration("config.json")

	//read parameters
	DSN = cfg.GetString("DSN", "no DSN")
	RPC_PORT := cfg.GetInt("RPC_PORT", 8000)
	RPC_HOST := cfg.GetString("RPC_HOST", "127.0.0.1")

	//start golang rpc server
	RPC := fmt.Sprintf("%s:%d", RPC_HOST, RPC_PORT)
	fmt.Printf("Start RPC Server on %s\n", RPC)
	rpc_server = rpc.NewServer(rpc_func_map, true, nil)
	listener, err := net.Listen("tcp", RPC)
	if err != nil {
		fmt.Println("Error server listen.")
		return
	}
	rpc_server.Listen(listener)
	rpc_server.Run()
	fmt.Println("Server ends.")
}


```
