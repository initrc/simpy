#!/usr/bin/env python

import os
import re
import sys
import time
import porter
from numpy import zeros, dot
from numpy.linalg import norm


class Sim:
    file = os.path.join(os.path.dirname(__file__), 'english.stop')
    stop_words = [w.strip() for w in open(file, 'r').readlines()]
    splitter = re.compile("[a-z\-']+", re.I)
    stemmer = porter.PorterStemmer()

    def build_word_dict(self, doc1, doc2):
        """Return a dict that maps filtered and stemmed word to id"""
        word_dict = dict()
        id = 0
        for doc in [doc1, doc2]:
            for w in self.splitter.findall(doc):
                w = w.lower()
                if w not in self.stop_words:
                    w = self.stemmer.stem(w, 0, len(w) - 1)
                    if w not in word_dict:
                        word_dict[w] = id
                        id += 1
        return word_dict

    def build_vector(self, doc, word_dict):
        """Return a word vector of the doc"""
        v = zeros(len(word_dict))
        for w in self.splitter.findall(doc):
            w = w.lower()
            w = self.stemmer.stem(w, 0, len(w) - 1)
            if w in word_dict:
                v[word_dict[w]] = 1
        return v

    def compare(self, doc1, doc2):
        """Return doc similarity in float or -1 if N/A"""
        # build word_dict: word => id
        word_dict = self.build_word_dict(doc1, doc2)
        # build and normalize word vectors
        v1 = self.build_vector(doc1, word_dict)
        v2 = self.build_vector(doc2, word_dict)
        norm1 = norm(v1)
        norm2 = norm(v2)
        if (norm1 == 0 or norm2 == 0):
            return -1
        else:
            return float(dot(v1, v2) / (norm(v1) * norm(v2)))

    def read_doc_from_file(self, file):
        """Return doc read from file"""
        try:
            doc = open(file, 'r').read()
        except:
            print "Error could not open file"
        return doc

if __name__ == '__main__':
    print "Calculating similarity..."
    sim = Sim()
    start = time.time()
    doc1 = sim.read_doc_from_file(sys.argv[1])
    doc2 = sim.read_doc_from_file(sys.argv[2])
    similarity = sim.compare(doc1, doc2)
    end = time.time()
    print "Similarity = %s\n%fs" % (similarity, end - start)
