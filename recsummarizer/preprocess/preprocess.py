from ..extractor.KL_divergence import epsilon_aspects_extraction
from ..movie.movie import Movie
from pathlib import Path

class PreProcess(object):
    def __init__(self, kl_threshold, top_k_number):
        self.__kl_threshold = kl_threshold
        self.__top_k_number = top_k_number

    def proprocess(self, base_path, persistence, general_corpus, review_file_type):
        current_directory = Path.cwd()
        # single_reviews_corenlp is a directory containing other folders inside it, in which
        # there are .txt files representing the item reviews
        movies_directory = Path(current_directory, base_path)
        
        for single_movie_directory in movies_directory.iterdir():

            print("trying to create: ", single_movie_directory)
            new_movie = Movie(single_movie_directory, general_corpus, review_file_type)
            print("movie created:", new_movie.file_name)
            new_movie.kl_values()

            new_movie.aspects_score = epsilon_aspects_extraction(new_movie.kl_nouns_values, self.__kl_threshold)
            # above, the top k aspects of a given itme is evaluated:
            new_movie.top_k_aspects_evaluation(self.__top_k_number)

            # in the sentence filtering phase, the sentences there are going to feed the
            # summarizator are selected:
            new_movie.sentence_filtering()

            persistence.persist_movie(new_movie)


    