from bs4 import BeautifulSoup
import os
import reader
#Given a title, extracts the key words of the title
def getTopic(title):
    return title
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