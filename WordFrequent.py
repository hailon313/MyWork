# -*- coding: gb2312 -*-
'''
-----------------------------------------------  
 WordFrequent: word frequent  
 Author : Zhang HaiLong  
 Date   : 2015-05-18  
 HomePage : http://
 Email  : purplehero3@qq.com
-----------------------------------------------
'''
import networkx as nx
from WordCoNetwork import Creat_Graph_Net
from TextProcess import Preprocessing
from TextProcess import open_file

#----����Apriori��Ƶ��ģʽ�ھ�---------------------
def frequent_pattern(G,pre_text,f1,f2):
    frequent1 = []#Ƶ��1-�
    frequent2 = []#Ƶ��2-�
    frequent3 = []#Ƶ��k-�
    frequent_all = []#����Ƶ���
    source_text=''.join(pre_text)
    #---------
    for node in G.nodes():   #1Ƶ��ģʽ
        m=G.node[node]['word_frequency']
        if m>f1 and len(node)>2:
            frequent1.append(([str(node)],m))
    #----------
    for node1,node2,edgedata in G.edges(data=True):  #2Ƶ��ģʽ
        d=int(edgedata['weight'])
        if d > f2:
            frequent2.append(([str(node1),str(node2)],d))
    frequent_all.append(frequent1)
    frequent_all.append(frequent2)
    #-----------
    for i in range(1,100):    #kƵ��ģʽ
        L=len(frequent_all[i])
        frequentk =[]
        for double in frequent_all[i]:
            for j in range(0,L):
                if double[0][1:] == frequent_all[i][j][0][:-1]:
                    string = ''.join(double[0])+str(frequent_all[i][j][0][-1])
                    counter = source_text.count(string)
                    if counter > f2:
                        teamp = [] #��ʱ
                        teamp.extend(double[0])
                        teamp.append(frequent_all[i][j][0][-1])
                        frequentk.append((teamp,counter))
                        #f.write(' '.join(double)+' '+str(frequent_all[i][j][-1])+' '+str(counter)+'\n')
        if frequentk == []:
            break
        else:
            frequent_all.append(frequentk)
    return frequent_all

#----���ڴʹ��������Ƶ���������ȡ-------------------------------
def frequent_pattern1(G,pre_text,threshold,save_file):
    fw = open(save_file,'a')
    list_len=len(pre_text)
    continuous = 0
    words = []
    string = ''
    fw.write('##begin'+'\n')  
    for i in range(0,list_len-1):         #���ж����ļ�����ȡ�������
        u=pre_text[i].split('/')[0]
        v=pre_text[i+1].split('/')[0]
        if((u == '��') or (v == '��') or (u==v)):
            #�����ǰ�ʻ�����һ����Ϊ����򲻴���
            if continuous != 0:
                words.append(string)
                continuous = 0
            continue
        if G.get_edge_data(u,v):
            w=G.get_edge_data(u,v)['weight']
            if w>threshold:
                if continuous == 0:
                    string = str(u)+' '+str(v)
                else:
                    string = string+' '+str(v)
                continuous = continuous+1
            elif continuous != 0:
                if string not in words:
                    words.append(string)
                continuous = 0
    for word in words:
        fw.write(word+'\n')
    fw.write('##end'+'\n')
    fw.close()

#----ɾ���ظ���------------------
def repeat_eliminate(input_file,output_file):#set����
    fr=open(input_file,'r')
    word=fr.readlines()
    fr.close()
    word_list=[]
    fw=open(output_file,'w')
    for ww in word:
        if ww not in word_list:
            fw.write(ww)
            word_list.append(ww)

#----���Ŷ�-------------
def confidence(G,threshold,con):
    for u,v,edgedata in G.edges(data=True):  #ɾ��Ȩ��С�ڷ�ֵ�ı�
        d=int(edgedata['weight'])
        if d <threshold:
            G.remove_edge(u,v)
        else:
            m=float(G.node[u]['word_frequency'])
            if float(d)/m < con:
                G.remove_edge(u,v)
    for node in G.nodes():    #ɾ����Ϊ��Ľ��
        if G.degree(node) == 0:
            G.remove_node(node)
    return G

#----Ƶ����ϲ�------------------
def frequent_merge(frequent_list):
    L = len(frequent_list)
    freq = []
    for i in range(1,L):
        temp = []
        string_list = []
        for j in range(len(frequent_list[i])):
            string_list.append(''.join(frequent_list[i][j][0]))
        #for ss in range(len(string_list)):
            #print string_list[ss]
        for k in range(len(frequent_list[i-1])):
            mm = 0
            for q in range(len(string_list)):
                if ''.join(frequent_list[i-1][k][0]) in string_list[q]:
                    mm = 1
                    break
            if mm == 0:
                temp.append(frequent_list[i-1][k])
                #print temp
                #print ''.join(frequent_list[i-1][k])
        temp.sort(key=lambda d:d[1],reverse=True)
        freq.append(temp)
    frequent_list[-1].sort(key=lambda d:d[1],reverse=True)
    freq.append(frequent_list[-1])
    return freq

#----Ƶ��ģʽ������ı�-------------
def print_frequent(freq,paper_numb,save_file):
    ff=open(save_file,'a')
    ff.write('#----paper '+str(paper_numb)+' begin------'+'\n')

    L = len(freq)
    for i in range(0,L):    
        if freq[i] != []:
            ff.write('# '+str(i+1)+' frequent'+'\n')
            for node in freq[i]:
                ff.write('['+' '.join(node[0])+']'+str(node[1])+'/')
            ff.write('\n')
    ff.write('# end'+'\n')
    ff.close()

#----�ʴ�����----------------
def word_tape(freq):
    L = len(freq)
    node_list = []
    for i in range(0,L):
        for node in freq[i]:
            node_list.extend(node[0])
    return node_list

#----�ؼ�����ȡ------------------
def keywords():
    corpus=open_file('out2.txt','r')
    wordsss = []#�ʵ�
    word_vector=[]
    paper_numb = 1#���±��
    for paragraph in corpus:
        pre_text = Preprocessing(paragraph,0)
        G=Creat_Graph_Net(pre_text)
        #print_number_of_nodes_edges(G)
        frequent_all = frequent_pattern(G,pre_text,3,2)  #����Ƶ����
        frequent_m = frequent_merge(frequent_all)#  Ƶ����ϲ�
        print_frequent(frequent_m,paper_numb,'888.txt')
        #words = word_tape(frequent_m)  #�ʴ�����
        wt = word_tape(frequent_m)
        wordsss.extend(wt)
        #print len(wordsss)
        #break
        paper_numb = paper_numb+1
    wordsss = list(set(wordsss)) # ���մʴ�
    print len(wordsss)
    print paper_numb

#----main--------------
if __name__ == '__main__':
    keywords()



