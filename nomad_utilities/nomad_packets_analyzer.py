#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import argparse
import sys
import json
import logging
import binascii
import numpy as np

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
from utils import *

JOBID 					= "jobid"
TASKID 					= "taskid"
ALLOCID 				= "allocid"
PUTTS					= "putts"
CREATETS				= "createts"
IDCREATETS				= "idcreatets"
IDREPLYTS				= "idreplyts"
TERMTS					= "termts"
allocid_jobs 			= {}
ack_jobs				= {}
name_jobs				= {}
allocid_ts				= {}
scheduling				= []
driver					= []

ACK 					= 0x010
PSH_ACK 		 		= 0x018
HTTP_OK_MESSAGE  		= "200 OK"
HTTP_PUT_MESSAGE 		= "PUT /v1/jobs"

NOMAD_SERVER_HTTP_PORT 	= 4646
NOMAD_SERVER_RPC_PORT  	= 4647

def evaluateNomad(file_name):

	print "Evaluating Nomad"

	global ack_jobs
	global scheduling
	global driver

	print len(driver)
	print len(scheduling)

	packets = rdpcap_and_close(file_name)
	for packet in packets:
		if TCP in packet:

			dport   = packet[TCP.name].dport
			payload = packet[TCP.name].payload.__str__()
			sport   = packet[TCP.name].sport
			flags   = packet[TCP.name].flags
			ack 	= str(packet[TCP.name].ack)
			seq		= str(packet[TCP.name].seq)

			if HTTP_PUT_MESSAGE in payload and dport == NOMAD_SERVER_HTTP_PORT:
				found = re.search('"ID":"(.+?)"', payload)
				if found:
					name 						= found.group(1)
					ts 							= packet.time
					name_jobs[name][PUTTS] 		= ts
				else:
					print "regex not working properly"
					sys.exit(-1)

			elif (flags == PSH_ACK or flags == ACK) and sport == NOMAD_SERVER_RPC_PORT:
				found_names 	= re.findall('([a-zA-Z0-9\-\_]{8,10}).Parent', payload)
				found_allocids	= re.findall('([a-zA-Z0-9\-\_]{36}).Job', payload)

				if len(found_names) != len(found_allocids):
					print "trace not usable"
					sys.exit(-1)

				allocids = []

				for name, allocid in zip(found_names, found_allocids):
					ts 									= packet.time
					ts_put								= name_jobs[name][PUTTS]
					allocid_jobs[allocid][CREATETS] 	= ts
					allocid_jobs[allocid][PUTTS]		= ts_put
					allocids.append(allocid_jobs[allocid][ALLOCID])
				
				if len(found_names) > 0 and len(found_allocids) > 0:
					ack_jobs[ack] = allocids

			elif flags == PSH_ACK and dport == NOMAD_SERVER_RPC_PORT:
				matches 		= re.findall('([a-zA-Z0-9\-\_]{36})', payload)
				node_ids 		= re.findall('NodeID.+([a-zA-Z0-9\-\_]{36})', payload)
				found_desired	= re.search('DesiredStatus', payload)
				node_register	= re.search('Node.Register', payload)

				if node_register:
					continue

				if not found_desired:
					ts_id_reply = packet.time
					for match in matches:
						if match not in node_ids and allocid_ts.get(match, None) != None:
							ts_id_create 					= allocid_ts[match][IDCREATETS]
							allocid_jobs[match][IDREPLYTS]	= ts_id_reply
							allocid_jobs[match][IDCREATETS]	= ts_id_create
				else:
					ts_term 	= packet.time
					allocids 	= []
					for match in matches:
						if match not in node_ids:
							allocid_jobs[match][TERMTS]	= ts_term
							allocids.append(match)

					if len(matches) > 0 and len(matches) > len(node_ids):
						ack_jobs[ack] = allocids

	for k,v in allocid_jobs.items():
		createts 	= v.get(CREATETS)
		putts 		= v.get(PUTTS)
		termts 		= v.get(TERMTS)

		if createts and putts:
			scheduling.append(createts - putts)

		if createts and termts:
			driver.append(termts - createts)


def define_connections(file_name):

	global allocid_jobs
	global name_jobs

	packets = rdpcap_and_close(file_name)
	for packet in packets:
		if TCP in packet:

			dport   = packet[TCP.name].dport
			payload = packet[TCP.name].payload.__str__()
			sport   = packet[TCP.name].sport

			if HTTP_PUT_MESSAGE in payload and dport == NOMAD_SERVER_HTTP_PORT:
				found = re.search('"ID":"(.+?)"', payload)
				if found:
					name 				= found.group(1)
					job 				= {}
					job[JOBID]			= name
					name_jobs[name]		= job
				else:
					print "regex not working properly"
					sys.exit(-1)

	for packet in packets:
		if TCP in packet:

			flags   = packet[TCP.name].flags
			sport   = packet[TCP.name].sport
			dport   = packet[TCP.name].dport
			payload = packet[TCP.name].payload.__str__()

			if (flags == PSH_ACK or flags == ACK)  and sport == NOMAD_SERVER_RPC_PORT:
				
				found_names 	= re.findall('([a-zA-Z0-9\-\_]{8,10}).Parent', payload)
				found_allocids	= re.findall('([a-zA-Z0-9\-\_]{36}).Job', payload)

				if len(found_names) != len(found_allocids):
					print "trace not usable"
					sys.exit(-1)

				for name, allocid in zip(found_names, found_allocids):

					job 					= {}
					job[ALLOCID] 			= allocid
					job[JOBID]				= name
					allocid_jobs[allocid] 	= job

if __name__ == '__main__':

		scheduling_total 	= []
		driver_total		= []

		print "Nomad Stock"
		define_connections("nomad_traces/server_stock.pcap")
		evaluateNomad("nomad_traces/server_stock.pcap")

		scheduling_total.append(np.mean(scheduling, dtype=np.float64))
		driver_total.append(np.mean(driver, dtype=np.float64))

		data = np.column_stack((scheduling, driver))
		with open('nomad_traces/create_and_boot_raw_nomad_stock.txt','w+') as f:
			np.savetxt(f, data, fmt='%.6f')

		scheduling 	= []
		driver 	 	= []

		print "################################"

		print "Nomad Tuned"
		define_connections("nomad_traces/server_tuned.pcap")
		evaluateNomad("nomad_traces/server_tuned.pcap")

		scheduling_total.append(np.mean(scheduling, dtype=np.float64))
		driver_total.append(np.mean(driver, dtype=np.float64))

		scheduling 	= scheduling[:100]
		driver 		= driver[:100]

		data = np.column_stack((scheduling, driver))
		with open('nomad_traces/create_and_boot_raw_nomad_tuned.txt','w+') as f:
			np.savetxt(f, data, fmt='%.6f')

		image_type 	= ' -  ClickOS'
		x_labels 	= ['Stock', 'Tuned']
		leg_labels 	= ['Scheduling', 'Driver']
		title = 'Nomad create and boot one instance'+ image_type
		ylabel = 'sec'

		data = np.column_stack((scheduling_total, driver_total))

		plot(data, title, ylabel, x_labels,leg_labels)	

	
