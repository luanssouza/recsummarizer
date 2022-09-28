from summarizer.summarizer import Summarizer

class SummarizerBaseline(Summarizer):
    def __init__(self, items_path, discard_threshold, number_of_sentences_in_summary):
        super().__init__(items_path, discard_threshold, number_of_sentences_in_summary)
    
    def summarize(self, item_id:int) -> list:
        item_dir = self._items_path + "{0}".format(item_id)
        item = self._get_item(item_dir)
        if not item:
            return []
        item.aspects = item.aspects_df['aspect'].tolist()
        return self._summary_sentences(item)