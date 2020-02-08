import unicodedata
from nltk.tokenize.treebank import TreebankWordTokenizer
import sys

# Normalize text by mapping non-ascii characters to approximate ascii. e.g., beyonc'{e} becomes beyonce
def normalize_unicode(text):
  #return text.encode('ascii', 'ignore')
  return unicodedata.normalize('NFD', text).encode('ascii', 'ignore')

# Standard word tokenizer.
_treebank_word_tokenize = TreebankWordTokenizer().tokenize

def word_tokenize(text, language='english'):
    """
    Return a tokenized copy of *text*,
    using NLTK's recommended word tokenizer
    (currently :class:`.TreebankWordTokenizer`
    along with :class:`.PunktSentenceTokenizer`
    for the specified language).
    :param text: text to split into sentences
    :param language: the model name in the Punkt corpus
    """
    if sys.version_info[0] < 3:
        return [token for token in _treebank_word_tokenize(text)]
    else:
        return [token for token in _treebank_word_tokenize(text.decode("UTF-8"))]

def get_ngrams(n, tokens, separator=" "):
  if n == 0:
    return [" ".join(tokens)]

  # extract each n-token sequence from entire sequence of tokens
  ngrams = []
  for i, token in enumerate(tokens):
    # first k-gram at position k-1
    if i >= n - 1:
      ngrams.append(separator.join(tokens[i - n + 1:i + 1]))
  return ngrams

def split_sent(sent, qrepr, ngram_size=3):
    """
    Split sentence into core elements, depending on the query representation.
    :param sent: sent as string
    :param qrepr: query representation (e.g., word or char).
    :param is_already_tokenized: use True if ``query'' was generated using vocab_inv (possibly using defeaturize),
            so we do not need to preprocess text
    :return:
    """
    if qrepr == "word":
        return word_tokenize(sent)
    elif qrepr == "char":
        cs = list(sent)
        return [c for i, c in enumerate(cs) if i == 0 or c != " " or cs[i - 1] != " "]
    elif qrepr.endswith("gram"):
        if sys.version_info[0] < 3:
            return get_ngrams(ngram_size, split_sent("#"+sent+"#", "char"), separator="")
        else:
            return get_ngrams(ngram_size, split_sent("#" + sent.decode("utf-8") + "#", "char"), separator="")
    else:
        raise Exception("Unrecognized representation %s!" % qrepr)

