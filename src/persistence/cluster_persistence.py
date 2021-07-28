from persistence.base_persistence import Persistence

from pathlib import Path

import scipy.cluster.hierarchy as shc

import pandas as pd
import numpy as np

class ClusterPersistence(Persistence):

    def __init__(self, dist_path: str, embedding, centroid):
        super().__init__(dist_path, embedding)
        self.__centroid = centroid

    def persist_movie(self, movie):
        movie_dir = self._dist_path + movie.file_name

        # making movie's folder
        Path(movie_dir).mkdir(parents=True, exist_ok=True)

        # making movie's aspects frequency csv
        asp_freq = {a: movie.nouns_occurrences[a] for a in movie.top_k_aspects}

        aspects_df = pd.DataFrame(asp_freq.items(), columns=['aspect', 'frequency'])

        aspects_df.to_csv(movie_dir + "/aspects.csv", index=False)
        
        # Saving filtered sentences
        filtered_sentences = []
        for f_s in movie.filtered_sentences_nn:
            sentence = f_s[0]
            nouns = list(f_s[1].retrieve_nouns().elements())
            filtered_sentences.append({'sentences': sentence, 'nouns': nouns })

        sentences_df = pd.DataFrame(filtered_sentences)
        sentences_df.to_csv(movie_dir + "/filtered_sentences.csv", index=False)

        # Saving filtered sentences embeddings
        sentences = [s['sentences'] for s in filtered_sentences]
        embeddings = list(self._embedding.sentences_embeddings(sentences))
        embeddings_df = pd.DataFrame(embeddings)
        embeddings_df = embeddings_df.fillna(0)
        embeddings_df.to_csv(movie_dir + "/embeddings_sentences.csv", index=False)

        # Saving aspects embeddings
        embeddings = list(self._embedding.sentences_embeddings(aspects_df['aspect'].to_list()))
        embeddings_df = pd.DataFrame(embeddings)
        embeddings_df = embeddings_df.fillna(0)
        embeddings_df.to_csv(movie_dir + "/embeddings.csv", index=False)

        # Saving clusters
        np.save(movie_dir + "/clusters.npy", self.__cluster_emb(embeddings_df.to_numpy()))


        # Saving Centroids
        centroid = self.__centroid.get_centroid(movie)
        centroid = " ".join(list(centroid))
                
        centroid_emb = self._embedding.sentence_embedding(centroid)

        np.save(movie_dir + "/centroid.npy", centroid_emb)
    
    def __cluster_emb(self, embeddings: np.ndarray):
        return shc.linkage(embeddings)
