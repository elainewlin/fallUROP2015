import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import sys
reload(sys) #Helps encode website data 
sys.setdefaultencoding('utf8')
'''
Reads source code of a url
'''
def readURL(url):
    hdr = {'User-Agent': 'Mozilla/5.0'} #bypasses some security constraints
    req = urllib2.Request(url, headers = hdr)
    f = urllib2.urlopen(req)           
    source = f.read()  
    return source

'''
If reading the using urllib2 doesn't give the full page source, use selenium
to get the URL page source as it shows up in the browser.
'''
def readURLSelenium(url):

    chromedriver = os.getcwd()+"chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver)
    browser.get(url)
    browser.implicitly_wait(10)
    
    source = browser.page_source
    writeFile(url, source)
    browser.close()

'''
Given a file with first line URL, rest HTML, returns the HTML portion of the file.
'''
def readFile(fileName):
    newFile = open(fileName, 'r')
    newFile.readline()
    text = newFile.read()
    newFile.close()
    return text