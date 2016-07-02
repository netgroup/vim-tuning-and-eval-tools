#!/usr/bin/python

from scapy.all import *
import matplotlib.pyplot as plt
import numpy as np

def rdpcap_and_close(filename, count=-1):
    pcap_reader = PcapReader(filename)
    packets = pcap_reader.read_all(count=count)
    pcap_reader.close()
    return packets

def plot(data, title, xlabel, ticklabels, legendlabels):

    N = data.shape[0] 
    bar_width = 0.6  
    bar_n = legendlabels.__len__()       
    ind = np.arange(N)
    fig, ax = plt.subplots()

    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_yticks(ind + bar_width/2)
    ax.set_yticklabels(ticklabels)
    rects = []
    legend_col = []
    c = 0.30
    sum_data = None 
    for i in range(0,bar_n):
        if i:
            rects.append(ax.barh(ind, data[:,[i]], bar_width, left=sum_data, color=str(c),edgecolor = "none"))
            sum_data += np.squeeze(np.asarray(data[:,[i]]))
        else:
            rects.append(ax.barh(ind, data[:,[i]], bar_width, color=str(c),edgecolor = "none"))
            sum_data = np.squeeze(np.asarray(data[:,[i]]))
        c += 0.10
        legend_col.append(rects[i][0])  
    
    #start, end = ax.get_xlim()
    #minor_ticks = np.arange(start, end, 0.05)
    #print minor_ticks 
    #ax.set_xticks(minor_ticks, minor=False)
    y_start, y_end = ax.get_ylim()
    ax.set_ylim(-bar_width/2, y_end+bar_width/2)
    ax.xaxis.grid(which='minor', alpha=0.5)                                                
    ax.xaxis.grid(which='major', alpha=0.8) 
    ax.legend(legend_col,legendlabels,loc=0)    
    plt.savefig('./'+ title+'.png')