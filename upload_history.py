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
	
	query_sting="TRUNCATE TABLE `history`";
	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Stock",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()


def upload_to_db(nid,ordi,date,price,result):

	#query_sting="INSERT INTO `news` (`id`, `date`, `title`, `content`) VALUES ('台股', '台股', '台股', '台股')";	
	#query_sting="INSERT INTO `news` (`id`, `date`, `title`, `content`) VALUES ('a', 'b', 'c', 'd')";	
	query_sting="INSERT INTO `history` (`id`, `ord`, `date`, `price`, `result`) VALUES (\'"+nid+"\',\'"+ordi+"\',\'"+date+"\',\'"+price+"\',\'"+result+"\')";
	#print query_sting

	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Stock",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()

def if_in_db(date):
	query_sting="SELECT * FROM history WHERE date = "+date

	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="Stock",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	if not cursor.rowcount:
		print "No results found"
		return False
	else:
		print "Already"
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
	if if_in_db(Day):
		return False
	tmp="";
	#upload_list=read_upload_list();

	#newsList = os.listdir('./stockReturn/tej/'+Day[0:4]); 
	#print newsList;
	
	#for newsFile in newsList:
		#print newsFile;

	try:

		Hdata =[]
		HIO = open("./merge/"+Day[0:4]+"/"+str(int(Day[4:6]))+"/"+Day+".txt", 'r');
		for nn in HIO.readlines():
			mm = nn.split("\t")


			if(mm[1] == "Positive"):
				hre = "1"
			else:
				hre = "0"
			Hdata.append(mm[0].replace('\xef\xbb\xbf', ''));
			Hdata.append(hre);
			#content = IO.read();
		HIO.close();






		IO = open("./stockReturn/tej/"+Day[0:4]+'/'+Day+'.txt', 'r');
		for n in IO.readlines():
			m = n.split(" ")
			if(len(m) < 8):
				print m
				continue
			try:
				re = Hdata[Hdata.index(m[1])+1]
				upload_to_db(m[1], "0", Day, m[len(m)-1], re);
			except Exception, e: 
				print str(e)
				continue

		#content = IO.read();
		IO.close();
		#print content;
			
		'''if newsTitle in upload_list:
			print "already_upload !";
	
		else:
			upload_to_db(nid,ordi,date,price,result);
			tmp=tmp+newsTitle;'''
		'''
		upload_to_db(date,newsTitle,stockID,content);
		tmp=tmp+newsTitle;
		'''
	except Exception, e: 
		print str(e)
		print sys.exc_info()

	'''tmp=tmp+upload_list;
	write_upload_list(tmp);'''
	#print "tmp : "+str(tmp);

#toDay="20161118"
toDay= time.strftime("%Y%m%d")
get_file(toDay);

#clear_db();
'''for i in range(0,10):
	toDay = 20161121+i
	get_file(str(toDay));
'''

#get_file("20160303");
#update_timestamp();

print "Upload Finished!"
