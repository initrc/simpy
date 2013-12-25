#!/usr/bin/env python

import os
import re
import sys
import time
from .porter import PorterStemmer
from numpy import zeros, dot
from numpy.linalg import norm


class Sim:
    file = os.path.join(os.path.dirname(__file__), 'english.stop')
    stop_words = [w.strip() for w in open(file, 'r').readlines()]
    splitter = re.compile("[a-z\-']+", re.I)
    stemmer = PorterStemmer()

    def build_word_dict(self, docs, word_sets):
        """Return a dict that maps filtered and stemmed word to id"""
        word_dict = {}
        id = 0
        for i in range(len(docs)):
            for w in self.splitter.findall(docs[i]):
                w = w.lower()
                if w not in self.stop_words:
                    w = self.stemmer.stem(w, 0, len(w) - 1)
                    if w not in word_dict:
                        word_dict[w] = id
                        id += 1
                    if w not in word_sets[i]:
                        word_sets[i].add(w)
        return word_dict

    def build_vector(self, doc, word_dict, word_set):
        """Return a word vector of the doc"""
        v = zeros(len(word_dict))
        for w in word_set:
            v[word_dict[w]] = 1
        return v

    def compare(self, docs):
        """Return doc similarity in float or -1 if N/A"""
        # support only 2 docs
        assert len(docs) == 2
        # build word_dict: word => id
        word_sets = [set(), set()]
        word_dict = self.build_word_dict(docs, word_sets)
        # build and normalize word vectors
        vecs, norms = [None, None], [None, None]
        for i in range(len(docs)):
            vecs[i] = self.build_vector(docs[i], word_dict, word_sets[i])
            norms[i] = norm(vecs[i])
        if (norms[0] == 0 or norms[1] == 0):
            return -1
        else:
            return dot(vecs[0], vecs[1]) / (norms[0] * norms[1])

    def read_doc_from_file(self, file):
        """Return doc read from file"""
        try:
            doc = open(file, 'r').read()
        except:
            print("Error could not open file")
        return doc

if __name__ == '__main__':
    """
    python -m algorithm.sim algorithm/text_hamlet.txt
    algorithm/text_othello.txt
    """
    print("Calculating similarity...")
    sim = Sim()
    start = time.time()
    docs = [sim.read_doc_from_file(sys.argv[1]),
            sim.read_doc_from_file(sys.argv[2])]
    similarity = sim.compare(docs)
    end = time.time()
    print("Similarity = %s\n%fs" % (similarity, end - start))
