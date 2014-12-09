import Document
class Collection:
    ''' Class for handling corpus collection'''
    def __init__(self):
        self.URLs= []
        self.documents = []
        self.words = []
        self.sentences = []
        self.wordsFrequencies = []
        self.indicativeWords = []
        self.indicativeSentences = []
    
    def __init__(self,urls,texts):
        self.URLs = urls
        for u,d in zip(urls,texts):
            doc = new Document(u,d)
            self.documents.append(doc)
    
    def __init__(self,urls):
        self.URLs = urls
        for u in self.URLs:
            doc = new Document(u)
            self.documents.append(doc)
            
        #self.documents = []
        self.words = []
        self.sentences = []
        self.wordsFrequencies = []
        self.indicativeWords = []
        self.indicativeSentences = []
    
    def getFrequentWords(self):
        for d in self.documents:
            w = d.getWords()
            self.words.extend(w)
        f = utils.getFreq(self.words)
        tokensFreqs = f.items()
        self.wordsFrequencies = utils.getSorted(tokensFreqs,1)
        return self.wordsFrequencies
    
    def getIndicativeWords(self):
        if self.indicativeWords:
            return self.indicativeWords
        else:
            toksTFDF = self.getTokensTFDF()
            sortedToksTFDF = sorted(toksTFDF.items(), key=lambda x: x[1][0]*x[1][1], reverse=True)
            indWords = [w[0] for w in sortedToksTFDF]
            
            wordsTags = utils.getPOS(indWords)[0]
            nvWords = [w[0] for w in wordsTags if w[1].startswith('N') or w[1].startswith('V')]
            wordsDic = dict(sortedToksTFDF)
            self.indicativeWords = [(w,wordsDic[w]) for w in nvWords]
            return self.indicativeWords
            
    def getWordsTFDF(self):
        
        tokensTF = dict(self.wordsFrequencies)
        tokensDF = {}
        for te in tokensTF:
            df = sum([1 for t in self.documents if te in t.getWords()])
            tokensDF[te] = df
        
        tokensTFDF = {}
        for t in tokensDF:
            tokensTFDF[t] = (tokensTF[t],tokensDF[t])
        
        return tokensTFDF
    
    def getIndicativeSentences(self,topK,intersectionTh):
        if self.indicativeSentences:
            return self.indicativeSentences
        else:
            topToksTuples = self.indicativeWords[:topK]
            topToks = [k for k,_ in topToksTuples]
            
            for d in self.documents:
                sents = d.getSentences()
                self.sentences.extend(sents)
            
            impSents ={}
            for sent in self.sentences:
                if sent not in impSents:
                    sentToks = utils.getTokens(sent)
                    if len(sentToks) > 100:
                        continue
                    intersect = utils.getIntersection(topToks, sentToks)
                    if len(intersect) > intersectionTh:
                        impSents[sent] = len(intersect)
                        #if sent not in impSentsF:
                        #    impSentsF[sent] = len(intersect)
                    #allImptSents.append(impSents)
            
            self.indicativeSentences = utils.getSorted(impSents.items(),1)
            return self.indicativeSentences