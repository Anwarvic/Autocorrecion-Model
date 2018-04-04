import pickle
from collections import defaultdict



UnigramCounts = pickle.load(open('data/grammarly_wikitionary.pickle', 'rb')) #dict
vocabulary = UnigramCounts.keys()
edit_table = defaultdict(set)
with open('data/count_1edit.txt') as fin:
    for line in fin:
        ch_tuple, count = line.split('\t')
        first, second = ch_tuple.split('|')
        if first != ' ':
            edit_table[first.lower()].add(second)
print ("Done Reading...")

def levenstein1(word_1):
    #Return all strings that are one edit away from this word.
    # ---------------- HELPFUL FUNCTION ----------------
    def split_word(wrd):
        #Return a list of all possible (first, rest) character pairs that comprise word.
        return [(wrd[:i], wrd[i:]) 
                for i in range(len(wrd)+1)]
    # --------------------------------------------------
    alphabet = "abcdefghijklmnopqrstuvwxyz'"
    pairs = split_word(word_1)
    replaces = [word_1.replace(ch, sub) for ch in word_1 for sub in edit_table[ch]]
    deletes = [a+b[1:] for (a, b) in pairs if b]
    transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
    inserts = [a+c+b for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def levenstein2(word_2):
    #Return all strings that are two edits away from this word.
    return {e2 for e1 in levenstein1(word_2) for e2 in levenstein1(e1)}

def known(words):
    #Return a set of the words subset that are actually in the vocabulary.
    return {w for w in words if w.lower() in vocabulary}

# print len(levenstein2('saticfay'))

print (known(levenstein2('saticfay')))