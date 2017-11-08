#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 20:53:56 2017

Power Grid Topo Analyser

@author: haotian
"""

import json
from queue import Queue

class Node:
    def __init__(self):
        self.edges = list()
    bs = -1
    state = False
    
class Bs:
    def __init__(self):
        self.nodes = list()
        self.edges = list()
    state = False
    island = -1

class Island:
    def __init(self):
        self.bss = list()

with open('homework.json', 'r') as f:
    data = json.load(f)
title = data['title']
n = data['node_count']
edges = data['edges']
m = len(edges)
nds = [Node() for i in range(0, n + 1)]
for i in range(0,m):
    if 'from' in edges[i].keys():
        fr = edges[i]['from']
        nds[fr].edges.append(i)
    if 'to' in edges[i].keys():
        to = edges[i]['to']
        nds[to].edges.append(i)
    if 'at' in edges[i].keys():
        at = edges[i]['at']
        nds[at].edges.append(i)        

bfs_queue = Queue()
bss = list()

for i in range(1, n + 1):
    if nds[i].state:
        continue
    bss.append(Bs())
    bfs_queue.put(i)
    while not bfs_queue.empty():
        i = bfs_queue.get()
        nds[i].bs = len(bss) - 1
        bss[len(bss) - 1].nodes.append(i)
        nds[i].state = True
        for ei in nds[i].edges:
            e = edges[ei]
            if e['type'] == 'CB' and e['state']:
                qi = e['from'] + e['to'] - i
                if not nds[qi].state:
                    bfs_queue.put(qi)
            elif e['type'] == 'BUS':
                qi = e['from'] + e['to'] - i
                if not nds[qi].state:
                    bfs_queue.put(qi)
                    
for i, e in enumerate(edges):
    if e['type'] == 'LINE' or e['type'] == 'TRFM' or e['type'] == 'CB':
        if nds[e['from']].bs != nds[e['to']].bs:
            bss[nds[e['from']].bs].edges.append(i)
            bss[nds[e['to']].bs].edges.append(i)

for i, bs in enumerate(bss):
    if bs.state:
        continue


for i, bs in enumerate(bss):
    print('BS%d:%s' % (i + 1, bs.nodes))