#!/usr/bin/env python
# -*- coding: utf8 -*-

#統計所選擇的文章中，片語出現的次數以及排序
#參考:http://hambao.pixnet.net/blog/post/18823664-python%E7%AD%86%E8%A8%98%EF%BC%9A%E7%94%A2%E7%94%9Fn-gram%E4%BB%A5%E5%8F%8A%E7%B0%A1%E5%96%AE%E9%A0%BB%E7%8E%87%E7%B5%B1%E8%A8%88
import sys
import re
import MySQLdb
from operator import itemgetter

db=MySQLdb.connect("localhost","root","nukimresearch212","Research",charset='utf8')
cursor=db.cursor()

#條件選擇。幾字片語、班級等級、班級、作業項目。
select_num   = int(sys.argv[1])
select_level = sys.argv[2]
select_class = sys.argv[3]
select_homeworkitem = sys.argv[4]

#條件判斷
all_article = ""
if select_level =="all":
	if select_class =="all":
		if select_homeworkitem =="all":
			sql_allallall = "SELECT Article FROM Article"
			cursor.execute(sql_allallall)
			result_allallall = cursor.fetchall()

			for article in result_allallall:
				all_article = all_article+article[0]

		else:
			sql_allall0 = "SELECT Article FROM Article WHERE homework_item='%s'" %(select_homeworkitem)
			cursor.execute(sql_allall0)
			result_allall0 = cursor.fetchall()

			for article in result_allall0:
                                all_article = all_article+article[0]

	else:
		if select_homeworkitem =="all":
			sql_all0all = "SELECT Article FROM Article WHERE class_name='%s' " %(select_class)
			cursor.execute(sql_all0all)
			result_all0all= cursor.fetchall()

			for article in result_all0all:
				all_article = all_article+article[0]

		else:
			sql_all00 = "SELECT Article FROM Article WHERE class_name ='%s' AND homework_item='%s' " %(select_class,select_homeworkitem)
                        cursor.execute(sql_all00)
                        result_all00= cursor.fetchall()

                        for article in result_all00:
                                all_article = all_article+article[0]

else:
        if select_class =="all":
		if select_homeworkitem =="all":
			sql_0allall = "SELECT Article FROM Article WHERE class_level ='%s' " %(select_level)
                        cursor.execute(sql_0allall)
                        result_0allall = cursor.fetchall()

                        for article in result_0allall:
                                all_article = all_article+article[0]
                else:
			sql_0all0 = "SELECT Article FROM Article WHERE class_level ='%s' AND homework_item='%s' " %(select_level,select_homeworkitem)
                        cursor.execute(sql_0all0)
                        result_0all0 = cursor.fetchall()

                        for article in result_0all0:
                                all_article = all_article+article[0]
        else:		
		if select_homeworkitem =="all":
			sql_00all = "SELECT Article FROM Article WHERE class_level ='%s' AND class_name='%s' " %(select_level,select_class)
                        cursor.execute(sql_00all)
                        result_00all = cursor.fetchall()

                        for article in result_00all:
                                all_article = all_article+article[0]

                else:
			sql_000 = "SELECT Article FROM Article WHERE class_level ='%s' AND class_name='%s' AND homework_item='%s'" %(select_level,select_class,select_homeworkitem)
                        cursor.execute(sql_000)
                        result_000 = cursor.fetchall()

                        for article in result_000:
                                all_article = all_article+article[0]


#文章正規化
re_article = re.sub("[.!?,;:\(\)\[\]\{\}\'\"\-]"," ",all_article).split()

#將文章依照選擇的片語單字數下去切割
#假如100字的文章，3字片語。切割就是123、234、345...。
#len(mylist)-(select_num-1)=>如果單字片語是3字，那最後兩字無法形成片語，所以就取到倒數第三字
def list2Ngram(mylist):
	return [mylist[i:(i+select_num)] for i in range(0,len(mylist)-(select_num-1))]

chNgram = list2Ngram(re_article)

#用chX去存片語中的單字
#get是dictionary的方法。get(key,value)，如果dict中沒有key，則回傳value，有則執行後面的方法
#以下是如果沒有(ch1,ch2)的片語，值為0，然後+1。如果已經存在，則直接+1。
def Ngram2freqdict(myNgram):
	mydict = dict()
	if select_num==2:
		for (ch1,ch2) in myNgram:
			mydict[(ch1,ch2)] = mydict.get((ch1,ch2),0)+1
	elif select_num==3:
		for (ch1,ch2,ch3) in myNgram:
                        mydict[(ch1,ch2,ch3)] = mydict.get((ch1,ch2,ch3),0)+1
	elif select_num==4:
		for (ch1,ch2,ch3,ch4) in myNgram:
                        mydict[(ch1,ch2,ch3,ch4)] = mydict.get((ch1,ch2,ch3,ch4),0)+1
	elif select_num==5:
		for (ch1,ch2,ch3,ch4,ch5) in myNgram:
                        mydict[(ch1,ch2,ch3,ch4,ch5)] = mydict.get((ch1,ch2,ch3,ch4,ch5),0)+1
	elif select_num==6:
                for (ch1,ch2,ch3,ch4,ch5,ch6) in myNgram:
                        mydict[(ch1,ch2,ch3,ch4,ch5,ch6)] = mydict.get((ch1,ch2,ch3,ch4,ch5,ch6),0)+1

	return mydict

Ngramfreqdict = Ngram2freqdict(chNgram)

#將片語依照出現次數排序
Ngramfreqsorted = sorted(Ngramfreqdict.items(), key=itemgetter(1), reverse=True)

#印出所有片語以及該片語出現次數
num = 0
for sentence_freq in Ngramfreqsorted:
	num=num+1

	sentence = ""
	for x in range(0,select_num):
		sentence = sentence + sentence_freq[0][x] +" "
	freq = sentence_freq[1]
	print num,sentence,freq
