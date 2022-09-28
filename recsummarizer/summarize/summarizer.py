import pandas as pd
import numpy as np

from .item import Item

class Summarizer(object):
    def __init__(self, items_path, discard_threshold, number_of_sentences_in_summary):
        self._items_path = items_path
        self._discard_threshold = discard_threshold
        self._number_of_sentences_in_summary = number_of_sentences_in_summary
        
    def summarize(self, item_id):
        pass
    
    def _get_item(self, item_dir: str) -> Item:
        
        try:
            centroid = np.load(item_dir + "/centroid.npy")

            aspects_df = pd.read_csv(item_dir + "/aspects.csv")

            sentences_df = pd.read_csv(item_dir + "/filtered_sentences.csv")

            sentences_df['embeddings'] = pd.read_csv(item_dir + "/embeddings_sentences.csv").values.tolist()

            return Item(centroid, aspects_df, sentences_df)
        except:
            return None
    
    def _summary_sentences(self, item):
        item.sentences_df['score'] = 0.0
        
        for i, row in item.sentences_df.iterrows():
            score = self._cosine_similarity(item.centroid, item.sentences_df['embeddings'][i])
            item.sentences_df.at[i, 'score'] = score

        item.sentences_df.sort_values(by=['score'], ascending=False, inplace=True)

        summary = self._sentence_selection(item.sentences_df, item.aspects)
        
        return [sentence[0] for sentence in summary]
    
    def _sentence_selection(self, sorted_sentences_by_score, aspects):
        
        sorted_sentences_by_score = sorted_sentences_by_score.values.tolist()
        sentences_in_summary = [sorted_sentences_by_score[0]]        
        number_chosen_sentences = len(sentences_in_summary)

        for candidate_sentence in sorted_sentences_by_score[1:]:

            discard = False
            
            for chosen_sentence in sentences_in_summary:
                current_score = self._cosine_similarity(candidate_sentence[2], chosen_sentence[2])
                if current_score >= self._discard_threshold:
                    discard = True
                    break

            if not discard:
                for a in aspects:
                    if a in candidate_sentence[0].lower():
                        sentences_in_summary.append(candidate_sentence)
                        number_chosen_sentences += 1
                        break

                if number_chosen_sentences >= self._number_of_sentences_in_summary:
                    return sentences_in_summary

        return sentences_in_summary
    
    def _cosine_similarity(self, centroid_embbeding, sentence_embbeding):

        centroid_norm = np.linalg.norm(centroid_embbeding, ord= 2)
        sentence_embbeding_norm = np.linalg.norm(sentence_embbeding, ord= 2)

        if centroid_norm == 0 or sentence_embbeding_norm == 0:
            return np.nan

        dot_product_embbedings = np.dot(centroid_embbeding, sentence_embbeding)
        cosine_denominator = centroid_norm * sentence_embbeding_norm
        cosine_similarity = dot_product_embbedings / cosine_denominator

        return cosine_similarity
