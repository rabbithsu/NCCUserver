

def FileToList(fileName, mode = 1):
    if mode == 1: 
        sentences = [];
        txtRead = open(fileName, mode = "r");
        for sentence in txtRead:
            if "\t" in sentence: 
                sentence = sentence.split("\t");
                sentenceClean = [str(n).rstrip().replace("\ufeff","").strip() for n in sentence];       
            else: 
                sentenceClean = sentence.rstrip().replace("\ufeff", "").strip();
            sentences.append(sentenceClean);
        txtRead.close();
        return sentences;
    else: 
        sentences = [];
        txtRead = open(fileName, mode = "r");
        txtRead.readline();
        for sentence in txtRead:
            if "\t" in sentence: 
                sentence = sentence.split("\t");
                sentenceClean = [str(n).rstrip().replace("\ufeff","").strip() for n in sentence];       
            else: 
                sentenceClean = sentence.rstrip().replace("\ufeff", "").strip();
            sentences.append(sentenceClean);
        txtRead.close();
        return sentences;
