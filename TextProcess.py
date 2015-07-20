# -*- coding: gb2312 -*-
'''
-----------------------------------------------  
 WordCoNetwork: word co-occurrence network  
 Author : Zhang Hailong
 Date   : 2015-02-13
 HomePage : http://
 Email  : purplehero3@qq.com
-----------------------------------------------
'''
import re

#---- open file ---------------------
def open_file(input_file):
    f=open(input_file,'r')
    my_file=f.readlines()
    f.close()
    return my_file

#----�ı�Ԥ����-----------------------------
def Preprocessing(file_name,withstopwords):
    corpus=open_file(file_name)
    stopword=open_file('stopwords.txt')
    wordlists = []
    for paragraph in corpus:
        paragraph = paragraph.split(',')
        for word in paragraph:
            if re.findall('/',word):  #ȥ���޷���ע���Ե�������
                unit = word.split('/')[0].strip()
                if unit !='':    #ȥ���մʱ�ע�Ϳ���
                    if withstopwords = 0:
                        if unit+'\n' not in stopword:    #ȥ��ͣ�ô�
                            wordlists.append(unit.strip())
                    else:
                        wordlists.append(unit.strip())
    return wordlists
