package pushers

import (

"fmt"
"strings"
"net/http"
"encoding/json"
"bytes"
"time"
"os"

)

func CreateHttpRequest(job XenJob) (*http.Request) {

	baseUrl 	:= "http://127.0.0.1:4646/v1"
	jobAPI 		:= "jobs"
	jobUrl		:= strings.Join([]string{baseUrl, jobAPI}, "/")

	

    b, err := json.Marshal(&job)
	if err != nil {
		fmt.Println("Encoding Error")
		return nil
	}

	req, err := http.NewRequest("PUT", jobUrl, bytes.NewBuffer(b))
	req.Header.Set("Content-Type", "application/json")
	return req
}


func NomadJobPusher(type_ string, run int) {

	job 		:= CreateXenJob(type_)

	for i := 0; i < run; i++ {

		job.XenJob.Name = fmt.Sprintf("example%v", i+1)
		job.XenJob.ID 	= fmt.Sprintf("example%v", i+1)

		req 		:= CreateHttpRequest(job)
		client 		:= &http.Client{}
		resp, err 	:= client.Do(req)
	    if err != nil {
	        fmt.Println("HTTP PUT Error")
	        fmt.Println(err)
	    }
	    defer resp.Body.Close()

	    

	    fmt.Printf("XenJob %s Pushed and Status:%s\n", job.XenJob.Name, resp.Status)
	    time.Sleep(1 * time.Second)

	    sshclient 	:= CreateSSHClient("root", "root", "127.0.0.1")
	    sshcommand 	:= CreateXlDestroy()

		fmt.Printf("Running command: %s\n", sshcommand.Path)
		if err := sshclient.RunCommand(sshcommand); err != nil {
			fmt.Fprintf(os.Stderr, "command run error: %s\n", err)
			os.Exit(1)
		}
		time.Sleep(5 * time.Second)

	}

}