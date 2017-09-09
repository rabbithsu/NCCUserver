#!/usr/bin/python	
#encoding: utf-8 
import MySQLdb,os,sys
import time




def update_timestamp():
	stamp= time.strftime("%Y-%m-%d %H:%M:%S");
	#UPDATE `dashboard` SET `time`="0.0" WHERE `Module`="uploadnews"
	
	query_sting="UPDATE `dashboard` SET `time`=\'"+stamp+"\' WHERE `Module`= \'uploadnews\'";
	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Stock",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()

def clear_db():
	
	query_sting="TRUNCATE TABLE `predict`";
	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Stock",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()


def upload_to_db(nid,date,result):

	#query_sting="INSERT INTO `news` (`id`, `date`, `title`, `content`) VALUES ('台股', '台股', '台股', '台股')";	
	#query_sting="INSERT INTO `news` (`id`, `date`, `title`, `content`) VALUES ('a', 'b', 'c', 'd')";	
	query_sting="INSERT INTO `predict` (`id`, `date`, `result`) VALUES (\'"+nid+"\',\'"+date+"\',\'"+result+"\')";
	#print query_sting

	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Stock",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()

def if_in_db(date):
	query_sting="SELECT * FROM predict WHERE date = "+date

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

def read_id(file_name):
	with open(file_name, "r") as text:
	    ID = []
	    for line in text:
	    	line=line.rstrip()
	        ID.append(line)
	    return ID
	
def write_upload_list(tmp):
	IO = open("upload.tmp", 'w');
	IO.write(tmp);
	IO.close();

def get_file(Day):
	tmp="";
	#upload_list=read_upload_list();
	if if_in_db(Day):
		return
	ID=read_id("ID.csv")


	try:
		

		print Day

		IO = open("./merge/"+Day[0:4]+"/"+str(int(Day[4:6]))+"/"+Day+".txt", 'r');
		for n in IO.readlines():
			m = n.split("\t")

			if(m[0].replace('\xef\xbb\xbf', '') not in ID):
				#	print m
				continue
			else:
				print m
			if(m[1] == "Positive"):
				re = "1"
			else:
				re = "0"
			upload_to_db(m[0].replace('\xef\xbb\xbf', ''), Day, re);
			#content = IO.read();
		IO.close();
			#print content;
	except Exception, e: 
		print str(e)
		print sys.exc_info()

	#print "tmp : "+str(tmp);


toDay= time.strftime("%Y%m%d")
get_file(toDay);

#clear_db();

'''for i in range(0,30):
	toDay = 20161101+i
	get_file(str(toDay));'''


#get_file("20160303");
#update_timestamp();

print "Upload Finished!"
