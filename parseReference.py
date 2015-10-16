from bs4 import BeautifulSoup
import urllib2
import requests
import urllib
import re
import html5lib
import os

'''
Given a reference, get the author and itlte.
'''
def parseReference(ref):
    split = ref.split(".")
    author = split[0]
    title = split[1]

'''
Given a URL and the HTML at the URL, returns all of the references, including the HTML tags.
'''
#PROBLEM: each URL has different format, unnecessary HTML code, TO-DO automatically detect this?
def findReferences(url, text):
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
        oxfordJournals: soup.findAll("div", {"class": "cit-metadata"}),
        springer: soup.findAll("div", {"class", "CitationContent"})
    }

    for site in sites.keys():
        if site in url:
            return sites[site]
    return 'ERROR: site not seen before'

'''
Removes all html tags from a bs4 tag.
'''
def removeTags(htmlTag):
    string = str(htmlTag).rstrip('\t\n\r')
    tag = re.compile(r'<[^>]+>')
    return tag.sub('', string)

folder = 'meta'
'''
Given a an article (url first line, html in the rest), returns the list of all references in a human-readable form.
'''
def getAllMetaRefs():
    for f in os.listdir(folder):
        if ".txt" in f:
            getAllRefs(f)


def getAllRefs(name):
    newFile = open('{}/{}'.format(folder, name), 'r')
    url = newFile.readline()
    text = newFile.read()
    refs = findReferences(url, text)
    for i in refs:
        print removeTags(i)
    newFile.close()

getAllMetaRefs()
