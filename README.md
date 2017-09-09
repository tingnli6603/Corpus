學生文本語料庫
===
研究目的是將蒐集來的學生文本，建置成一個語料庫網站，供老師研究使用。功能包括搜尋單一字詞，了解學生搭配字詞情形，並統計出該單字最常出現的搭配字；搜尋單一字詞，了解學生前後句子如何使用；統計學生最常使用之片語，範圍為2到6字片語。搜尋時可以搜尋該單字的所有變化形態，或者是只搜尋該單字的某一詞性。

文章處理－搭配詞及前後句
---
kwic_rearticle.py、wis_rearticle.py

將所有文本做斷詞，使用nltk套件的porter套件以及特殊字元過濾將每一個單字做詞幹還原；用nltk套件的pos_tag標註每個單字的詞性。詞幹還原以及詞性標註是用於增加搜尋條件。最後再抓取該單字的前後三個單字或前後句存入資料庫內。

N-gram
---
n_gram.py

N-gram用於統計文本單中最常被使用的片語，片語的字數分2字至6字。方法是使用Python的Dictionary做類似斷詞的動作，將文章以每兩字等方式切割開，並統計該片語的次數，最後依照次數多寡排序。

網站內容
---
首頁-單字搜尋
---
![image](https://github.com/tingnli6603/Corpus/blob/master/WebImg/search.png)
前後搭配詞
---
![image](https://github.com/tingnli6603/Corpus/blob/master/WebImg/word.png)

搭配詞統計
---
![image](https://github.com/tingnli6603/Corpus/blob/master/WebImg/word_freq.png)

單字前後句
---
![image](https://github.com/tingnli6603/Corpus/blob/master/WebImg/sentence.png)

N gram搜尋
---
![image](https://github.com/tingnli6603/Corpus/blob/master/WebImg/ngramsearch.png)

N gran結果
---
![image](https://github.com/tingnli6603/Corpus/blob/master/WebImg/ngram.png)
