#!/usr/bin/env python

##########################################
#
# Summarize.py: Simple python script using Nltk to summarize articles from the web. 
#               Based on the numerous paper and example found on the Internet (i.e. http://thetokenizer.com/2013/04/28/build-your-own-summary-tool/)
#
# Author: Cosimo Iaia <cosimo.iaia@gmail.com>
# Date: 20/02/2016
#
# This file is distribuited under the terms of GNU General Public
#
#########################################



from __future__ import print_function

import codecs
import nltk
from nltk.corpus import stopwords
import re
import string
import sys

_IS_PYTHON_3 = sys.version_info.major == 3

stop_words = stopwords.words('english')

# The low end of shared words to consider
LOWER_BOUND = .20

# The high end, since anything above this is probably SEO garbage or a
# duplicate sentence
UPPER_BOUND = .90


def u(s):
    """Function found on the web. Damn Unicode strings. JMC"""
    if _IS_PYTHON_3 or type(s) == unicode:
        return s
    else:
        return codecs.unicode_escape_decode(s)[0]


def is_unimportant(word):
    """words that can be safely ignored"""
    return word in ['.', '!', ',', ] or '\'' in word or word in stop_words


def only_important(sent):
    return filter(lambda w: not is_unimportant(w), sent)


def compare_sentences(first, second):
    """Compare two word-tokenized sentences for shared words"""
    if not len(first) or not len(second):
        return 0
    return len(set(only_important(first)) & set(only_important(second))) / ((len(first) + len(second)) / 2.0)


def compare_with_bounds(first, second):
    """Wrap the comparison between the bounds """
    result = compare_sentences(first, second)
    if result <= LOWER_BOUND or result >= UPPER_BOUND:
        result = 0
    return result


def calculate_score(origin, sentences):
    """Calculate the average score of the sentence compared to all the others, within the bounds"""
    result = 0
    if len(origin):
        result=sum(compare_with_bounds(origin, sentence) for sentence in sentences) / float(len(sentences))
    return result



def find_likely_body(b):
    """Find the tag with the most directly-descended <p> tags"""
    return max(b.find_all(), key=lambda t: len(t.find_all('p', recursive=False)))


class Summary(object):

    def __init__(self, url, article_html, title, summaries):
        self.url = url
        self.article_html = article_html
        self.title = title
        self.summaries = summaries

    def __repr__(self):
        return u('Summary({}, {}, {}, {})').format(repr(self.url), repr(self.article_html), repr(self.title), repr(self.summaries))

    def __unicode__(self):
        return u('{} - {}\n\n{}').format(self.title, self.url, '\n'.join(self.summaries))

    def __str__(self):
        if _IS_PYTHON_3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode('utf8')


def summarize_block(block):
    """Return the sentence that best summarizes block"""
    if not block:
        return None
    sents = nltk.sent_tokenize(block)
    word_sents = list(map(nltk.word_tokenize, sents))
    d = dict((calculate_score(word_sent, word_sents), sent)
             for sent, word_sent in zip(sents, word_sents))
    return d[max(d.keys())]


def summarize_blocks(blocks):
    summaries = [re.sub('\s+', ' ', summarize_block(block) or '').strip()
                 for block in blocks]
    # deduplicate and preserve order
    summaries = sorted(set(summaries), key=summaries.index)
    return [u(re.sub('\s+', ' ', summary.strip())) for summary in summaries if any(c.lower() in string.ascii_lowercase for c in summary)]


def summarize_url(addr):
    import bs4
    import requests

    html = bs4.BeautifulSoup(requests.get(addr).text)
    b = find_likely_body(html)
    summaries = summarize_blocks(map(lambda p: p.text, b.find_all('p')))
    return Summary(addr, b, html.title.text if html.title else None, summaries)




if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(summarize_url(sys.argv[1]))
        sys.exit(0)
    else:
        print('Usage: summarize <URL>')
        sys.exit(1)
