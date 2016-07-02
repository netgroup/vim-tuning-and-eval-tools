#!/usr/bin/python

import numpy as np
from utils import *

if __name__ == '__main__':

	down_artifact 	= []
	init_env 		= []
	spawn 			= []
	clean 			= []

	image_type 		= ' -  ClickOS'
	x_labels 		= ['Stock', 'Tuned']
	leg_labels 		= ['down_artifact', 'init_env', 'spawn', 'clean']
	title 			= 'Nomad driver breakdown'+ image_type
	ylabel 			= 'msec'
	
	down_temp 	= np.loadtxt('nomad_traces/down_artifact_stock.txt')
	init_temp	= np.loadtxt('nomad_traces/init_env_stock.txt')
	spawn_temp	= np.loadtxt('nomad_traces/spawn_stock.txt')
	clean_temp 	= np.loadtxt('nomad_traces/clean_stock.txt')

	data = np.column_stack((down_temp, init_temp, spawn_temp, clean_temp))
	with open('nomad_traces/driver_breakdown_raw_nomad_stock.txt','w+') as f:
		np.savetxt(f, data, fmt='%.6f')

	down_artifact.append(np.mean(down_temp, dtype=np.float32))
	init_env.append(np.mean(init_temp, dtype=np.float32))
	spawn.append(np.mean(spawn_temp, dtype=np.float32))
	clean.append(np.mean(clean_temp, dtype=np.float32))

	down_temp 	= np.loadtxt('nomad_traces/down_artifact_tuned.txt')
	init_temp	= np.loadtxt('nomad_traces/init_env_tuned.txt')
	spawn_temp	= np.loadtxt('nomad_traces/spawn_tuned.txt')
	clean_temp 	= np.loadtxt('nomad_traces/clean_tuned.txt')

	data = np.column_stack((down_temp, init_temp, spawn_temp, clean_temp))
	with open('nomad_traces/driver_breakdown_raw_nomad_tuned.txt','w+') as f:
		np.savetxt(f, data, fmt='%.6f')

	down_artifact.append(np.mean(down_temp, dtype=np.float32))
	init_env.append(np.mean(init_temp, dtype=np.float32))
	spawn.append(np.mean(spawn_temp, dtype=np.float32))
	clean.append(np.mean(clean_temp, dtype=np.float32))

	data = np.column_stack((down_artifact, init_env, spawn, clean))

	plot(data, title, ylabel, x_labels, leg_labels)