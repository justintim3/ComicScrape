#import libraries
import urllib.request as urllib2
import bs4
import re
import time
import csv

# traverses an HTML tag tree via depth first traversal
def Traverse(Tags):
    result = []
    for tag in Tags:
        if tag.string and tag.string.strip():
            result.append(tag.string.strip())
        elif hasattr(tag, "contents") and tag.contents:
            result.extend(Traverse(tag.contents))
        else:
            pass
    return result

# splits a list into a list of sublists based on a lambda that returns a boolean
def HigherOrderListSplit(sequence, l):
    result = []
    g = []
    for element in sequence:
        if l(element):
            result.append(g)
            g = []
        g.append(element)
    return result

def ScrapeComic(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    creators = soup.find_all("td", attrs={"valign": "top", "width": "366", "align": "left"})
    miscellaneous = soup.find_all("td", attrs={"colspan": "3", "valign": "top"})

    # Take out the <div> of name and get its value
    publisher_box = soup.find("a", attrs={"class": "test"})
    series_box = soup.find("span", attrs={"class": "page_headline"})
    issue_box = soup.find("span", attrs={"class": "page_subheadline"})
    creators_box = HigherOrderListSplit (
        Traverse(creators),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension
    miscellaneous_box = HigherOrderListSplit (
        Traverse(miscellaneous),
        lambda x: re.compile(".*:$").match(x)
    )[1:]

    comic = {
        "Publisher" : publisher_box.text.strip(),
        "Issue" : issue_box.text.strip().replace("\"", ""),
        "Series" : series_box.text.strip().split(" - ")[0],
        "Series Number": series_box.text.strip().split(" - ")[1]
    }
    miscellaneous_box[9:10] = []
    miscellaneous_box[7:8] = []
    miscellaneous_box[2:5] = []

    comic.update({ x[0][0:-1]: x[1:] for x in creators_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x
    comic.update({ x[0][0:-1]: x[1:] for x in miscellaneous_box})
    return comic

#keep 1,2, 6,7,9

def ComicToCsv(Comic):
    return ",".join([str(x) for x in Comic.values()])

with open("Comic.csv", "a") as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(ScrapeComic("http://www.comicbookdb.com/issue.php?ID=" + str(1)).keys())
    for ComicId in range(1, 3):
        try:
            print(ScrapeComic("http://www.comicbookdb.com/issue.php?ID=" + str(ComicId)))
            writer.writerow(ScrapeComic("http://www.comicbookdb.com/issue.php?ID=" + str(ComicId)).values())
            time.sleep(1)
        except:
            pass
