import pandas as pd
import numpy as np

import scipy.cluster.hierarchy as shc
from scipy import cluster

from collections import Counter

from embedding import embeddings

def cluster_emb(aspects):
    aspects_df = pd.DataFrame(aspects.items(), columns=['aspect', 'frequency'])

    aspects_df['embedding'] = list(embeddings.sentences_embeddings(aspects_df['aspect'].to_list()))

    return shc.linkage(np.array(aspects_df['embedding'].to_list())), pd.DataFrame(aspects_df['embedding'].to_list())

def cuttree(aspects_df: pd.DataFrame, n_clusters: int, clusters: np.ndarray):

    aspects_df['cluster'] =  np.squeeze(cluster.hierarchy.cut_tree(clusters, n_clusters=n_clusters))

    r = []
    for i in range(0, n_clusters):
      idxmax = aspects_df[aspects_df['cluster'] == i]['frequency'].idxmax()
      r.append(aspects_df.loc[idxmax]['aspect'])
    return r

