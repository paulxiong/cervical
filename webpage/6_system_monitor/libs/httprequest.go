package lib

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

var url string = "http://127.0.0.1:3000/api1/smonitor"

func httpPostJSON(sysinfo SysStateInfo) {
	jsons, _ := json.Marshal(sysinfo)
	result := string(jsons)
	jsoninfo := strings.NewReader(result)

	req, err := http.NewRequest("POST", url, jsoninfo)
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
	}

	if resp != nil && resp.Body != nil {
		// statuscode := resp.StatusCode
		// hea := resp.Header
		// body, _ := ioutil.ReadAll(resp.Body)
		// fmt.Println(string(body))
		// fmt.Println(statuscode)
		// fmt.Println(hea)
		resp.Body.Close()
	}
}
