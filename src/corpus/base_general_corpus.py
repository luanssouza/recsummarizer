class BaseGeneralCorpus(object):

    def search_noun(self, movie_nouns_occurrences: dict) -> list:
        """
        Search noun in a general corpus and retrieves it values: the noun(text) and its frequency (int).
        Later, maps each noun with its frequency in a movie corpus and in a general corpus.

        Parameters
        ----------
        movie_nouns_occurrences : dict 
            A dict containing a noun present in a movie corpora and its frequency in movie reviews.


        Returns:
        ----------
        nouns_corporas_occurrences : list 
            A list of tuples - (noun string, frequency of this noun in review corpora, frequency of this noun in a general corpus).
        """
        pass