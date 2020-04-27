import os
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from time import gmtime, strftime

filePath = r'C:\Users\meysam\Meysam Test Codes\SpringerBookDownloader\web_scraping_springer_free_books_url.txt'
folderLocation = r'C:\Users\meysam\Meysam Test Codes\SpringerBookDownloader\DownloadedBooks'

print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

with open(filePath, encoding='UTF-8') as file:
    for line in file:
        #print(line)
        urls = re.findall('http://[^\s]+', line)
        if urls != []:
            #print(urls)
            r = requests.get(urls[0])
            #print('URL content:\n', r.content)
            redirectURL = r.url
            #print('redirect URL: ', redirectURL)
            bookID = r.url.rsplit('/', 1)[1]
            #print('bookID:', bookID)
            soup = bs(r.content, 'lxml')
            pageTitle = soup.select_one('title').text
            #print('pageTitle: ', pageTitle)
            pageTitleFileName = pageTitle.rsplit(' |', 1)[0].replace(' ', '_').replace('/', '_') + '.pdf'
            #print('pageTitleFileName: ', pageTitleFileName)
            fileName = os.path.join(folderLocation, pageTitleFileName)
            #print('fileName: ', fileName)
            with open(fileName, 'wb') as f:
                downloadURL = urljoin("https://link.springer.com/content/pdf/", bookID)
                #print('downloadURL: ', downloadURL)
                f.write(requests.get(downloadURL + '.pdf').content)
                print('Enjoy reading the', pageTitle.rsplit(' |', 1)[0] , 'It is downloaded successfully!')

print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))