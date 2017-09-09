import os, sys, string, re, datetime,time;
from GetFilePaths import GetFilePaths as GetFilePaths; #get folder file list
from FileToList import FileToList as FileToList; #transfer file to list


rootFolder = "";
prepareFolder = 'prepareFile/';
newsFolder = 'news/'; 
outputFolder = 'newsPNV/'; 
if os.path.isdir(rootFolder + outputFolder) == False:
        os.makedirs(rootFolder + outputFolder); 


PosDictRead = open(rootFolder + prepareFolder + "PositiveWords.txt", 'r'); #read file
NegDictRead = open(rootFolder + prepareFolder + "NegativeWords.txt", 'r'); #read file
PosWordsList = PosDictRead.readlines(); 
NegWordsList = NegDictRead.readlines();
PosWordsList = [w.strip('\n') for w in PosWordsList];
NegWordsList = [w.strip('\n') for w in NegWordsList];
lenPosDict = len(PosWordsList); 
SentimentalList = PosWordsList + NegWordsList; 
PosDictRead.close(); #close file
NegDictRead.close(); #close file
ScoreDict = [];
ScoreWordsList = {};
for i in range(5):
        ScoreDict.append("ScoredWords" + str(i + 1) + ".txt");
        IO = open(rootFolder + prepareFolder + ScoreDict[i], 'r'); #read file
        ScoreWordsList[i + 1] = IO.readlines();
        ScoreWordsList[i + 1] = [w.strip('\n') for w in ScoreWordsList[i + 1]];
IO.close(); #close file


def Clearup(s, chars):
        return re.sub('[%s]' % chars, '', s);


def ChiSquaredTest(CandidateDict, G1DF, G2DF, numG1, numG2):
        total = numG1 + numG2; 
        ChiSquareTS = {};  
        for key in CandidateDict:
                N10 = numG1 - G1DF[key]; 
                N11 = numG2 - G2DF[key];
                N0 = G1DF[key] + G2DF[key];
                N1 = N10 + N11;
                if N0 == 0 or N1 == 0:
                        ChiSquareTS[key] = 0;
                else:
                        #期望值
                        E00 = float(N0*numG1) / total;
                        E01 = float(N0*numG2) / total;
                        E10 = float(N1*numG1) / total;
                        E11 = float(N1*numG2) / total;
                        if E00 != 0 and E01 != 0 and E10 != 0 and E11 != 0:
                                if E00 < 5 or E01 <5 or E10 < 5 or E11 < 5:
                                        ChiSquareTS[key] = (abs(G1DF[key] - E00) - 0.5)**2 / E00 + (abs(G2DF[key] - E01) - 0.5)**2 / E01 + (abs(N10 - E10) - 0.5)**2 / E10 + (abs(N11 - E11) - 0.5)**2 / E11;
                                else:
                                        ChiSquareTS[key] = ((G1DF[key] - E00)**2 / E00) + ((G2DF[key] - E01)**2 / E01) + ((N10 - E10)**2 / E10) + ((N11 - E11)**2 / E11);
                        else: 
                                ChiSquareTS[key] = 0;
        return ChiSquareTS; # Return the test statistic of Chi-squared test of each word in the candidate dictionary


def HammingDistance(s1, s2): #Return the Hamming distance between equal-length sequences        
        if len(s1)!=len(s2):
                print("Undefined for sequences of unequal length")
        return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2)) #zip

def process_news_list(yesterDay):
      
        N00 = {};  
        N01 = {};  
        for w in SentimentalList:  # initialize all values to zero 
                N00[w] = 0;
                N01[w] = 0;
        whatYear = str(yesterDay[0:4]);
        whatMonth = str(yesterDay[4:6]);
        newsList = os.listdir(rootFolder + newsFolder + whatYear + '/' + whatMonth + '/' + yesterDay + '/'); 
        NumofPosNews = 0; 
        NumofNegNews = 0; 
        newsTitleWeight = 0.6; 
        stockIDList = [];     
        newsTitlePorN = {}; 
        newsContentPorN = {}; 
        newsAddvalue = {}; 
        newsScores = {}; 
        newsTitle = '';
        stockID = '';        
        for newsFile in newsList:                 
                newsTitle = newsFile.split("##")[0]; 
                stockID = newsFile.split("##")[1].replace('.txt',''); 
                if stockID not in stockIDList:
                        stockIDList.append(stockID);
                mykey = stockID + '\\' + newsTitle;  
                
                p = 0; 
                n = 0;            
                
                for term in PosWordsList:
                        if term in newsTitle:
                                p = p + 1;
                for term in NegWordsList:
                        if term in newsTitle:
                                n = n + 1;
                             
                if p > n:
                        newsTitlePorN[mykey] = 1;
                elif p == n:
                        newsTitlePorN[mykey] = 0;
                elif p < n:
                        newsTitlePorN[mykey] = -1;            
               
                IO = open(rootFolder + newsFolder + whatYear + '/' + whatMonth + '/' + yesterDay + '/' + newsFile, 'r');
                newsContent = IO.read();
                IO.close();            
                p = 0;
                n = 0;
                for term in PosWordsList:
                        if term in newsContent:
                                p = p + 1;
                for term in NegWordsList:
                        if term in newsContent:
                                n = n + 1;
                if p > n:
                        newsContentPorN[mykey] = 1;
                        NumofPosNews = NumofPosNews + 1;
                elif p == n:
                        newsContentPorN[mykey] = 1;
                elif p < n:
                        newsContentPorN[mykey] = -1;
                        NumofNegNews = NumofNegNews + 1;
                
                newsScores[mykey] = [];
                termTemp = []; 
                for term1 in SentimentalList:
                        if term1 in newsContent: 
                                if term1 not in termTemp: 
                                        termTemp = termTemp + [term1];
                                        if newsContentPorN[mykey] == 1: 
                                                N00[term1] = N00[term1] + 1;
                                        elif newsContentPorN[mykey] == -1: 
                                                N01[term1] = N01[term1] + 1; 
                
                for score in range(1, 5):
                        for term in ScoreWordsList[score]:
                                if term in newsContent:
                                        newsScores[mykey].append(score); #ex.newsScore[mykey] => [3, 3, 3, 2, 3, 1, 5, 3, 2, 3, 2, ...]
                scoreNoDuplicate = []; 
                for score in newsScores[mykey]: 
                        if score not in scoreNoDuplicate:
                                scoreNoDuplicate.append(score); 
                newsAddvalue[mykey] = str(len(scoreNoDuplicate)) + " " + str(sorted(scoreNoDuplicate)); 
                m = newsTitleWeight * newsTitlePorN[mykey] + (1 - newsTitleWeight) * newsContentPorN[mykey];
                if m < 0:
                        NumofNegNews = NumofNegNews + 1;
                elif m > 0:
                        NumofPosNews = NumofPosNews + 1;

        
        CV = 3.8415;  
        Chi2TS = ChiSquaredTest(SentimentalList, N00, N01, NumofPosNews, NumofNegNews); 

        featureList = [];  
        PosFeatureList = [];  
        NegFeatureList = [];  
        count = 0;
        for term in SentimentalList:
                if Chi2TS[term] > CV:
                        featureList.append(term);
                        
                        if      count < lenPosDict:
                                PosFeatureList.append(1);
                                NegFeatureList.append(0);
                        else:
                                NegFeatureList.append(1);
                                PosFeatureList.append(0);
                count += 1;                
        NumofFeatures = len(featureList);

       
        PosMatrix=[{} for row in range(NumofPosNews + 1)];
        PosMatrix[0]={'ky':featureList};        
        NegMatrix=[{} for row in range(NumofNegNews + 1)];
        NegMatrix[0]={'ky':featureList};        
        PosHD = {};
        NegHD = {};
        Decision = {};        
        newsIndex = 0;

        for newsFile in newsList: 
                newsTitle = newsFile.split("##")[0]; 
                stockID = newsFile.split("##")[1].replace('.txt',''); 
                mykey = stockID + '\\' + newsTitle; 
                IO = open(rootFolder + newsFolder + whatYear + '/' + whatMonth + '/' + yesterDay + '/' + newsFile, 'r');
                newsContent = IO.read();
                IO.close();
                if newsContentPorN[mykey] == 1: 
                        PosMatrix[NumofPosNews] = {mykey:[0 for col in range(NumofFeatures)]}; 
                        for feature in range(NumofFeatures):
                                if PosMatrix[0]['ky'][feature] in newsContent: 
                                        PosMatrix[NumofPosNews][mykey][feature] = 1;

                        if sum(PosFeatureList) == 0:
                                PosHD[mykey] = 9999;
                        else:
                                PosHD[mykey] = HammingDistance(PosMatrix[NumofPosNews][mykey], PosFeatureList) / sum(PosFeatureList) 
                        if sum(NegFeatureList) == 0:
                                NegHD[mykey] = 9999;
                        else:
                                NegHD[mykey] = HammingDistance(PosMatrix[NumofPosNews][mykey], NegFeatureList) / sum(NegFeatureList) 
                        if PosHD[mykey] < NegHD[mykey]: 
                               newsContentPorN[mykey] = 1; 
                        elif PosHD[mykey] == NegHD[mykey]:
                               newsContentPorN[mykey] = 0;
                        elif PosHD[mykey] > NegHD[mykey]: 
                               newsContentPorN[mykey] = -1; 
                        NumofPosNews = NumofPosNews - 1; 
                elif newsContentPorN[mykey] == -1: 
                        NegMatrix[NumofNegNews] = {mykey:[0 for col in range(NumofFeatures)]}; 
                        for feature in range(NumofFeatures):
                                if NegMatrix[0]['ky'][feature] in newsContent: 
                                        NegMatrix[NumofNegNews][mykey][feature] = 1;
                        if sum(PosFeatureList) == 0:
                                        PosHD[mykey] = 9999;
                        else:
                                PosHD[mykey] = HammingDistance(NegMatrix[NumofNegNews][mykey],PosFeatureList) / sum(PosFeatureList);
                        if sum(NegFeatureList) == 0:
                                NegHD[mykey] = 9999;
                        else:
                                NegHD[mykey] = HammingDistance(NegMatrix[NumofNegNews][mykey],NegFeatureList) / sum(NegFeatureList);
                        if PosHD[mykey] > NegHD[mykey]:
                                newsContentPorN[mykey] = -1; 
                        elif PosHD[mykey] == NegHD[mykey]:
                                newsContentPorN[mykey] = 0;                       
                        elif PosHD[mykey] < NegHD[mykey]:
                                newsContentPorN[mykey] = 1; 
                        NumofNegNews = NumofNegNews - 1;
                if newsTitlePorN[mykey] == 0 and newsContentPorN[mykey] == 0: 
                        Decision[mykey] = 0;
                else:
                        v = newsTitleWeight * newsTitlePorN[mykey] + (1 - newsTitleWeight) * newsContentPorN[mykey]; 
                        #print "v : "+str(v);
                        if v < 0:
                                Decision[mykey] = -1;
                        else:
                                Decision[mykey] = 1;
	#time.sleep(2)
        
        whatYear = yesterDay[0:4];
        whatMonth = yesterDay[4:6];
        if (os.path.isdir(rootFolder + outputFolder + whatYear + '/' + whatMonth + '/') == False): 
            os.makedirs(rootFolder + outputFolder + whatYear + '/' + whatMonth + '/');
        IO = open(rootFolder + outputFolder + whatYear + '/' + whatMonth + '/' + yesterDay + ".txt",'w');
	
        for stockID in stockIDList:
                numPos = 0;
                numNeg = 0;
                totScore = 0;
                totNum = 0;
                for newsFile in newsList: 
                        newsTitle = newsFile.split("##")[0]; 
                        newsStockID = newsFile.split("##")[1].replace('.txt',''); 
                        if stockID == newsStockID:
                                mykey = stockID + '\\' + newsTitle; 
                                if(float(Decision[mykey]) > 0):
                                        numPos = numPos + 1;
                                elif(float(Decision[mykey]) < 0):
                                        numNeg = numNeg + 1;
                                if float(newsAddvalue[mykey].split(" ")[0]) > 0:
                                        totScore = totScore + float(newsAddvalue[mykey].split(" ")[0]);
                                        totNum = totNum + 1;

                       
                #totalPN_news = numPos + numNeg;
                if totNum == 0:
                        IO.write(yesterDay + '\t' + stockID + '\t' + str(numPos) + '\t' + str(numNeg) + '\t' + str(0) + '\n');
			print yesterDay + '\t' + stockID + '\t' + str(numPos) + '\t' + str(numNeg) + '\t' + str(0) + '\n';

                elif totNum != 0:
                        IO.write(yesterDay + '\t' + stockID + '\t' + str(numPos) + '\t' + str(numNeg) + '\t' + str(float(totScore) / totNum) + '\n');
			print yesterDay + '\t' + stockID + '\t' + str(numPos) + '\t' + str(numNeg) + '\t' + str(float(totScore) / totNum) + '\n'


        IO.close()


deltaDays = -1;
yd = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days = deltaDays), '%Y%m%d');
yd = time.strftime("%Y%m%d")
print "Date : "+yd;



t=time.time();
process_news_list(yd);
'''for i in range(0, 30):
	yd = 20161101+i
	#get_file(str(toDay));
	process_news_list(str(yd));'''

print "exec time : "+str(time.time()-t);
#news_size = os.listdir(newsFolder+'2016/10/'+str(yd));
#print "news_size : "+str(len(news_size));
