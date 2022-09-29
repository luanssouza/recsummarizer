import numpy as np
from scipy import cluster

from .summarizer_clusters import SummarizerClusters

class SummarizerClustersSemantic(SummarizerClusters):
    def __init__(self, items_path, discard_threshold, number_of_sentences_in_summary):
        super().__init__(items_path, discard_threshold, number_of_sentences_in_summary)

    def summarize(self, item_id:int, n_clusters: int) -> list:
        item_dir = self._items_path + "{0}".format(item_id)
        item = self._get_item(item_dir)
        if not item:
            return []
        item.aspects_embeddings = pd.read_csv(item_dir + "/embeddings.csv").fillna(0).to_numpy()
        item.aspects = self._cut_label(item, n_clusters)
        return self._summary_sentences(item)
        
    def _cut_label(self, item, n_clusters) -> list:
        aspects_clusters = cluster.hierarchy.cut_tree(item.clusters, n_clusters=n_clusters)
        item.aspects_df['cluster'] =  np.squeeze(aspects_clusters)
        
        r = []
        for i in range(0, n_clusters):
            asp_clt = item.aspects_df[item.aspects_df['cluster'] == i]
            asp_idx = asp_clt.index.to_list()
            asp_cen = sum(item.aspects_embeddings[asp_idx])
            asp_max = 0
            aspect = ''
            for i, row in asp_clt.iterrows():
                sim = self._cosine_similarity(asp_cen, item.aspects_embeddings[i])
                if sim > asp_max:
                    aspect = row['aspect']
                    
            r.append(aspect)

        return r