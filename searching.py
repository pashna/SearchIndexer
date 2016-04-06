from utils.utils import load_obj
from Engine.Searcher import Searcher
import sys

if __name__ == "__main__":

    requests = []
    for line in sys.stdin:
        line = line.replace("\n", "")
        requests.append(line.split(' & '))

    r_index = load_obj("optimized_index")
    searcher = Searcher(r_index)
    result_doc_matrix = []

    for request in requests:
       result_doc_matrix.append(searcher.and_words(request[0], request[1]))

    r_index = None
    searcher = None

    docs = load_obj("documents")
    for result_docs in result_doc_matrix:
        print len(result_docs)
        for doc_id in result_docs:
            print docs[doc_id]


    """
    print len(r_index["fit"]["docs"])
    print searcher.and_words("fit", "fit")
    """