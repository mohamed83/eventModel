class Collection:
    ''' Class for handling corpus collection'''
    def __init__(self):
        self.URLs= []
        self.documents = []
        self.words = []
        self.sentences = []
        self.indicativeWords = []
        self.indicativeSentences = []
    
    def __init__(self,urls):
        self.URLs = urls
        self.documents = []
        self.words = []
        self.sentences = []
        self.indicativeWords = []
        self.indicativeSentences = []
    
     
        