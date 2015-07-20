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

#----����ʹ�������-----------------------------
def Creat_Graph_Net(pre_text):  #����������
    #----����������------
    G=nx.DiGraph()
    #nx.set_node_attributes(G,'word_property','')#��ӽ������--����
    nx.set_node_attributes(G,'word_frequency',1)#��ӽ������--��Ƶ
   
    #----�����㣬�����Ƶ----------------------------------
    node_list = []
    for word in pre_text:            #��Ӵ�Ƶ
        m1=word.strip().split('/')[0]
        #m2=word.strip().split('/')[1]
        if m1 == '��':
            node_list.append(m1)
        else:
            if m1 not in G.nodes():
                G.add_node(m1)
                G.node[m1]['word_frequency']=1
                #G.node[m1]['word_property']=m2
            else:
                G.node[m1]['word_frequency']+=1
        node_list.append(m1)
    #----����ߣ������Ȩ��---------------------------------
    list_len=len(node_list)
    for i in range(0,list_len-1):         #���ж����ļ�����ȡ�������
        if((node_list[i].strip() == '��') or (node_list[i+1].strip() == '��')):
            #�����ǰ�ʻ�����һ����Ϊ����򲻴���
            continue
        u,v= node_list[i],node_list[i+1]
        if u==v:               #ɾ�������ͬ�Ľ��ԣ��硰ϵͳ,ϵͳ��
            continue
        if G.get_edge_data(u,v):       #���ͼG���б�(u,v),���˱�Ȩֵ+1
            w=G.get_edge_data(u,v)['weight']+1
            G.add_weighted_edges_from([(u,v,w)])
        else:
            #���ͼG��û�б�(u,v),���˱���ӵ�ͼG
            G.add_weighted_edges_from([(u,v,1)])
            
    return G

#----�������ͼ-------------
def random_gaph(a,b):
    #���ɰ���a���ڵ㡢�Ը���b���ӵ����ͼ
    G = nx.random_graphs.erdos_renyi_graph(28972,0.001002)
    return G

#----�����籣�浽�ļ�,�Ա����´�ʹ��-------------------
def Save_Gaph(G,file_name):
    output = open(file_name+'.pkl','wb')
    pickle.dump(G,output)
    output.close()

#----���ļ�������������-----
def load_pkl_file(file_name):
    pkl_file = open(file_name,'rb')
    G=pickle.load(pkl_file)
    #pprint.pprint(pkl_file)
    pkl_file.close()
    return G

#----��������������---------
def print_number_of_nodes_edges(G):
    print '����������',G.number_of_nodes()            #�����
    print '���������',G.number_of_edges()            #����

#----ɾ��Ȩ��С�ڷ�ֵ�ı�-------------------
def Del_Weight(G,edge_weight):
    for u,v,edgedata in G.edges(data=True):  #ɾ��Ȩ��С�ڷ�ֵ�ı�
        d=int(edgedata['weight'])
        if d <edge_weight: #and G.node[u]['word_frequency']<2 and G.node[v]['word_frequency']<2:
            G.remove_edge(u,v)
    for node in G.nodes():    #ɾ����Ϊ��Ľ��
        if G.degree(node) == 0 and G.node[node]['word_frequency']<2:
            G.remove_node(node)
    return G

#----ɾ���ض����ԵĽ��--------------------
def Del_Property(G,word_property_list):
    for node in G.nodes():    #ɾ������word_property_list�д��ԵĽ��
        if G.node[node]['word_property'] in word_property_list:
            G.remove_node(node)
    return G

#----ɾ��Ȩ��С�ڷ�ֵ�ıߺ��ض����ԵĽ��-------------
def Del_Weight_Property(G,edge_weight,word_property_list):
    for u,v,edgedata in G.edges(data=True):  #ɾ��Ȩ��С�ڷ�ֵ�ı�
        d=int(edgedata['weight'])
        if d <edge_weight: #and G.node[u]['word_frequency']<2 and G.node[v]['word_frequency']<2:
            G.remove_edge(u,v)
    for node in G.nodes():    #ɾ������word_property_list�д��ԵĽ��
        if G.node[node]['word_property'] in word_property_list:
            G.remove_node(node)
    for node in G.nodes():    #ɾ����Ϊ��Ľ���
        if G.degree(node) == 0:
            G.remove_node(node)
    return G

#----��Ƶ���-------------------------
def print_word_frequency(save_file):
    f=open(save_file,'w')
    for node in G.nodes():
        m=G.node[node]['word_frequency']
        f.write(node+':'+str(m)+'\n')
    f.close()

#----��ȡ��Ȩ�أ����浽�ļ�-------------------
def print_weight(save_file):
    print "��ӡ��Ȩ��"
    f=open(save_file,'w')
    for u,v,edgedata in G.edges(data=True):
        d=int(edgedata['weight'])
        s=''.join([str(u),str(G.node[u]['word_property']),'_',str(v),\
                    str(G.node[v]['word_property']),':',str(d),'\n'])
        f.write(s)
    f.close()

#----����ƽ���ȷֲ�----------------
def print_average_degree():
    degree = nx.degree_histogram(G)#����ͼ�����нڵ�Ķȷֲ�����
    degree_sum = 0
    i=0
    for d in degree:
        degree_sum =degree_sum + d*i
        i=i+1
    return float(degree_sum)/float(G.number_of_nodes())  #ƽ���ȷֲ�

#----���ȷֲ�---------------------
def print_node_degree(save_file):
    f=open(save_file,'w')
    d=G.degree()
    for node in G.nodes():
        f.write(node+G.node[node]['word_property']+':'+str(d[node])+'\n')
    f.close()

#----ͼֱ��-----------------
def diameter(G):     #����ͼG��ֱ��������·���ĳ��ȣ�
    return nx.diameter(G)

#----ƽ�����·��-----------------
def average_shortest_path(G):  #����ͼG���нڵ��ƽ�����·������   
    return nx.average_shortest_path_length(G)

#----������ͼ��-----------------
def connected_subgraphs(G):
    if is_directed(G):   #�ж��Ƿ�����ͼ
        scc=nx.strongly_connected_component_subgraphs(G)#����ǿ��ͨ��ͼ��list
        wcc=nx.weakly_connected_components(G)#��������ͨ��ͼ��list
        i=0
        for nn in scc:
            i=i+1
            print '��',i,'��ͨ������ ','������',nn.number_of_edges(),'  �������',nn.number_of_nodes()
    else:
        print '��ͨ��������',nx.number_connected_components(G)    #��ͨ������Ŀ
        #nx.connected_components(G)    #��ȡ��ͨ�����Ľڵ��б�����ÿ����ͨͼ�Ľڵ��б�
        cc=nx.connected_component_subgraphs(G)#��ȡ��ͨ���������ص����б�
            #����Ԫ����ͼ����Щ�������սڵ���Ŀ�Ӵ�С���У����Ե�һ������������ͨ����
                #�����
        i=0
        for nn in cc:
            i=i+1
            print '��',i,'��ͨ������ ','������',nn.number_of_edges(),'  �������',nn.number_of_nodes()

#----�����������------------
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

