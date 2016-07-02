package pushers

import (

"fmt"
"strings"
"io/ioutil"
"encoding/json"
"os"

)


type Resources struct {
	CPU 		int32 			`json:"CPU"`
	MemoryMB 	int32 			`json:"MemoryMB"`
	DiskMB		int32			`json:"DiskMB"`
	IOPS		int32			`json:"IOPS"`
	Networks	interface {} 	`json:"Networks"`
}

type XenConfig struct {
	ImgSource string 	`json:"img_source"`
	CfgSource string 	`json:"cfg_source"`
}

type LogConfig struct {
	MaxFiles 		int32 	`json:"MaxFiles"`
	MaxFileSizeMB	int32 	`json:"MaxFileSizeMB"`
}

type RestartPolicy struct {
	Interval 	int64 	`json:"Interval"`
	Attempts 	int32	`json:"Attempts"`
	Delay 		int64 	`json:"Delay"`
	Mode 		string 	`json:"Mode"`
}

type XenTask struct {
	Name 			string 			`json:"Name"`
	Driver 			string 			`json:"Driver"`
	Config 			XenConfig		`json:"Config"`
	Constraints 	interface {}	`json:"Constraints"`
	Env 			interface {} 	`json:"Env"`
	Services 		interface {}	`json:"Services"`
	Resources 		Resources 		`json:"Resources"`
	Meta 			interface {} 	`json:"Meta"`
	KillTimeout  	int64			`json:"KillTimeout"`
	LogConfig 		LogConfig		`json:"LogConfig"`
}

type XenTaskGroup struct {
	Name 			string 			`json:"Name"`
	Count 			int32 			`json:"Count"`
	Constraints		interface {} 	`json:"Constraints"`
	Tasks 			[]XenTask	 	`json:"Tasks"`
	RestartPolicy 	RestartPolicy 	`json:"RestartPolicy"`
	Meta 			interface {} 	`json:"Meta"`
}

type Constraint struct {
	LTarget 	string 	`json:"LTarget"`
	RTarget 	string 	`json:"RTarget"`
	Operand 	string 	`json:"Operand"`
}

type Update struct {
	Stagger  	int64 	`json:"Stagger"`
	MaxParallel int 	`json:"MaxParallel"`
}

type XenJobDescription struct {
	Region 				string 			`json:"Region"`
	ID 					string 			`json:"ID"`
	Name 				string  		`json:"Name"`
	Type 				string 			`json:"Type"`
	Priority 			int 			`json:"Priority"`
	AllAtOnce 			bool			`json:"AllAtOnce"`
	Datacenters			[]string 		`json:"Datacenters"`
	Constraints 		[]Constraint 	`json:"Constraints"`
	TaskGroups 			[]XenTaskGroup `json:"TaskGroups"`
	Update 				Update 			`json:"Update"`
	Periodic 			interface {} 	`json:"Periodic"`
	Meta				interface {} 	`json:"Meta"`
	Status 				string 			`json:"Status"`
	StatusDescription 	string 			`json:"StatusDescription"`
	CreateIndex			int32			`json:"CreateIndex"`
	ModifyIndex			int32			`json:"ModifyIndex"`
}

type XenJob struct {
	XenJob 	XenJobDescription 	 `json:"Job"`	
}


func CreateXenJob(type_ string) XenJob {
	file_name 	:= strings.Join([]string{type_, "job.json"}, "_")
	path 		:= strings.Join([]string{"/home/conet/workspace/goprojects/src/github.com/pierventre/KARAOKE-Pushers", file_name}, "/")

	file, e 	:= ioutil.ReadFile(path)

    if e != nil {
        fmt.Printf("File error: %v\n", e)
        os.Exit(1)
    }

    var job XenJob
    json.Unmarshal(file, &job)
    return job
}
