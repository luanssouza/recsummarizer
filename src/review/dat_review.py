from review.base_review import Review

from sentence import Sentence as Sentence

from collections import Counter
import string

from corenlp_protobuf import Document, parseFromDelimitedString


class DatReview(Review):
    def __init__(self, file):
        super().__init__()
    
        self.review_extractor(file)
        
    def review_extractor(self, file): 
        
        filename = file.name.split(".")
        filename = filename[0] + ".dat"

        self._file_name = filename
        
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        # NN 	Noun, singular or mass
     	# NNS 	Noun, plural
     	# NNP 	Proper noun, singular
    	# NNPS 	Proper noun, plural
        
        desired_pos=["NN", "NNS", "NNP", "NNPS"]
       

        #first person pronouns should be compared in lower case:
        first_person_pronoun = ["i","we", "us","me","my","mine", "our", "ours", "myself", "ourselves"]
        
        review = file
        with open(review, 'rb') as f:
            buf = f.read()
        doc = Document()
        parseFromDelimitedString(doc, buf)


        punctuation = [i for i in string.punctuation]
        for s in doc.sentence:
            word_counter = 0
            sentiment_value = s.annotatedParseTree.sentiment
            sentiment = s.sentiment
            new_sentence = Sentence.Sentence(s.sentenceIndex, sentiment_value, sentiment, filename)
            self._number_of_sentences += 1
            sentiment_value = int(sentiment_value)            
            self._average_sentiment += sentiment_value

            for t in s.token:
                new_sentence.add_token(t.word)
                if t.word in punctuation:
                    continue

                word_counter += 1

                current_word = t.word.lower()
                
                if current_word in first_person_pronoun:
                    #personal opinion is setted to True:
                    new_sentence.personal_opinion = True
                
                if t.pos in desired_pos:
                    new_sentence.add_noun(current_word)  
                    self._nouns_occurrences[current_word] += 1

            new_sentence.number_of_tokens = word_counter
            self._sentences.append(new_sentence)
            self._raw_review += new_sentence.__str__()

        if self._number_of_sentences == 0:
            return False

        self._average_sentiment = self._average_sentiment / self._number_of_sentences
        
        return True