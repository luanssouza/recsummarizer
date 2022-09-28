import numpy as np

from .item import Item
from summarizer.summarizer import Summarizer

class SummarizerClusters(Summarizer):
    def __init__(self, items_path, discard_threshold, number_of_sentences_in_summary):
        super().__init__(items_path, discard_threshold, number_of_sentences_in_summary)

    def _get_item(self, item_dir: str) -> Item:
        
        try:
            item = super()._get_item(item_dir)
            item.clusters = np.load(item_dir + "/clusters.npy")
            return item
        except:
            return None
    
    def _cut_label(self, item, n_clusters) -> list:
        """
        Given a cluster hiearchy, this method will return n labels.
        """
        pass