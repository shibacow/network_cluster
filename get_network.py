#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from mog_op import MongoOp
import pylab
import community as community_louvain
import matplotlib.cm as cm
import networkx as nx
from collections import Counter
def get_data():
    mp = MongoOp('localhost',db='twitter_retweet_users')
    col=mp.get_col('gakujyutu_kaigi')
    query='this.retweeters.length >= 50'
    cond={'$where':query}
    rdict={}
    cnt=0
    for a in col.find(cond):
        tid=int(a['twitter_id'])
        rdict.setdefault(tid,set())
        assert(len(a['retweeters'])>=50)
        for u in a['retweeters']:
            rdict[tid].add(int(u))
        cnt+=1
        if cnt % 1000==0:
            msg='cnt={} tid={}'.format(cnt,tid)
            print(msg)
    print('cnt={}'.format(cnt))
    return rdict
def gen_graph(rdict):
    print('rdict size={}'.format(len(rdict)))
    vector=[]
    cnt2=0
    for i,iu in rdict.items():
        cnt2+=1
        if cnt2 % 1000 == 0:
            print('cnt2={}'.format(cnt2))
        for j,ju in rdict.items():
            if i==j:continue
            simp_a=len(iu & ju)
            simp_b=min(len(iu),len(ju))
            if simp_b==0:continue
            simp_v=simp_a/simp_b
            if simp_v > 0.01:
                v0=(i,j,{'weight':simp_v})
                vector.append(v0)
    graph=nx.Graph()
    cnt=Counter()
    graph.add_edges_from(vector)
    deg = graph.degree()
    #to_remove = [n[0] for n in deg if n[1] < 10]
    #graph.remove_nodes_from(to_remove)
    print('graph={}'.format(graph))
    #first compute the best partition
    print('start calc comunity')
    partition = community_louvain.best_partition(graph)
    print('start calc comunity')
    print('partition size={}'.format(len(partition)))
    pylab.figure(figsize=(30,30))
    # draw the graph
    pos = nx.spring_layout(graph)
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(graph, pos, partition.keys(), node_size=5,
                           cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(graph, pos,width=3.0)
    pylab.show()
    pylab.savefig("graph_networkx.png")

def main():
    rdict=get_data()
    gen_graph(rdict)
if __name__=='__main__':main()
