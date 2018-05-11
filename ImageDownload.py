import csv
import urllib
import urllib.parse
import urllib.request
import time
import sys


def ScrapeImage():

    with open('comicImg.csv') as csvfile:
        for row in csvfile:
                url = "http://www.comicbookdb.com/graphics/comic_graphics/" + row
                filename = url[url.rfind('/') + 1:]
                filename.strip()
                urllib.request.urlretrieve("http://www.comicbookdb.com/graphics/comic_graphics/"+row, "ComicImage\\"+filename )
                time.sleep(1)

ScrapeImage()

row = "1/1/1_20050917191424_thumb.jpg"
url = "http://www.comicbookdb.com/graphics/comic_graphics/" + row
filename = url[url.rfind('/') + 1:]
#url = "http://www.comicbookdb.com/graphics/comic_graphics/" + row
#urllib.request.urlretrieve(url, "ComicImage/"+filename )
