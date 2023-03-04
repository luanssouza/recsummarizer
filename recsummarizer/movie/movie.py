from ..sentence import Sentence
from ..review.review_factory import review_factory
from ..extractor.KL_divergence import KL_divergence

from collections import Counter

from nltk.tokenize.treebank import TreebankWordDetokenizer
detokenizer = TreebankWordDetokenizer()

class Movie(object):

    def __init__(self, single_movie_directory, general_corpus, review_file_type):

        self.file_name = single_movie_directory.name
        self.reviews = []
        self.number_of_reviews = 0
        self.aspects_score = {}
        self.top_k_aspects = []
        self.filtered_sentences = []
        self.filtered_sentences_nn = []
        self.nouns_occurrences = Counter() 
        self.kl_nouns_values = {}

        self.__general_corpus = general_corpus
        self.__review_file_type = review_file_type

        self.movie_extractor(single_movie_directory)
    
    def movie_extractor(self, single_movie_directory):
        '''
        Function to instantiate Movie objects form the
        files processed by CoreNLP

        Parameters:

            single_movies_directory(directory): the folder
            containing each xml file parsed by CoreNLP
        '''

        for filename in single_movie_directory.iterdir():
            
            new_review = review_factory(filename, self.__review_file_type)
            
            if new_review:
                
                self.reviews.append(new_review)
                self.number_of_reviews += 1
                new_review.id = self.number_of_reviews
                
                for noun in new_review.nouns_occurrences:
                    self.nouns_occurrences[noun] += new_review.nouns_occurrences[noun] 


    
    def kl_values(self):
      
        '''
        Function that computes the KL value for each noun
        in the reviews of a movie

        Parameters:
            None

        Returns:
            None
        '''
        # nouns_frequencies_in_corporas: contain tuples - (noun string, frequency of this noun in review corpora, frequency of this noun in BNC)

        nouns_frequencies_in_corporas = self.__general_corpus.search_noun(self.nouns_occurrences)

        for noun_values in nouns_frequencies_in_corporas:

            noun = noun_values[0]
            frequency_in_reviews = noun_values[1]
            frequency_in_general = noun_values[2]      

            # for each noun in a movie, its KL value is computed:
            noun_kl_value = KL_divergence.KL_divergence(frequency_in_reviews, frequency_in_general)

            self.kl_nouns_values[noun] = noun_kl_value

            


    def top_k_aspects_evaluation(self, k):
              
        '''
        Function that computes top-k
        aspects of a movie

        Parameters:
            k - the top-k number; if k=5, so
            the top-5 aspects are evaluated.

        Returns:
            None
        '''
        
        #above, key=lambda x: x[1] guarantees that the dict is going to be sorted by 
        #it's score value;
        #reverse=True means the ordering is going to be in descending order
        sorted_aspects = sorted(self.aspects_score.items(), key=lambda x: x[1], reverse=True)
       
        for x in sorted_aspects[0:k]:
            self.top_k_aspects.append(x[0])

   
    
    def aspect_scoring(self):

              
        '''
        Function that computes the score for
        each aspect in a movie item

        score = occurrence of the aspect in the current review * KL value os the aspect * average sentiment of the current review

        Parameters:
            None

        Returns:
            None
        '''

        for aspect in self.aspects_score:

            accumulated_score = 0

            for review in self.reviews:

                accumulated_score = review.nouns_occurrences[aspect] * kl_nouns_values[aspect] * review.average_sentiment

            aspect_score = accumulated_score / self.number_of_reviews
            
            self.aspects_score[aspect] = aspect_score

    
    
    def sentence_filtering(self):
           
        '''
        Function that filters the sentences having personal information,
        less than 5 tokens and with not positive sentiment, and
        that don't have an aspect in it.

        Parameters:
            None

        Returns:
            None
        '''
        
        for review in self.reviews:
            for sentence in review.sentences:

                personal_opinion = sentence.personal_opinion
                number_of_tokens = sentence.number_of_tokens
                sentiment_value = int(sentence.sentiment_value)

                if not personal_opinion and number_of_tokens > 5 and sentiment_value >= 3: 

                    nouns_in_sentence = sentence.retrieve_nouns()
                    
                    for noun in nouns_in_sentence.keys():
                        if noun in self.top_k_aspects:
                            self.filtered_sentences.append(detokenizer.detokenize(sentence.tokens))
                            self.filtered_sentences_nn.append((detokenizer.detokenize(sentence.tokens), sentence))
                            break


        
