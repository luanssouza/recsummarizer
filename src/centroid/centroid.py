import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import math 
from collections import OrderedDict

from gensim.parsing.preprocessing import remove_stopwords
from gensim.parsing.preprocessing import strip_punctuation

class Centroid(object):
    def __init__(self, normalizer, threshold):
        self.__normalizer = normalizer
        self.__threshold = threshold

    def get_centroid(self, movie):

        movie_reviews = []

        for review in movie.reviews:

            processed_review = strip_punctuation(review.raw_review)
            processed_review = remove_stopwords(processed_review)
            # now, processed_review is a document going to tf-idf phase,
            # and each processed review is considered as a document.

            movie_reviews.append(processed_review)

        text_data = np.array(movie_reviews)

        count = CountVectorizer()
        bag_of_words = count.fit_transform(text_data)

        feature_names = count.get_feature_names()


        aux_dataframe = pd.DataFrame(bag_of_words.toarray(), columns=feature_names)
        aux_dataframe = aux_dataframe.transpose()

        number_total_documents = len(aux_dataframe.columns)

        dataframe_tf_idf = self.__normalizer.normalize(aux_dataframe)
        
        last_columns_of_values = (-1 * number_total_documents)

        dataframe_only_columns = dataframe_tf_idf[dataframe_tf_idf.columns[last_columns_of_values:]]
        
        dictionary = dataframe_only_columns.to_dict(orient="index")

        selected_centroid_words = []
        
        for word in dictionary:
                word_documents_value = dictionary[word]

                for documents in word_documents_value:

                    tf_idf_value = word_documents_value[documents]

                    if(tf_idf_value > self.__threshold):

                        selected_centroid_words.append(word)
                        
        selected_centroid_words = set(selected_centroid_words)
        
        return selected_centroid_words