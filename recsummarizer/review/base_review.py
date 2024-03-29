from collections import Counter


class Review(object):
    def __init__(self):
        self._id = 0
        self._file_name = ""
        self._sentences = []
        self._number_of_sentences = 0
        self._occurrences_of_each_aspect = Counter()
        self._aspects = []
        self._average_sentiment = 0
        self._raw_review = ""
        self._nouns_occurrences = Counter()        
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def sentences(self):
        return self._sentences
    
    @property
    def number_of_sentences(self):
        return self._number_of_sentences

    @number_of_sentences.setter
    def number_of_sentences(self, number):
        self._number_of_sentences = number

    @property
    def occurrences_of_each_aspect(self):
        return self._occurrences_of_each_aspect

    @property
    def average_sentiment(self):
        return self._average_sentiment

    @property
    def file_name(self):
        return self._file_name
    
    @property
    def nouns_occurrences(self):
        return self._nouns_occurrences

    @property
    def raw_review(self):
        return self._raw_review


    def review_extractor(self, file): 
        """
        Given a file that represents a review, this function instantiates 
        review objects (and consequently, sentence objects) by parsing the tree.
        For each review object, is computed it's file name, it's sentences, number of sentences,
        average sentiment, and occurrences of nouns. The aspects aren't instantiated in
        this function, but in the module movie.py.

        
        Args: 
            file (Path): the file containing a raw single review

        Returns:
            None

        """    
        
        pass