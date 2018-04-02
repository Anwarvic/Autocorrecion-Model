from collections import defaultdict


class EditModel:
    def __init__(self):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.edit_table = self.read_edit_table('data/count_1edit.txt')

    def read_edit_table(self, file_name):
        """
        Reads in the string edit counts file. Stores a dictionary of tuples
        (s1,s2) -> count.
        """
        edit_table = defaultdict(lambda: 0)
        f = file(file_name)
        for line in f:
            contents = line.split('\t')
            edit_table[contents[0]] = int(contents[1])
        return edit_table

    def edit_count(self, s1, s2):
        """Returns how many times substring s1 is edited as s2."""  
        return self.edit_table[s1 + "|" + s2]

    def editProbabilities(self, word):
        """
        Computes p(x|word) edit model for a given word. 
        Returns a dictionary mapping x -> p(x|word).
        """
        s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        counts = defaultdict(lambda: 0)
        # deletes
        for a, b in s:
            if b and a + b[1:] in self.vocabulary:
                tail = ''
                if len(a) > 0:
                    tail = a[-1]
                original = tail + b[0]
                replacement = tail
                count = self.edit_count(original, replacement)
                if count:
                    counts[a + b[1:]] += count
        # transposes
        for a, b in s:
            if len(b)>1 and a + b[1] + b[0] + b[2:] in self.vocabulary:
                # new word is a + b[1] + b[0] + b[2:]
                # edit is b[0]b[1] -> b[1]b[0]
                original = b[0] + b[1]
                replacement = b[1] + b[0]
                count = self.edit_count(original, replacement)
                if count:
                    counts[a + b[1] + b[0] + b[2:]] += count
        # replaces
        for a, b in s:
            if b: 
                for c in self.alphabet:
                    if a + c + b[1:] in self.vocabulary:
                        # new word is a + c + b[1:]. 
                        original = b[0]
                        replacement = c
                        count = self.edit_count(original, replacement)
                        if count:
                            counts[a + c + b[1:]] += count
        # inserts
        for a, b in s:
            for c in self.alphabet:
                if a + c + b in self.vocabulary:
                    # new word is a + c + b. 
                    tail = ''
                    if len(a) > 0:
                        tail = a[-1]
                    original = tail
                    replacement = tail + c
                    count = self.edit_count(original, replacement)
                    if count:
                        counts[a + c + b] += count
      
        # normalize counts. sum over them all, divide each entry by sum.
        total = 0.0
        for a,b in counts.iteritems():
            total += b
        # self count
        selfCount = max(9*total, 1)
        counts[word] = selfCount
        total += selfCount
        probs = {}
        if(total != 0.0): 
            for a,b in counts.iteritems():
                probs[a] = float(b)/total
        return probs
        

  
  


def dameraulevenshtein(seq1, seq2):
    # The following "function" calculates the Levenshtein distance between two strings. 
    # It's taken from http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance
    # MIT license.
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
            # This block deals with transpositions
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x-1] == seq2[y] and seq1[x] != seq2[y]):
                thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
    return thisrow[len(seq2) - 1]
