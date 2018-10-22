Vim-tuning-and-eval-tools
================================

Tools for performance evaluation and tuning of Virtual Infrastructure Managers for (Micro) Virtual Network Functions

License
=============

This sofware is licensed under the Apache License, Version 2.0.

Information can be found here:
 [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

Structure
=============

The repository is organized in this way:
- **NOMAD.patch** contains our patch which adds the initial support for XEN hypervisor and some utility scripts;
- **NOMAD_tuned.patch** contains our patch which tunes the support for XEN hypervisor and contains some utility scripts;
- **nomad_utilities** folder contains scripts we used to generate Jobs, to analyze the packets and to generate the plots;
- **nova** folder contains the modification to Nova component and includes also the tuned driver;
- **glance** folder contains the modification to Glance component;

Tips
==============

We report some suggestions useful to handle the code:
- **NOMAD_tuned.patch** depends on NOMAD.patch. 
- **NOMAD.patch** depends on commit 7f4140758ee0660e23303305a2634ef442a76114.
- It is necessary to install all the dependecies of the Python scripts.
- It is necessary to install all the dependecies of the GO program. 
- **nomad_pusher.go** depens on xen_job.json

Usage
==============

We report the usage of our scripts:

- For nomad_driver_analyzer.py, it is necessary to put the necessary input in the folder ./nomad_traces and then run the command:
		
		./nomad_driver_analyzer.py

- For nomad_packet_analyzer.py, it is necessary to put the necessary packets traces in the folder ./nomad_traces and then run the command:
		
		./nomad_packets_analyzer.py

- For nomad_pusher.jo, it is necessary to create a main program like this:

		package main

		import (
		    "github.com/user_xxx/our_go_files"
		)

		func main() {
		    pushers.NomadJobPusher("xen", 100)
		}