from review.base_review import Review

from sentence import sentence as Sentence

import string


class StanzaReview(Review):
    def __init__(self, text, nlp_pipeline):
        super().__init__()
        self.__nlp_pipeline = nlp_pipeline
    
        self.review_extractor(text)
        
    def review_extractor(self, text): 

        doc = self.__nlp_pipeline(text)
        
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        # NN 	Noun, singular or mass
     	# NNS 	Noun, plural
     	# NNP 	Proper noun, singular
    	# NNPS 	Proper noun, plural
        
        desired_pos=["NN", "NNS", "NNP", "NNPS"]
       

        #first person pronouns should be compared in lower case:
        first_person_pronoun = ["i","we", "us","me","my","mine", "our", "ours", "myself", "ourselves"]

        punctuation = [i for i in string.punctuation]

        for s in doc.sentences:
            word_counter = 0
            sentiment_value = s.sentiment
            sentiment = s.sentiment
            new_sentence = Sentence.Sentence(s.index, sentiment_value, sentiment, "")
            self._number_of_sentences += 1
            sentiment_value = int(sentiment_value)            
            self._average_sentiment += sentiment_value

            for t in s.words:
                new_sentence.add_token(t.text)
                if t.text in punctuation:
                    continue

                word_counter += 1

                current_word = t.text.lower()
                
                if current_word in first_person_pronoun:
                    #personal opinion is setted to True:
                    new_sentence.personal_opinion = True
                
                if t.xpos in desired_pos:
                    new_sentence.add_noun(current_word)  
                    self._nouns_occurrences[current_word] += 1

            new_sentence.raw_sentence = s.text
            new_sentence.number_of_tokens = word_counter
            self._sentences.append(new_sentence)
            self._raw_review += new_sentence.__str__()

        if self._number_of_sentences == 0:
            return False

        self._average_sentiment = self._average_sentiment / self._number_of_sentences
        
        return True