from bs4 import BeautifulSoup
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
     #regular expression to deal with unicode??
    return string

'''
Given a file name, returns a list of all references at the end of an article.
input: name of the file
output: list of references at the end of the article
'''
def findEndRef(fileName):
    text = reader.readFile(fileName)
    soup = BeautifulSoup(text, 'html5lib')
    endRefs = soup.findAll("div", {"class": "cit-metadata"})
    endRefs = map(removeTags, endRefs)
    return endRefs

'''
Given the HTML code of an article, returns a list the numbers to the references made in the article.
input: name of the file
ouput: list of the in text citations to articles i.e. [1,2-4,5]
'''
def findInArticleRef(fileName):
    text = reader.readFile(fileName)
    soup = BeautifulSoup(text, 'html5lib')
    inText = soup.findAll("a", {"class", "xref-bibr"})
    inText = map(removeTags, inText)
    inText = map(lambda string: re.sub('\xe2\x80\x93',"-", string), inText) #deals with unicode dashes
    inText = map(lambda string: re.sub(r'[^0-9/-]+','',string), inText) #deletes not numbers
    return inText

'''
Get the reference numbers of all of the articles referenced within the meta article
input: list of the in text citations to articles
output: dictionary where keys are articles referenced, values are how many times each article occurred
'''
def getArticleCounts(articleRefs):
    articleCounts = {}
    def incrementKeyCount(key):
        if key in articleCounts:
            articleCounts[key] += 1
        else:
            articleCounts[key] = 1

    def convertInt(string):
        return [int(s) for s in str.split() if s.isdigit()]
    for a in articleRefs:
        if '-' in a: #dealing with ranges such as 9-13
            first = int(a.split('-')[0])
            last = int(a.split('-')[1])
            for i in xrange(first, last+1):
                incrementKeyCount(i)
        else:
            incrementKeyCount(int(a))
    return articleCounts

'''
Returns the list of all numbers referenced in the article that occur more than once.
We say that these are the articles being summarized.
'''
def getMetaNums(fileName):
    allArticles = getArticleCounts(findInArticleRef(fileName))
    meta = [article for article in allArticles if allArticles[article] > 1]
    return meta

'''
Given a file name, returns the list of all meta articles referenced
'''
def getMetaReferences(fileName):
    folder = 'meta'
    fileName = '{}/{}'.format(folder, fileName)
    metaNums = getMetaNums(fileName)
    allReferences = findEndRef(fileName)
    metaReferences = [allReferences[num-1] for num in metaNums] #metaNums is 1 indexed, arrays are 0 indexed
    return metaReferences