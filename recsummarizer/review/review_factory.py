from .base_review import Review
from .dat_review import DatReview
from .xml_review import XmlReview

def review_factory(file:str, review_file_type:str = "xml") -> Review:
    """
    Review Factory Method

    Parameters
    ----------
    file : str
        Given a file that represents a review, this function instantiates review objects (and consequently, sentence objects) by parsing the tree.

    review_tyoe : str
        dat or xml.
        Default xml.

    Returns:
    ----------
    A Review instance.
    """

    reviews = {
        "dat": DatReview,
        "xml": XmlReview
    }

    return reviews[review_file_type](file)