from .base_review import Review

from ..sentence import Sentence

import string

import xml.etree.ElementTree as ET

class XmlReview(Review):
    def __init__(self, file):
        super().__init__()
        
        self.review_extractor(file)

    def review_extractor(self, file):
        
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
            new_sentence = Sentence(sentence_id, sentiment_value, sentiment, filename)
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