from extractor import KL_divergence, aspects_clustering as ac
from movie import  Movie
from pathlib import Path
import numpy as np
import pandas as pd

class PreProcess(object):
    def __init__(self, kl_threshold, top_k_number):
        self.__kl_threshold = kl_threshold
        self.__top_k_number = top_k_number

    def proprocess(self, base_path, dist_path, general_corpus):
        current_directory = Path.cwd()
        # single_reviews_corenlp is a directory containing other folders inside it, in which
        # there are .txt files representing the item reviews
        movies_directory = Path(current_directory, base_path)
        
        for single_movie_directory in movies_directory.iterdir():

            print("trying to create: ", single_movie_directory)
            new_movie = Movie.Movie(single_movie_directory, general_corpus)
            print("movie created:", new_movie.xml_name)
            new_movie.kl_values()

            new_movie.aspects_score = KL_divergence.epsilon_aspects_extraction(new_movie.kl_nouns_values, self.__kl_threshold)
            # above, the top k aspects of a given itme is evaluated:
            new_movie.top_k_aspects_evaluation(self.__top_k_number)
            
            movie_dir = dist_path + new_movie.xml_name

            # making movie's folder
            Path(movie_dir).mkdir(parents=True, exist_ok=True)

            # making movie's aspects frequency csv
            asp_freq = {a: new_movie.nouns_occurrences[a] for a in new_movie.top_k_aspects}

            aspects_df = pd.DataFrame(asp_freq.items(), columns=['aspect', 'frequency'])

            aspects_df.to_csv(movie_dir + "/aspects.csv", index=False)

            # in the sentence filtering phase, the sentences there are going to feed the
            # summarizator are selected:
            new_movie.sentence_filtering()

            filtered_sentences = []
            for i in range(len(new_movie.filtered_sentences)):
                sentence = new_movie.filtered_sentences[i]
                nouns = list(new_movie.filtered_sentences_nn[i][1].retrieve_nouns().elements())
                filtered_sentences.append({'sentences': sentence, 'nouns': nouns })

            sentences_df = pd.DataFrame(filtered_sentences)
            sentences_df.to_csv(movie_dir + "/filtered_sentences.csv", index=False)
            
            clusters, embeddings = ac.cluster_emb(asp_freq)
            np.save(movie_dir + "/clusters.npy", clusters)
            embeddings.to_csv(movie_dir + "/embeddings.csv", index=False)


    