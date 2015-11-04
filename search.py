from bs4 import BeautifulSoup
import os
import reader
from parseReference import removeTags

'''
annotatedMeta.tsv contains article titles and the human-annotated key words
Given a title of an article, returns the key words to search for
'''
def findKeyWord(title):
    lines = [line.strip('\r\n') for line in open('annotated meta.tsv')]
    for line in lines:
        if title in line:
            return line.split('\t')[1]

#Given a search query, generates a URL to search for it
def generateURL(query):
    """
    A url in the required format is generated.
    """
    query = '+'.join(query.split())
    url = 'http://jnci.oxfordjournals.org/search?fulltext=' + query + '&hits=25&submit=yes'
    return url

#Gets a list of all article titles
def getTitles(url):
    source = reader.readURL(url)
    soup = BeautifulSoup(source)
    links = soup.findAll("span", {"class":"cit-title"})
    return links

query = 'breast cancer'
url = generateURL(query)
print url
print map(removeTags,getTitles(url))