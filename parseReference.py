from bs4 import BeautifulSoup
import urllib2
import requests
import re
import html5lib
import os
import reader

'''
Given a URL and the HTML at the URL, returns all of the references, including the HTML tags.
Finds all of the references at the end for general websites
#PROBLEM: each URL has different format, unnecessary HTML code, TO-DO automatically detect this?
def findEndRef(url, text):
    soup = BeautifulSoup(text, 'html5lib')

    pubmed = 'ncbi.nlm.nih.gov/pmc'
    scienceDirect = 'sciencedirect'
    wileyOnline = 'onlinelibrary.wiley'
    bmj = 'bmj'
    oxfordJournals = 'oxfordjournals'
    springer = 'link.springer'

    sites = {
        pubmed: soup.findAll("span", { "class" : "element-citation" }),
        wileyOnline: soup.findAll("cite"),
        scienceDirect: soup.findAll("ul", {"class", "reference"}),
        bmj: soup.findAll("div", {"class": "cit-metadata"}),
        oxfordJournals: soup.findAll("span", {"class": "cit-article-title"}),
        springer: soup.findAll("div", {"class", "CitationContent"})
    }

    for site in sites.keys():
        if site in url:
            return sites[site]
    return 'ERROR: site not seen before'
'''
'''
Removes all html tags and white space from a bs4 tag.
'''
def removeTags(htmlTag):
    string = str(htmlTag)
    tag = re.compile(r'<[^>]+>')
    string = tag.sub('', string)
    string = re.sub('\s+', " ", string) #removes white space
     #regular expression to deal with unicode
    return string

'''
Given a file name, returns a list of all references at the end of an article.
'''
def findEndRef(fileName):
    text = reader.readFile(fileName)
    soup = BeautifulSoup(text, 'html5lib')
    endRefs = soup.findAll("div", {"class": "cit-metadata"})
    endRefs = map(removeTags, endRefs)
    return endRefs

'''
Given the HTML code of an article, returns a list the numbers to the references made in the article.
'''
def findInArticleRef(fileName):
    text = reader.readFile(fileName)
    soup = BeautifulSoup(text, 'html5lib')
    inText = soup.findAll("a", {"class", "xref-bibr"})
    inText = map(removeTags, inText)
    inText = map(lambda string: re.sub('\xe2\x80\x93',"-", string), inText)
    inText = map(lambda string: re.sub(r'[^0-9/-]+','',string), inText)
    return inText


#get the numbers of the references in the article
#PROBLEM: cannot tell which articles are being summarized
def getNums(articleRefs):

    articleRefNums = {}
    def incrementKeyCount(key):
        if key in articleRefNums:
            articleRefNums[key] += 1
        else:
            articleRefNums[key] = 1

    def convertInt(string):
        return [int(s) for s in str.split() if s.isdigit()]
    for a in articleRefs:
        if '-' in a:
            first = int(a.split('-')[0])
            last = int(a.split('-')[1])
            for i in xrange(first, last+1):
                incrementKeyCount(i)
        else:
            incrementKeyCount(int(a))
    return articleRefNums.keys()

folder = 'meta'

'''
annotatedMeta.tsv contains article titles and the human-annotated key words
Given a title of an article, returns the key words
'''
def findKeyWord(title):
    annotated = annotatedMeta.tsv
for f in os.listdir(folder):
    fileName = '{}/{}'.format(folder, f)
    metaName = f.strip(".txt")
    allMetaRefs = [metaName] + findEndRef(fileName)
    inArticleRefs = getNums(findInArticleRef(fileName))
  #  print inArticleRefs
    '''
    print metaName
    print len(allMetaRefs)
    print len(inArticleRefs)
    '''






