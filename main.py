"""
A spelling corrector, based on the algorithm presented in "Introduction to
Spelling Correction" by Peter Norvig.

Edited by:
    - Florian Eder      00819174
    - Moritz Enderle
"""
import re
from collections import Counter


def words(text):
    """
    Return all words in text
    :param text: text to be parsed
    :return: list of words
    """
    return re.findall(r'\w+', text.lower())


with open('words.txt', encoding="utf-8") as f:
    WORDS = Counter(words(f.read()))


def probability(_word, _no_words=sum(WORDS.values())):
    """
    Probability of `word`
    :param _word: word to be probed
    :param _no_words: number of words in the counter
    :return probability of `word`
    """
    return WORDS[_word] / _no_words


def correction(_word):
    """
    Most probable spelling correction for word
    :param _word: word to be corrected
    :return most probable spelling correction for word
    """
    return max(candidates(_word), key=probability)


def candidates(_word):
    """
    Generate possible spelling corrections for word
    :param _word: word to be corrected
    :return: list of possible spelling corrections for word
    """
    return known([_word]) or known(edits1(_word)) or known(edits2(_word)) or [_word]


def known(_words):
    """
    The subset of `words` that appear in the dictionary of WORDS
    :param _words: list of words to be checked
    :return: list of words that appear in the dictionary of WORDS
    """
    return set(w for w in _words if w in WORDS)


def edits1(_word):
    """All edits that are one edit away from `word`
    :param _word: word to be corrected
    :return: list of possible spelling corrections for word
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(_word[:i], _word[i:]) for i in range(len(_word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(_word):
    """
    All edits that are two edits away from `word`
    :param _word: word to be corrected
    :return: list of possible spelling corrections for word
    """
    return (e2 for e1 in edits1(_word) for e2 in edits1(e1))
