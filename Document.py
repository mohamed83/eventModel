class Document:
    ''' class for representing corpus document'''
    def __init__(self):
        self.URL = ''
        self.text = ''
        self.words = []
        self.sentences = []
    
    def __init__(self,url):
        self.URL = url
        self.text = ''
        self.words = []
        self.sentences = []