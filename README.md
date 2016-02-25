# summarize.py
Simple python script using Nltk to summarize articles from the web.

Based on the numerous paper and example found on the Internet (i.e. http://thetokenizer.com/2013/04/28/build-your-own-summary-tool/).

Usage:

Install NLTK: 
 - http://www.nltk.org/install.html
 
Download the corpora files and trained model:


$ python

\>\>\> import nltk

\>\>\> nltk.download('all')


Now you can pass any url on the commandline to be summarized i.e.:

./summarize.py http://arstechnica.com/information-technology/2015/08/netflix-shuts-down-its-last-data-center-but-still-runs-a-big-it-operation/

It supports also multiple language as based on NLTK StopWords corpus.
