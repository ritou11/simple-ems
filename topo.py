#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 20:53:56 2017

Power Grid Topo Analyser

@author: haotian
"""

import json
from queue import Queue
# TODO: Seperate into functions
# TODO: Print node topo
# TODO: Add notes


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
    kv = -1


class Island:
    def __init__(self):
        self.bss = list()


class Kv:
    def __init__(self):
        self.bss = list()


with open('homework.json', 'r') as f:
    data = json.load(f)
title = data['title']
n = data['node_count']
edges = data['edges']
m = len(edges)
nds = [Node() for i in range(0, n + 1)]
for i in range(0, m):
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
islands = list()
kvs = list()

for k in range(1, n + 1):
    if nds[k].state:
        continue
    bss.append(Bs())
    bfs_queue.put(k)
    nds[k].state = True
    while not bfs_queue.empty():
        i = bfs_queue.get()
        nds[i].bs = len(bss) - 1
        bss[-1].nodes.append(i)
        for ei in nds[i].edges:
            e = edges[ei]
            if e['type'] == 'CB' and e['state']:
                qi = e['from'] + e['to'] - i
                if not nds[qi].state:
                    bfs_queue.put(qi)
                    nds[qi].state = True
            elif e['type'] == 'BUS':
                qi = e['from'] + e['to'] - i
                if not nds[qi].state:
                    bfs_queue.put(qi)
                    nds[qi].state = True

for i, e in enumerate(edges):
    if e['type'] == 'LINE' or e['type'] == 'TRFM' or e['type'] == 'CB':
        if nds[e['from']].bs != nds[e['to']].bs:
            bss[nds[e['from']].bs].edges.append(i)
            bss[nds[e['to']].bs].edges.append(i)

for k, bs in enumerate(bss):
    if bs.state:
        continue
    islands.append(Island())
    bfs_queue.put(k)
    bs.state = True
    while not bfs_queue.empty():
        i = bfs_queue.get()
        bss[i].island = len(islands) - 1
        islands[-1].bss.append(i)
        for ei in bss[i].edges:
            e = edges[ei]
            if e['type'] == 'LINE' or e['type'] == 'TRFM':
                qi = nds[e['from']].bs + nds[e['to']].bs - i
                if not bss[qi].state:
                    bfs_queue.put(qi)
                    bss[qi].state = True
for bs in bss:
    bs.state = False
for k, bs in enumerate(bss):
    if bs.state:
        continue
    kvs.append(Kv())
    bfs_queue.put(k)
    bs.state = True
    while not bfs_queue.empty():
        i = bfs_queue.get()
        bss[i].kv = len(kvs) - 1
        kvs[-1].bss.append(i)
        for ei in bss[i].edges:
            e = edges[ei]
            if e['type'] == 'CB':
                qi = nds[e['from']].bs + nds[e['to']].bs - i
                if not bss[qi].state:
                    bfs_queue.put(qi)
                    bss[qi].state = True
# TODO: Print friendly
for i, bs in enumerate(bss):
    print('BS%d:%s' % (i + 1, bs.nodes))
for i, island in enumerate(islands):
    print('Island%d:%s' % (i + 1, [x + 1 for x in island.bss]))
for i, kv in enumerate(kvs):
    print('KV%d:%s' % (min(kv.bss) + 1, [x + 1 for x in kv.bss]))
