from utils.utils import load_obj
from Engine.Searcher import Searcher
import sys

if __name__ == "__main__":
    r_index = load_obj("optimized_index")
    searcher = Searcher(r_index)
    result_doc_id = []

    print searcher.and_words("love", "sex")