#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from time import sleep
import time
import json
import sys
import MySQLdb
import math
import os
from datetime import date, timedelta

#CH
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

## 這是測試

def update_timestamp():
	stamp= time.strftime("%Y-%m-%d %H:%M:%S");
	#UPDATE `dashboard` SET `time`="0.0" WHERE `Module`="uploadnews"
	
	query_sting="UPDATE `dashboard` SET `time`=\'"+stamp+"\' WHERE `Module`= \'price\'";
	db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="news",charset="utf8")	
	cursor = db.cursor()

	result=cursor.execute(query_sting);
	result = cursor.fetchall()
	db.commit()

	cursor.close()
	db.close()

def crawler(text):
	ID=text.split(",")[0];
	name=text.split(",")[1];
	print "ID : "+str(ID);

	links ='http://finance.google.com/finance/info?client=ig&q=TPE:'+str(ID)
	#links ='http://finance.google.com/finance/info?client=ig&q=TPE:2454'
	#print links
	

	res = requests.get(links)
	#print res

	json_file=res.text

	for char in ['//','[',']']:
		json_file=json_file.replace(char,'')

	#print json_file
	
	try:

		info=json.loads(json_file)

		'''
		print info["t"]
		print info["l_fix"]
		print info["lt_dts"][:10]
		print info["c_fix"]
		'''
		#print info["lt_dts"][0:4]+info["lt_dts"][5:7]+info["lt_dts"][8:10]+','+info["t"]+','+str(name)+','+info["l_fix"]
		return info["lt_dts"][0:4]+info["lt_dts"][5:7]+info["lt_dts"][8:10]+','+info["t"]+','+str(name)+','+info["l_fix"]
		#return info["t"]+',None,'+info["lt_dts"][0:4]+info["lt_dts"][5:7]+info["lt_dts"][8:10]+','+info["pcls_fix"]
	except:
		print "Error ID : "+str(text)
		return "Error";
	
def read_id():
	yesterday = "20" + (date.today() - timedelta(1)).strftime('%y%m%d')
	with open("./stockReturn/tej/"+yesterday[0:4]+"/"+yesterday+".txt", "r") as text:
	    ID = []
	    for line in text:
	    	line=line.rstrip()
	        ID.append(line)
	    return ID

def output_csv(file_name,text):
	#f=file(file_name,"w")
	if not os.path.exists("stockReturn/tej/"+ file_name[0:4]):
		os.makedirs("stockReturn/tej/"+ file_name[0:4])
	
	f = open("stockReturn/tej/"+ file_name[0:4] +'/'+ file_name, "w")

	for line in text:
		try:
			if(line is None):
				print "Error : line is None Type"
			else:
				f.write(line+"\n")
				#print line;
		except:
			print "Error : output_csv "+line
	
	f.close

def process():
	#ID=read_id("ID_all.csv")
	#ID=read_id("priceinfo.txt")
	ID=read_id()
	#print ID	

	
	Price=[]
	#Price.append("ID,name,date,price")
	#CSV header


	#i=0
	for id in ID:
		info = id.replace("\t"," ").split(' ')
		info = filter(None, info)
		print info
		result = crawler(info[1]+","+info[2]).split(",")
		if result[0] == "Error":
			continue
		else:
			ln = math.log(float(result[3])/float(info[8]), math.e)
			Price.append(result[0]+" "+result[1]+" "+result[2]+" "+ str(ln) +" "+info[4]+" "+info[5]+" "+info[6]+" "+info[7]+ " "+result[3])
		#sleep(0.05) #50ms
		sleep(1) #1s
		#sleep(0.1)
		#print str(id)+'/'+str(len(ID))
		#i=i+1


	#file_name="google_api_"+str(time.localtime().tm_mon)+'_'+str(time.localtime().tm_mday)+'_'+str(time.localtime().tm_hour)+'_'+str(time.localtime().tm_min)
	#file_name=str(time.localtime().tm_year)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+".txt"
	file_name=time.strftime("%Y%m%d")+".txt"
	output_csv(file_name,Price)
	
#print "/-----------google api-----------/"

process();
#update_timestamp();

#print "/*_*_*_*_*_*_*_*_*_*_*_*_*_/"

print "Upload Finished!"



