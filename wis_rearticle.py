#!/usr/bin/env python
# -*- coding: utf8 -*-

import MySQLdb
import nltk

db=MySQLdb.connect("localhost","root","nukimresearch212","Research",charset='utf8')
cursor=db.cursor()

#詞幹還原
def word_stem(word):
	word_len = len(word)
	suffix = word[word_len-3:word_len]

	sql_stemmerselect = "SELECT irregular_word,stemmer FROM Stemmer"
	cursor.execute(sql_stemmerselect)
	stemmer_words = cursor.fetchall()

	stemmer_dict = {}
	for stemmer_word in stemmer_words:
	        irregular_word = stemmer_word[0]
        	stemmer = stemmer_word[1]

	        stemmer_dict[irregular_word] = stemmer

	if word in stemmer_dict:
        	return stemmer_dict[word]

	elif suffix=="ied":
        	return word[0:word_len-3]+"y"

	elif suffix=="ies":
        	return word[0:word_len-3]+"y"

	elif suffix=="oes":
        	return word[0:word_len-3]+"o"

	else:
		porter = nltk.PorterStemmer()
        	return porter.stem(word)

#相關資訊輸入
def wis(x,left_first,left_end,right_first,right_end,student_id,class_level,class_name,homework_item):

	left_sentence = ""
        right_sentence = ""

	#article_postag[x][0]為單字，article_postag[x][1]為該單字的詞性
	#例:[(Tom,N),(jump,V)]。
        word = article_postag[x][0]
        word_postag = article_postag[x][1]


        print word,word_postag,word_stem(word)

	#找出左右句子
        for w in article_postag[left_first:left_end]:
        	left_sentence = left_sentence+w[0]+" "
        for w in article_postag[right_first:right_end]:
        	right_sentence = right_sentence+w[0]+" "

	print left_sentence,word,right_sentence

        sql="INSERT INTO Word_sentence (class_level,class_name,homework_item,student_ID,word,word_postag,word_stem,left_sentence,right_sentence) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(class_level,class_name,homework_item,student_id,word,word_postag,word_stem(word),left_sentence,right_sentence)
        cursor.execute(sql)
	db.commit()


#判斷是否處理過
sql_finished = "SELECT wis_finished,file_Name FROM Article"
cursor.execute(sql_finished)
finished_result = cursor.fetchall()

for finished_status in finished_result:

	finished_value = finished_status[0]
	finished_pri   = finished_status[1]

	if finished_value == None:

		sql_selectarticle = "SELECT Article,student_ID,class_level,class_name,homework_item FROM Article WHERE file_Name =%d" %(finished_pri)
		cursor.execute(sql_selectarticle)
		selectarticle_result = cursor.fetchone()

		article       = selectarticle_result[0]
		student_id    = selectarticle_result[1]
		class_level   = selectarticle_result[2]
		class_name    = selectarticle_result[3]
		homework_item = selectarticle_result[4]

		#文章正規化，將符號以前後空白隔開，split用
		re_article = (article.encode('utf8').replace("."," . ").replace("!"," ! ").replace("?"," ? ").replace(","," , ").replace(";"," ; ")
			      .replace(":"," : ").replace("("," ( ").replace(")"," ) ").replace("["," [ ").replace("]"," ] ").replace("{"," { ")
			      .replace("}"," } ").replace('"',' " ').replace("-"," - ").replace("'","’").decode('utf8').split())
	
		#詞性標註
		article_postag = nltk.pos_tag(re_article)

		article_len = len(article_postag)

		#判斷方式是取得單字的前10個及後10個單字的位置
		for x in range(0,article_len):

			#如果搜尋到的單字是標點符號則跳過
			if article_postag[x][0] in ".!?,;:()[]{}-\"\'":
				continue

			#如果單字是開頭或結尾，會湊不滿前或後10個單字的條件，所以加入判斷。
			else:
				if x<9:
					wis(x,0,x,(x+1),(x+11),student_id,class_level,class_name,homework_item)

				elif x>len(article_postag)-11:
					wis(x,(x-10),x,x+1,article_len,student_id,class_level,class_name,homework_item)

				else:
					wis(x,(x-10),x,(x+1),(x+10),student_id,class_level,class_name,homework_item)

	#處理完後，將finished的欄位標示為done
	sql_done = "UPDATE Article SET wis_finished = '%s' WHERE file_Name = '%d'" %("done",finished_pri)
	cursor.execute(sql_done)
        db.commit()
