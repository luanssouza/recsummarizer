from .base_general_corpus import BaseGeneralCorpus

import pandas as pd

class CsvGeneralCorpus(BaseGeneralCorpus):

    def __init__(self, nouns_df: pd.DataFrame):
        """
        CsvGeneralCorpus constructor.

        Parameters
        ----------
        nouns_df : DataFrame
            DataFrame with nouns frequency.

        Returns:
        ----------
        A CsvGeneralCorpus instance.
        
        """

        self.__nouns_df = nouns_df


    def search_noun(self, item_nouns_occurrences: dict) -> list:
        """
        Search noun in a General Corpus and retrieves it values: the noun(text) and its frequency (int).
        Later, maps each noun with its frequency in a item corpus and in a General Corpus.


        Parameters
        ----------
        item_nouns_occurrences : dict 
            A dict containing a noun present in a item corpora and its frequency in item reviews.

        Returns:
        ----------
        nouns_corporas_occurrences : list 
            A list of tuples - (noun string, frequency of this noun in review corpora, frequency of this noun in a General Corpus).

        """

        nouns_corporas_occurrences = []

        for word in item_nouns_occurrences.keys():

            try:
                bnc_noun_occurrence = self.__nouns_df.loc[word][0]
            except KeyError:
                bnc_noun_occurrence = 0                

            noun_values = (word, item_nouns_occurrences[word], bnc_noun_occurrence)
            nouns_corporas_occurrences.append(noun_values)

        return nouns_corporas_occurrences