import datetime, os, time;
from FileToList import FileToList as FileToList; #transfer file to list

rootFolder="";
pnvFolder = 'newsPNV/'; 
prepareFolder = 'prepareFile/'; 
financeFolder = 'financeReport/tej/'; 
stockFolder = 'stockReturn/tej/'; 
txtFolder = 'merge/';


thisYear = datetime.date.today().year;
thisMonth = datetime.date.today().month;
thisDay = datetime.date.today().day;

deltaDays = -1;
pnews = 0; 
nnews = 0; 
snews = 0; 
tcount = 0; 

def cleanSC(inString):
    outString = str(inString);
    outString = str(outString).rstrip(); 
    outString = str(outString).lstrip();
    outString = str(outString).replace('\ufeff','');
    outString = str(outString).replace('\n', '');
    return outString;

#global variables
f3v = {};
sr = {}; 
sp = {}; 
f5v = {}; 
coeff = {}; 
stockID = {}; 

def getCoefficient(): 
    coeff = {};
    IO = open(rootFolder + prepareFolder + 'coefficient.txt', mode = 'r');
    records = [];
    for record in IO:
        records = record.split('\t');    
    IO.close();
    coeff = {'c':cleanSC(records[0]), 'Pnews':cleanSC(records[1]), 'Nnews':cleanSC(records[2]), 'avgScore':cleanSC(records[3]), 'EPS':cleanSC(records[4]), 'ROA':cleanSC(records[5]), 'ROE':cleanSC(records[6]), 'BPS':cleanSC(records[7]), 'PB':cleanSC(records[8])};
    return coeff;

def getF3V(inDate): 
    f3v = {};
    whatYear = inDate[0:4];
    whatMonth = inDate[4:6];
    IO = open(rootFolder + pnvFolder + whatYear + '/' + whatMonth + '/' + inDate + '.txt', mode = 'r'); 
    records = IO.readlines(); #read all and save to list
    for record in records:
        fields = record.split('\t');
        f3v[cleanSC(fields[1])] = [cleanSC(fields[2]), cleanSC(fields[3]), cleanSC(fields[4])]; 
    IO.close();
    return f3v;

def getSR(inDate): 
    print('inDate', inDate);
    print stockFolder
    sr = {};
    sp = {};
    dataYear = inDate[0:4];
    IO = open(rootFolder + stockFolder + dataYear + '/' + inDate + '.txt', mode = 'r'); 
    records = IO.readlines();
    for record in records:
        #fields = record.split('\t');
        fields = record.split(' ');
        print fields
        sr[cleanSC(fields[1])] = cleanSC(fields[3]); 
        sp[cleanSC(fields[1])] = cleanSC(fields[4]);
    IO.close();
    return sr, sp;

def getstockID():
    stockID = {};
    IO = open(rootFolder + prepareFolder + 'stockID_Name.txt', mode = 'r'); 
    records = IO.readlines();
    for record in records:
        fields = record.split('\t');
        stockID[cleanSC(fields[0])] = cleanSC(fields[1]); 
    IO.close();
    return stockID;

def getF5V(inDate): 
    dataYear = inDate[0:4];
    
    f5v = {};
    fYear = '';
    fMonth = '';
    sYear = int(inDate[0:4]);
    sMonth = int(inDate[4:6]);
    sDay = int(inDate[6:8]);
    
    if ((datetime.date(sYear, sMonth, sDay) >= datetime.date(sYear, 5, 16)) and (datetime.date(sYear, sMonth, sDay) <= datetime.date(sYear, 8, 14))): 
        fYear = str(sYear);
        fMonth = '03';
    elif ((datetime.date(sYear, sMonth, sDay) >= datetime.date(sYear, 8, 15)) and (datetime.date(sYear, sMonth, sDay) <= datetime.date(sYear, 11, 14))): 
        fYear = str(sYear);
        fMonth = '06';
    elif ((datetime.date(sYear, sMonth, sDay) >= datetime.date(sYear, 11, 15)) and (datetime.date(sYear, sMonth, sDay) <= datetime.date(sYear, 12, 31))): 
        fYear = str(sYear);
        fMonth = '09';
    elif ((datetime.date(sYear, sMonth, sDay) >= datetime.date(sYear, 1, 1)) or (datetime.date(sYear, sMonth, sDay) <= datetime.date(sYear, 3, 31))): 
        dataYear = str(sYear - 1);
        fYear = str(sYear - 1);
        fMonth = '09';
    elif ((datetime.date(sYear, sMonth, sDay) >= datetime.date(sYear, 4, 1)) and (datetime.date(sYear, sMonth, sDay) <= datetime.date(sYear, 5, 15))): 
        fYear = str(sYear - 1);
        fMonth = '12';
    
    IO = open(rootFolder + financeFolder + dataYear + '/' + fYear + fMonth + '.txt', mode = 'r'); 
    IO.readline(); 
    records = IO.readlines();
    for record in records:
        fields = record.split('\t');        
        f5v[cleanSC(fields[1])] = [cleanSC(fields[3]),cleanSC(fields[4]),cleanSC(fields[5]),cleanSC(fields[6]),cleanSC(fields[7])];
    IO.close();
    return f5v;

def getTNnewsDate(inDate, tLimit):
    tcount = 1; 
    tcountLimit = tLimit; 
    iYear = int(inDate[0:4]);
    iMonth = int(inDate[4:6]);
    iDay = int(inDate[6:8]);
    deltaDays = -1;
    yDay = datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d'); 
    yYear = yDay[0:4];    
    nDate = []; 
    tDate = []; 
    while tcount <= tcountLimit: 
        if tcount < tcountLimit: 
            if os.path.isfile(rootFolder + stockFolder + yYear + '/' + yDay + '.txt'): 
                tDate.append(datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d')); 
                tcount = tcount + 1; 
            nDate.append(datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d')); 
            deltaDays = deltaDays - 1; 
            yDay = datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d'); 
            yYear = yDay[0:4];
        else: 
            if os.path.isfile(rootFolder + stockFolder + yYear + '/' + yDay + '.txt'):
                nDate.append(datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d'));
                tcount = tcount + 1;
            else: 
                nDate.append(datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d')); 
                deltaDays = deltaDays - 1; 
                yDay = datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d'); 
                yYear = yDay[0:4];
                while os.path.isfile(rootFolder + stockFolder + yYear + '/' + yDay + '.txt') == False: 
                    nDate.append(datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d')); 
                    deltaDays = deltaDays - 1; 
                    yDay = datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay) + datetime.timedelta(days = deltaDays), '%Y%m%d'); 
                    yYear = yDay[0:4];
    return nDate, tDate;

def mergeP(inDate):
    coeff = getCoefficient(); 
    stockID = getstockID(); 
    f5v = getF5V(inDate); 

   
    newsDate = []; 
    transactionDate = [];  
    newsDate, transactionDate = getTNnewsDate(inDate, 7);   
    
    print newsDate
    print transactionDate	
    iYear = int(inDate[0:4]); 
    iMonth = int(inDate[4:6]); 
    iDay = int(inDate[6:8]); 
    
   
    calResult = {}; 

    for key in stockID:
        calResult[key] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];


    fdata_v = 0;
    for fdate in transactionDate: 
        sr = {};
        sp = {};
        sr, sp = getSR(fdate); 
        for key in stockID:
            if key in sr:
                calResult[key][fdata_v + 2] = float(sr[key]);                
                calResult[key][8] = calResult[key][8] + calResult[key][fdata_v + 2];
            if key in sp:
                calResult[key][fdata_v + 18] = float(sp[key]);
        fdata_v = fdata_v + 1;

    
    for ndate in newsDate: 
        f3v = getF3V(ndate); 
        for key in stockID: 
            if key in f3v:
                for v in range(3): 
                    calResult[key][v + 10] = calResult[key][v + 10] + float(f3v[key][v]);
                    
       
    for key in stockID:
        if key in f5v:
            for v in range(5): 
                if f5v[key][v] == '-': 
                    calResult[key][v + 13] = calResult[key][v + 13] + 0;
                else:
                    calResult[key][v + 13] = calResult[key][v + 13] + float(f5v[key][v]);
       
        calResult[key][9] = calResult[key][9] + float(coeff['c']); 
        calResult[key][9] = calResult[key][9] + float(coeff['Pnews']) * calResult[key][10]; 
        calResult[key][9] = calResult[key][9] + float(coeff['Nnews']) * calResult[key][11]; 
        calResult[key][9] = calResult[key][9] + float(coeff['avgScore']) * calResult[key][12]; 
        calResult[key][9] = calResult[key][9] + float(coeff['EPS']) * calResult[key][13]; 
        calResult[key][9] = calResult[key][9] + float(coeff['ROA']) * calResult[key][14]; 
        calResult[key][9] = calResult[key][9] + float(coeff['ROE']) * calResult[key][15]; 
        calResult[key][9] = calResult[key][9] + float(coeff['BPS']) * calResult[key][16]; 
        calResult[key][9] = calResult[key][9] + float(coeff['PB']) * calResult[key][17]; 

   
    for key in stockID:
        if key in calResult:
            calResult[key][1] = 7 * calResult[key][9] - calResult[key][8];
            if calResult[key][1] > 0: 
                calResult[key][0] = 'Positive';
            if calResult[key][1] < 0:
                calResult[key][0] = 'Negative';
        
    
    if (os.path.isdir(rootFolder + txtFolder + str(iYear) + '/' + str(iMonth)) == False): 
        os.makedirs(rootFolder + txtFolder + str(iYear) + '/' + str(iMonth));
    IO = open(rootFolder + txtFolder + str(iYear) + '/' + str(iMonth) + '/' + datetime.datetime.strftime(datetime.date(iYear, iMonth, iDay), '%Y%m%d') + '.txt', mode = 'w');
    for key in calResult:
        
        IO.write(key + '\t' +
                 str(calResult[key][0]) + '\t' +
                 str(calResult[key][1]) + '\t' +
                 str(calResult[key][2]) + '\t' +
                 str(calResult[key][3]) + '\t' +
                 str(calResult[key][4]) + '\t' +
                 str(calResult[key][5]) + '\t' +
                 str(calResult[key][6]) + '\t' +
                 str(calResult[key][7]) + '\t' +
                 str(calResult[key][8]) + '\t' +
                 str(calResult[key][9]) + '\t' +
                 str(calResult[key][10]) + '\t' +
                 str(calResult[key][11]) + '\t' +
                 str(calResult[key][12]) + '\t' +
                 str(calResult[key][13]) + '\t' +
                 str(calResult[key][14]) + '\t' +
                 str(calResult[key][15]) + '\t' +
                 str(calResult[key][16]) + '\t' +
                 str(calResult[key][17]) + '\n');
    IO.close();


for pastSevenDays in range(0, -7, -1):

    tDay = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days = pastSevenDays), '%Y%m%d');
    print tDay;
    #for i in range(0, 22):
    #tDay = str(20161101+i)
    whatYear = tDay[0:4];
    whatMonth = tDay[4:6];
    whatDay = tDay[6:8];
    print tDay;
   
        #tDay="20151027";
    mergeP(tDay);

print "merge complete";


