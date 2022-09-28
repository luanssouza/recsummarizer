
class Persistence(object):
    
    def __init__(self, dist_path: str, embedding):
        self._dist_path = dist_path
        self._embedding = embedding

    def persist_movie(self, movie):
        """
        This function creates a folder with movie name and save the preprocessed movie files.

        Parameters
        ----------
        movie : Movie
            A preprocessed movie instance.

        Returns
        ----------
        None.

        """
        pass
