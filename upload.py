#!/usr/bin/python    
#-*- coding: utf-8 -*-
import MySQLdb,os,sys
import time




def update_timestamp():
	stamp= time.strftime("%Y-%m-%d %H:%M:%S");
	#UPDATE `dashboard` SET `time`="0.0" WHERE `Module`="uploadnews"
	
	query_sting="UPDATE `dashboard` SET `time`=\'"+stamp+"\' WHERE `Module`= \'uploadnews\'";
	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="news",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()

def clear_db():
	
	query_sting="TRUNCATE TABLE `news`";
	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="news",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()


def upload_to_db(date,newsTitle,stockID,content):

	#query_sting="INSERT INTO `news` (`id`, `date`, `title`, `content`) VALUES ('台股', '台股', '台股', '台股')";	
	#query_sting="INSERT INTO `news` (`id`, `date`, `title`, `content`) VALUES ('a', 'b', 'c', 'd')";	
	query_sting="INSERT INTO `news` (`id`, `date`, `title`, `content`) VALUES (\'"+stockID+"\',\'"+date+"\',\'"+newsTitle+"\',\'"+content+"\')";
	#print query_sting

	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Stock",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()

def if_in_db(date):
	query_sting="SELECT * FROM news WHERE date = "+date

	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Stock",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	if not cursor.rowcount:
		print "No results found"
		return False
	else:
		print "get"
		return True 
	db.commit()

	cursor.close()
	db.close()

def read_upload_list():

	IO = open("upload.tmp", 'r');
	tmp = IO.read();
        IO.close();
	#print tmp;
	return tmp;
	
def write_upload_list(tmp):
	IO = open("upload.tmp", 'w');
	IO.write(tmp);
	IO.close();

def get_file(Day):
	#tmp="";
	#upload_list=read_upload_list();
	if if_in_db(Day):
		return

	newsList = os.listdir("news/"+Day[0:4]+ "/"+ Day[4:6]+ '/' + Day); 
	#print newsList;
	
	for newsFile in newsList:
		#print newsFile;

		try:
			
			news_path=newsFile;
			newsFile=newsFile.replace('.txt','');
			newsFile=newsFile.replace('][','##');
			newsFile=newsFile.replace('[2','2');	
			newsFile=newsFile.replace(']','');
			#print newsFile
			
			date=newsFile.split("##")[0]; 
			newsTitle = newsFile.split("##")[1]; 
		        stockID = newsFile.split("##")[2];
			print date+" / "+newsTitle+" / "+stockID;

			IO = open("./news/"+Day[0:4]+"/"+Day[4:6] + '/'+ Day+'/' + news_path, 'r');
			content = IO.read();
		        IO.close();
			#print content;

			
			#if newsTitle in upload_list:
			#	print "already_upload !";
			
			#else:
			upload_to_db(date,newsTitle,stockID,content);
			#tmp=tmp+newsTitle;
			'''
			upload_to_db(date,newsTitle,stockID,content);
			tmp=tmp+newsTitle;
			'''
		except Exception, e: 
			print str(e)
			print "Error in news file !";
			#continue;
	#tmp=tmp+upload_list;
	#write_upload_list(tmp);
	#print "tmp : "+str(tmp);

#toDay="20161102"
toDay= time.strftime("%Y%m%d")
get_file(toDay);

#clear_db();
'''for i in range(0,30):
	toDay = 20161101+i
	get_file(str(toDay));'''


#update_timestamp();

print "Upload Finished!"
