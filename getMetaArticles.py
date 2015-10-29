from bs4 import BeautifulSoup
import os
import reader
import re
#We get meta articles from the Oxford Journal by searching for "cancer meta analysis"
metaList = "oxfordJournalMeta.txt"
baseURL = "http://jnci.oxfordjournals.org"

'''
oxfordJournalMeta.txt contains URLs of full meta articles in the Oxford Journals.
Adds the URL to the text file.
'''
def addMetaURL(url):
    newFile = open(metaList, 'a')
    newFile.write(url)
    newFile.write("\n")
    newFile.close()
'''
Removes duplicate article URLs from the file
'''
def removeMetaDuplicates():
    lines = open(metaList, 'r').readlines()
    lines_set = set(lines)
    out  = open(metaList, 'w')
    for line in lines_set:
        out.write(line)

'''
url is a search result on Oxford Journals with meta articles.
Scans the search results and adds all meta article urls to the list.
'''
def addAllLinks(url):
    source = reader.readURL(url)
    soup = BeautifulSoup(source)
    links = soup.findAll("a", {"rel":"full-text"})
    for link in links:
        url = link['href'].split("?sid")[0] #getting rid of search id
        articleURL = baseURL + url
        addMetaURL(articleURL)
    removeMetaDuplicates()

#addAllLinks(url)

'''
Give a URL for an article, creates a new file in meta.
File named after the article title.
First line is url.
Remainder of file is the url page source.
'''
def writeSource(url, source):
    metaFolder = 'meta'
    soup = BeautifulSoup(source)
    if soup.title is not None:
        title = cleanTitle(soup.title.string)
        newName = '{}/{}.txt'.format(metaFolder,title)
        if not os.path.isfile(newName):
            newFile = open(newName, 'w')
            newFile.write(url)
            newFile.write("\n")
            newFile.write(source)
            newFile.close()

'''
Makes a title into a valid filename
'''
def cleanTitle(title):
    title = title.strip()
    title = re.sub('[^\w\-_\. ]', ' ', title)
    return title
'''
Reads list of urls from a text file.
'''
def readMeta():
    lines = [line.rstrip('\n') for line in open(metaList)]
    for i in range(len(lines)):
        link = lines[i]
        source = reader.readURL(link)
        writeSource(link, source)

readMeta()


