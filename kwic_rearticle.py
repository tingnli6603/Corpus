#!/usr/bin/env python
# -*- coding: utf8 -*-

import MySQLdb
import re
import nltk

db=MySQLdb.connect("localhost","root","nukimresearch212","Research",charset='utf8')
cursor=db.cursor()

#將單字還原成詞幹。例:goes=>go，went=>go。
#用於搜尋單字的各種變化形態。例:搜尋go就可以搜尋到went及goes等。
#如果使用nltk中的porter做詞幹還原，會有些特殊單字無法還原。
#詞幹還原順序:不規則變化(辭庫)>特殊結尾(ied、ies、oes)>porter
def word_stem(word):
        word_len = len(word)
	#取得單字的結尾最後三個單字
        suffix = word[word_len-3:word_len]

	#搜尋特殊變化辭庫
        sql_stemmerselect = "SELECT irregular_word,stemmer FROM Stemmer"
        cursor.execute(sql_stemmerselect)
        stemmer_words = cursor.fetchall()

	#將不規則辭庫存成dict。key是不規則單字，value是詞幹。
        stemmer_dict = {}
        for stemmer_word in stemmer_words:
                irregular_word = stemmer_word[0]
                stemmer = stemmer_word[1]

                stemmer_dict[irregular_word] = stemmer

        if word in stemmer_dict:
                return stemmer_dict[word]

	#將特殊結尾還原
        elif suffix=="ied":
                return word[0:word_len-3]+"y"

        elif suffix=="ies":
                return word[0:word_len-3]+"y"

        elif suffix=="oes":
                return word[0:word_len-3]+"o"

	#最後用詞幹還原套件porter
        else:
                porter = nltk.PorterStemmer()
                return porter.stem(word)

#將相關資料存入資料庫
def KWIC(class_level,class_name,homework_item,student_id,word,word_postag,L3,L2,L1,R1,R2,R3):

        print word,word_postag,word_stem(word)
        print L3,L2,L1,'"'+word+'"',R1,R2,R3

        sql="INSERT INTO KWIC (class_level,class_name,homework_item,student_ID,word,word_postag,word_stem,L3,L2,L1,R1,R2,R3) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(class_level,class_name,homework_item,student_id,word,word_postag,word_stem(word),L3,L2,L1,R1,R2,R3)
        cursor.execute(sql)
        db.commit()

#判斷該篇文章是否已經處理過
sql_finished = "SELECT kwic_finished,file_Name FROM Article"
cursor.execute(sql_finished)
finished_result = cursor.fetchall()


for finished_status in finished_result:

        finished_value = finished_status[0]
        finished_pri   = finished_status[1]

	#如果文章尚未處理過才執行
        if finished_value == None:

		sql_selectarticle = "SELECT Article,student_ID,class_level,class_name,homework_item FROM Article WHERE file_Name =%d" %(finished_pri)
                cursor.execute(sql_selectarticle)
                selectarticle_result = cursor.fetchone()

                article       = selectarticle_result[0]
                student_id    = selectarticle_result[1]
		class_level   = selectarticle_result[2]
		class_name    = selectarticle_result[3]
		homework_item = selectarticle_result[4]

		#將文章正規化
		re_article = re.sub("[.!?,;:\(\)\[\]\{\}\'\"\-]"," ",article).split()

		#將每一個單字做詞性標註
		article_postag = nltk.pos_tag(re_article)

                article_len = len(article_postag)

		#如果單字位置是0，則不會有L3、L2、L1的單字。以此類推
		for x in range(0,article_len):

			if x==0:
				KWIC(class_level,class_name,homework_item,student_id,article_postag[0][0],article_postag[0][1],"","","",article_postag[1][0],article_postag[2][0],article_postag[3][0])

			elif x==1:
				KWIC(class_level,class_name,homework_item,student_id,article_postag[1][0],article_postag[1][1],"","",article_postag[0][0],article_postag[2][0],article_postag[3][0],article_postag[4][0])

			elif x==2:
				KWIC(class_level,class_name,homework_item,student_id,article_postag[2][0],article_postag[2][1],"",article_postag[0][0],article_postag[1][0],article_postag[3][0],article_postag[4][0],article_postag[5][0])

			elif x==len(article_postag)-3:
				KWIC(class_level,class_name,homework_item,student_id,article_postag[x][0],article_postag[x][1],article_postag[(x-3)][0],article_postag[(x-2)][0],article_postag[(x-1)][0],article_postag[(x+1)][0],article_postag[(x+2)][0],"")

			elif x==len(article_postag)-2:
				KWIC(class_level,class_name,homework_item,student_id,article_postag[x][0],article_postag[x][1],article_postag[(x-3)][0],article_postag[(x-2)][0],article_postag[(x-1)][0],article_postag[(x+1)][0],"","")

			elif x==len(article_postag)-1:
				KWIC(class_level,class_name,homework_item,student_id,article_postag[x][0],article_postag[x][1],article_postag[(x-3)][0],article_postag[(x-2)][0],article_postag[(x-1)][0],"","","")

			else:
				KWIC(class_level,class_name,homework_item,student_id,article_postag[x][0],article_postag[x][1],article_postag[(x-3)][0],article_postag[(x-2)][0],article_postag[(x-1)][0],article_postag[(x+1)][0],article_postag[(x+2)][0],article_postag[(x+3)][0])

		#文章處理完，finished的欄位標示done
		sql_done = "UPDATE Article SET kwic_finished = '%s' WHERE file_Name = '%d'" %("done",finished_pri)
        	cursor.execute(sql_done)
        	db.commit()
