import os
import re
import sys
import porter
from numpy import zeros, dot
from numpy.linalg import norm


class Sim:
    file = os.path.join(os.path.dirname(__file__), 'english.stop')
    stop_words = [w.strip() for w in open(file, 'r').readlines()]
    splitter = re.compile("[a-z\-']+", re.I)
    stemmer = porter.PorterStemmer()

    def add_word_count(self, word, word_count_dict):
        """Filter stop words, stem the word and add to word_count_dict"""
        w = word.lower()
        if w not in self.stop_words:
            w = self.stemmer.stem(w, 0, len(w) - 1)
            word_count_dict.setdefault(w, 0)
            # count not needed but kept for the future
            word_count_dict[w] += 1

    def build_vector(self, doc, word_dict):
        """Return a word vector of the doc"""
        v = zeros(len(word_dict))
        for w in self.splitter.findall(doc):
            w = w.lower()
            # word_data = (index, count)
            word_data = word_dict.get(self.stemmer.stem(
                w, 0, len(w) - 1), None)
            if word_data:
                v[word_data[0]] = 1
        return v

    def compare(self, doc1, doc2):
        """Return doc similarity in float or -1 if N/A"""
        # word => count
        word_count_dict = dict()
        for doc in [doc1, doc2]:
            for w in self.splitter.findall(doc):
                self.add_word_count(w, word_count_dict)

        # sorted word => (index, count)
        word_dict = dict()
        words = word_count_dict.keys()
        words.sort()
        # TODO test range vs xrange
        for i in range(len(words)):
            word_dict[words[i]] = (i, word_count_dict[words[i]])

        # Keep word_dict in memory and delete the rest
        del words
        del word_count_dict

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
    doc1 = sim.read_doc_from_file(sys.argv[1])
    doc1 = sim.read_doc_from_file(sys.argv[2])

    #doc1="I like to eat chicken\nnoodle soup."
    #doc2="I have read the book \"Chicken noodle soup for the soul\"."

    print "Doc1: %s\n\nDoc2: %s\n" % (doc1, doc2)
    print "Similarity = %s" % sim.compare(doc1, doc2)
