from bs4 import BeautifulSoup
import os
import reader
import parseReference
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
   # url = 'http://jnci.oxfordjournals.org/search?fulltext=' + query + '&hits=25&submit=yes' #search oxford journals
    url = 'http://www.ncbi.nlm.nih.gov/pmc/?term='+query #search pubmed
    return url

#Gets a list of all article titles
def getTitles(url):
    source = reader.readURL(url)
    soup = BeautifulSoup(source)
    #links = soup.findAll("span", {"class":"cit-title"}) #oxford journals
    links = soup.findAll("div", {"class":"title"}) #pubmed
    links = map(parseReference.removeTags, links)
    return links

#test = 'Meta-Analysis of Soy Intake and Breast Cancer Risk.txt'
for fileName in os.listdir(os.getcwd()+"/meta"):
    if ".txt" in fileName and len(fileName) > 8: #HACKY, FIX
        query = findKeyWord(fileName) 
        url = generateURL(query)
        print url
        searchResults = getTitles(url)
        metaReferences = parseReference.getMetaReferences(fileName)
        for meta in metaReferences:
            for result in searchResults:
                if result in meta:
                    print result
#print getTitles(testURL)
