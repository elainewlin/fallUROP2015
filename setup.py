from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import sys
reload(sys) #Helps encode website data
sys.setdefaultencoding('utf8')
 
folder = 'meta'
'''
Given the title of an article and the url, creates a new file in meta folder.
File named after the article title.
First line is url.
Remainder of file is the url page source.
'''
def createFileName(url):
    chromedriver = "/Users/elainelin/Documents/fallUROP2015/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)
    browser.get(url)
    browser.implicitly_wait(10)
    
    source = browser.page_source
    soup = BeautifulSoup(source)
    if soup.title is not None:
        title = soup.title.string

        newName = '{}/{}.txt'.format(folder,title)
        if not os.path.isfile(newName):
            newFile = open(newName, 'w')
            newFile.write(url)
            newFile.write("\n")
            newFile.write(source)
            newFile.close()
    browser.close()

def readMeta():
    lines = [line.rstrip('\n') for line in open('links.txt')]
    for i in range(len(lines)):
        if i % 3 == 0:
            link = lines[i]
            title = lines[i+1]
            createFileName(link)
def readURL(url):
    hdr = {'User-Agent': 'Chrome/45.0.2454.101'}
    req = urllib2.Request(url, headers = hdr)
    f = urllib2.urlopen(req)           
    myfile = f.read()  
    return myfile

readMeta()