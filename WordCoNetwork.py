# -*- coding: gb2312 -*-
'''
-----------------------------------------------  
 WordCoNetwork: word co-occurrence network  
 Author : Zhang Hailong
 Date   : 2015-03-13  
 HomePage : http://
 Email  : purplehero3@qq.com
-----------------------------------------------
'''
import re
import networkx as nx
import to_pajek as tp
import pickle

#----构造词共现网络-----------------------------
def Creat_Graph_Net(pre_text):  #创建词网络
    #----构建词网络------
    G=nx.DiGraph()
    #nx.set_node_attributes(G,'word_property','')#添加结点属性--词性
    nx.set_node_attributes(G,'word_frequency',1)#添加结点属性--词频
   
    #----输入结点，计算词频----------------------------------
    node_list = []
    for word in pre_text:            #添加词频
        m1=word.strip().split('/')[0]
        #m2=word.strip().split('/')[1]
        if m1 == '。':
            node_list.append(m1)
        else:
            if m1 not in G.nodes():
                G.add_node(m1)
                G.node[m1]['word_frequency']=1
                #G.node[m1]['word_property']=m2
            else:
                G.node[m1]['word_frequency']+=1
        node_list.append(m1)
    #----输入边，计算边权重---------------------------------
    list_len=len(node_list)
    for i in range(0,list_len-1):         #按行读入文件，读取两个结点
        if((node_list[i].strip() == '。') or (node_list[i+1].strip() == '。')):
            #如果当前词或者下一个词为句号则不处理
            continue
        u,v= node_list[i],node_list[i+1]
        if u==v:               #删除结点相同的结点对，如“系统,系统”
            continue
        if G.get_edge_data(u,v):       #如果图G中有边(u,v),将此边权值+1
            w=G.get_edge_data(u,v)['weight']+1
            G.add_weighted_edges_from([(u,v,w)])
        else:
            #如果图G中没有边(u,v),将此边添加到图G
            G.add_weighted_edges_from([(u,v,1)])
            
    return G

#----生成随机图-------------
def random_gaph(a,b):
    #生成包含a个节点、以概率b连接的随机图
    G = nx.random_graphs.erdos_renyi_graph(28972,0.001002)
    return G

#----将网络保存到文件,以便于下次使用-------------------
def Save_Gaph(G,file_name):
    output = open(file_name+'.pkl','wb')
    pickle.dump(G,output)
    output.close()

#----从文件读入网络数据-----
def load_pkl_file(file_name):
    pkl_file = open(file_name,'rb')
    G=pickle.load(pkl_file)
    #pprint.pprint(pkl_file)
    pkl_file.close()
    return G

#----输出结点数、边数---------
def print_number_of_nodes_edges(G):
    print '网络结点数：',G.number_of_nodes()            #结点数
    print '网络边数：',G.number_of_edges()            #边数

#----删除权重小于阀值的边-------------------
def Del_Weight(G,edge_weight):
    for u,v,edgedata in G.edges(data=True):  #删除权重小于阀值的边
        d=int(edgedata['weight'])
        if d <edge_weight: #and G.node[u]['word_frequency']<2 and G.node[v]['word_frequency']<2:
            G.remove_edge(u,v)
    for node in G.nodes():    #删除度为零的结点
        if G.degree(node) == 0 and G.node[node]['word_frequency']<2:
            G.remove_node(node)
    return G

#----删除特定词性的结点--------------------
def Del_Property(G,word_property_list):
    for node in G.nodes():    #删除带有word_property_list中词性的结点
        if G.node[node]['word_property'] in word_property_list:
            G.remove_node(node)
    return G

#----删除权重小于阀值的边和特定词性的结点-------------
def Del_Weight_Property(G,edge_weight,word_property_list):
    for u,v,edgedata in G.edges(data=True):  #删除权重小于阀值的边
        d=int(edgedata['weight'])
        if d <edge_weight: #and G.node[u]['word_frequency']<2 and G.node[v]['word_frequency']<2:
            G.remove_edge(u,v)
    for node in G.nodes():    #删除带有word_property_list中词性的结点
        if G.node[node]['word_property'] in word_property_list:
            G.remove_node(node)
    for node in G.nodes():    #删除度为零的结点和
        if G.degree(node) == 0:
            G.remove_node(node)
    return G

#----词频输出-------------------------
def print_word_frequency(save_file):
    f=open(save_file,'w')
    for node in G.nodes():
        m=G.node[node]['word_frequency']
        f.write(node+':'+str(m)+'\n')
    f.close()

#----提取边权重，保存到文件-------------------
def print_weight(save_file):
    print "打印加权边"
    f=open(save_file,'w')
    for u,v,edgedata in G.edges(data=True):
        d=int(edgedata['weight'])
        s=''.join([str(u),str(G.node[u]['word_property']),'_',str(v),\
                    str(G.node[v]['word_property']),':',str(d),'\n'])
        f.write(s)
    f.close()

#----计算平均度分布----------------
def print_average_degree():
    degree = nx.degree_histogram(G)#返回图中所有节点的度分布序列
    degree_sum = 0
    i=0
    for d in degree:
        degree_sum =degree_sum + d*i
        i=i+1
    return float(degree_sum)/float(G.number_of_nodes())  #平均度分布

#----结点度分布---------------------
def print_node_degree(save_file):
    f=open(save_file,'w')
    d=G.degree()
    for node in G.nodes():
        f.write(node+G.node[node]['word_property']+':'+str(d[node])+'\n')
    f.close()

#----图直径-----------------
def diameter(G):     #返回图G的直径（最长最短路径的长度）
    return nx.diameter(G)

#----平均最短路径-----------------
def average_shortest_path(G):  #返回图G所有节点间平均最短路径长度   
    return nx.average_shortest_path_length(G)

#----计算子图数-----------------
def connected_subgraphs(G):
    if is_directed(G):   #判断是否有向图
        scc=nx.strongly_connected_component_subgraphs(G)#返回强连通子图的list
        wcc=nx.weakly_connected_components(G)#返回弱连通子图的list
        i=0
        for nn in scc:
            i=i+1
            print '第',i,'连通分量： ','边数：',nn.number_of_edges(),'  结点数：',nn.number_of_nodes()
    else:
        print '连通分量数：',nx.number_connected_components(G)    #连通分量数目
        #nx.connected_components(G)    #获取连通分量的节点列表，包含每个连通图的节点列表
        cc=nx.connected_component_subgraphs(G)#获取连通分量，返回的是列表，
            #但是元素是图，这些分量按照节点数目从大到小排列，所以第一个就是最大的连通分量
                #结点数
        i=0
        for nn in cc:
            i=i+1
            print '第',i,'连通分量： ','边数：',nn.number_of_edges(),'  结点数：',nn.number_of_nodes()

#----深度优先搜索------------
def dfs(G):
    f=open('3131.txt','w')
    for node1,node2 in nx.dfs_edges(G):
        f.write(str(node1)+' '+str(node2)+'\n')
    f.close()
    
#----main--------------
if __name__ == '__main__':
    pre_text=TextProcess('out1.txt')
    G=Creat_Graph_Net(pre_text)
    Save_Gaph(G,'network_xinwen')
    #G=load_pkl_file('network_xifenci.pkl')
    #G=load_pkl_file('network_nostopword.pkl')
    #G=confidence(G,20,0.5)
    Del_Weight(G,2)
    print_number_of_nodes_edges(G)
    #Del_Weight_Property(G,200,['v','vn'])
    tp.write_pajek(G,'Pajek001.net')
    #dfs(G)
    #G=Del_Weight_Property(G,1,'v,vt')
    #G=Del_Property(G,'v,vt')
    #frequent_pattern(G,pre_text,2,'2_pattern.txt')
    #repeat_eliminate('2_pattern.txt','2_eliminate.txt')
    #G=random_gaph(28972,0.001002)

