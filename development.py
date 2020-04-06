#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time: 2020/4/5 21:14
# @Author: qyh

import matplotlib.pyplot as plt
import numpy.random as rdm
import networkx as nx

node_num = 100
probability = 0.01
er_graph = nx.erdos_renyi_graph(node_num, probability)
susceptible = 'S'
infected = 'I'
recovered = 'R'


# Init
def onset(graph):
    for i in graph.nodes.keys():
        graph.nodes[i]['state'] = susceptible


# Set infection rate
def infect_prop(graph, proportion):
    for i in graph.nodes.keys():
        if rdm.random() <= proportion:
            graph.nodes[i]['state'] = infected


# Model building
def build_model(p_infect, p_recover):
    def model(graph, i):
        if graph.nodes[i]['state'] == infected:
            for m in graph.neighbors(i):
                if graph.nodes[m]['state'] == susceptible:
                    if rdm.random() <= p_infect:
                        graph.nodes[m]['state'] = infected
            if rdm.random() <= p_recover:
                graph.nodes[i]['state'] = recovered
    return model


# Single model run
def model_run(graph, model):
    for i in graph.nodes.keys():
        model(graph, i)


# Multiple model cycles
def model_iter(graph, model, iter_num):
    for i in range(iter_num):
        model_run(graph, model)


def draw(graph):
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xticks([])
    ax.set_xticks([])
    pos = nx.spring_layout(graph, k=0.2)
    nx.draw_networkx_edges(graph, pos, alpha=0.5, width=1)
    nx.draw_networkx_nodes(graph, pos, node_size=80)
    plt.show()


def calc_infection_rate(graph):
    onset(graph)
    infect_prop(graph, 0.05)
    model = build_model(0.2, 0.8)
    model_iter(graph, model, 10)
    infect = [v for (v, attr) in graph.nodes(data=True) if attr['state'] == recovered]
    infection_rate = len(infect) / node_num
    print(infection_rate)


if __name__ == '__main__':
    draw(er_graph)
    calc_infection_rate(er_graph)
