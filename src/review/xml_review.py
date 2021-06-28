from sentence import Sentence as Sentence

import xml.etree.ElementTree as ET
from collections import Counter
import string

from corenlp_protobuf import Document, parseFromDelimitedString



class Review:
    def __init__(self, file):
        self._id = 0
        self._file_name = "not instantiated yet"
        self._sentences = []
        self._number_of_sentences = 0
        self._occurrences_of_each_aspect = Counter()
        self._aspects = []
        self._average_sentiment = 0
        self._raw_review = ""
        self._nouns_occurrences = Counter()
        
        #self.review_extractor(file)
        self.review_extractor_dat(file)
        
    
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
        Given a xml file that represents a review, this function instantiates 
        review objects (and consequently, sentence objects) by parsing the xml tree.
        For each review object, is computed it's xml name, it's sentences, number of sentences,
        average sentiment, and occurrences of nouns. The aspects aren't instantiated in
        this function, but in the module Movie.py.

        
        Args: 
            file (Path): the file containing a raw single review

        Returns:
            None

        """    
        
        filename = file.name.split(".")
        filename = filename[0] + ".xml"

        self._file_name = filename
        
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        # NN 	Noun, singular or mass
     	# NNS 	Noun, plural
     	# NNP 	Proper noun, singular
    	# NNPS 	Proper noun, plural
        
        desired_pos=["NN", "NNS", "NNP", "NNPS"]
       

        #first person pronouns should be compared in lower case:
        first_person_pronoun = ["i","we", "us","me","my","mine", "our", "ours", "myself", "ourselves"]
        

        tree = ET.parse(file)
        root = tree.getroot()

        element = root.findall(".//sentence")# finds only elements with the tag "sentence" which are direct children of the current root    

        punctuation = [i for i in string.punctuation]

        for sentence in element:
            
            word_counter = 0
            sentence_id = sentence.attrib["id"]
            sentiment_value = sentence.attrib["sentimentValue"]
            sentiment = sentence.attrib["sentiment"]
            new_sentence = Sentence.Sentence(sentence_id, sentiment_value, sentiment, filename)
            self._number_of_sentences += 1
            sentiment_value = int(sentiment_value)            
            self._average_sentiment += sentiment_value
            
            
            sentence.findall(".//token")

            for tokens in sentence:
                for token in tokens:

                    for token_child in token:

                        if token_child.tag == "word":

                            current_word = token_child.text.lower()

                            if current_word in first_person_pronoun:
                        
                                #personal opinion is setted to True:
                                new_sentence.personal_opinion = True

                            new_sentence.add_token(token_child.text) 


                            if token_child.text not in punctuation:

                                word_counter += 1

                        if token_child.tag == "POS" and token_child.text in desired_pos:
                            for token_child in token:
                                if token_child.tag == "word":
                                    new_sentence.add_noun(token_child.text.lower())  
                                    self._nouns_occurrences[token_child.text.lower()] += 1
                                    

            new_sentence.number_of_tokens = word_counter
            self._sentences.append(new_sentence)
            self._raw_review += new_sentence.__str__()

        if self._number_of_sentences == 0:
            return False

        self._average_sentiment = self._average_sentiment / self._number_of_sentences
        
        return True