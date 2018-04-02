import re
import pickle
from collections import Counter



COUNTS = pickle.load(open("data/grammarly_wikitionary.pickle",'r'))
vocabulary = set(COUNTS.keys())
BI_COUNTS = pickle.load(open("data/count_2w.pickle",'r'))



def known(words):
    #Return a set of the words subset that are actually in the vocabulary.
    return {w for w in words if w in vocabulary or w.lower() in vocabulary}



def correct_word(word):
    """
    Find the best spelling correction for this word.
    Prefer edit distance 0, then 1, then 2; otherwise default to word itself.
    """
    # ---------------- HELPFUL FUNCTIONS ----------------
    def edits0(word_0): 
        #Return all strings that are zero edits away from word (i.e., just word itself).
        return {word_0}
    def edits1(word_1):
        #Return all strings that are one edit away from this word.
        # ---------------- HELPFUL FUNCTION ----------------
        def split_word(wrd):
            #Return a list of all possible (first, rest) character pairs that comprise word.
            return [(wrd[:i], wrd[i:]) 
                    for i in range(len(wrd)+1)]
        # --------------------------------------------------
        alphabet = "abcdefghijklmnopqrstuvwxyz'"
        pairs      = split_word(word_1)
        deletes    = [a+b[1:]           for (a, b) in pairs if b]
        transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
        replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
        inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
        return set(deletes + transposes + replaces + inserts)
    def edits2(word_2):
        #Return all strings that are two edits away from this word.
        return {e2 for e1 in edits1(word_2) for e2 in edits1(e1)}
    # ------------------------------------------------
    candidates = known(edits0(word)).union(known(edits1(word)))
    c = Counter({w: COUNTS[w] for w in candidates})
    if c.most_common(1)[0][1] < 100000: #------------------------------> hyper-parameter
        candidates = candidates.union(known(edits2(word))) 
        c = Counter({w: COUNTS[w] for w in candidates})
    return c.most_common(100)    #lists of tuple


def BI_COUNTS_exists(bi):
    return BI_COUNTS.get(bi, 0)





def correct_sentence(sentence):
    output_sentence = ""
    start_word = "<s>"
    for wrd in sentence.split(" "):
        if known(wrd): #-----------------------> REMOVE MAYBE
            continue
        candidates = set([start_word+' '+word for word, count in correct_word(wrd)])
        print candidates
    #     start_word = winner
    #     #print start_word
    #     output_sentence += winner + " "
    # return output_sentence


def correct_text(text):
    #Correct all the words within a text, returning the corrected text.
    def correct_match(match):
        #Spell-correct word in match, and preserve proper upper/lower/title case.
        def case_of(text):
            #Return the case-function appropriate for text: upper, lower, title, or just str.
            return (str.upper if text.isupper() else
                    str.lower if text.islower() else
                    str.title if text.istitle() else
                    str)
        word = match.group()
        return case_of(word)(correct_sentence(word.lower()))
    return re.sub('[a-zA-Z]+', correct_match, text)

