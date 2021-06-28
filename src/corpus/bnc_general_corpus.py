from corpus.base_general_corpus import BaseGeneralCorpus

import sqlite3

class BncGeneralCorpus(BaseGeneralCorpus):

    def __init__(self, db_path: str):
        """
        BncGeneralCorpus constructor.

        Parameters
        ----------
        db_path : str
            Path of database.

        Returns:
        ----------
        A BncGeneralCorpus instance.
        
        """

        self.__db_path = db_path


    def search_noun(self, movie_nouns_occurrences: dict) -> list:
        """
        Search noun in BNC and retrieves it values: the noun(text) and its frequency (int).
        Later, maps each noun with its frequency in a movie corpus and in BNC.


        Parameters
        ----------
        movie_nouns_occurrences : dict 
            A dict containing a noun present in a movie corpora and its frequency in movie reviews.

        Returns:
        ----------
        nouns_corporas_occurrences : list 
            A list of tuples - (noun string, frequency of this noun in review corpora, frequency of this noun in BNC).

        """

        connection = sqlite3.connect(self.__db_path)
        cursor = connection.cursor()

        nouns_corporas_occurrences = []

        for word in movie_nouns_occurrences.keys():

            cursor.execute("SELECT * FROM nouns_frequencies WHERE noun=?", (word,))
            fetched = cursor.fetchall()

            if fetched:
                bnc_noun_occurrence = int(fetched[0][1])
            else:
                bnc_noun_occurrence = 0

            noun_values = (word, movie_nouns_occurrences[word], bnc_noun_occurrence)
            nouns_corporas_occurrences.append(noun_values)

        connection.close()

        return nouns_corporas_occurrences