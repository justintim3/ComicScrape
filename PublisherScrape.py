import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapePublisher(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    info = soup.find_all("td", attrs={"valign": "top", "align": "left"})

    name_box = soup.find("span", attrs={"class": "page_subheadline"})

    info_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    publisher = {
        "PublisherID": int(url[url.find("=") + 1:]),
        "Name": name_box.text.strip(),
    }

    publisher.update({x[0][0:-1]: x[1:] for x in info_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return publisher


publisherList = ScrapeFunctions.ReadCSV("PublisherIDs.csv", 0)

publishersFile = open("Publishers.csv", "w", newline="", encoding="utf-8")
publishersWriter = csv.writer(publishersFile)
publisherColumnList = [
    "PublisherID",
    "Name",
    "Website",
    "Notes",
    "Titles"
]

print(publisherColumnList)
publishersWriter.writerow(publisherColumnList)

#start = 1
#end = 21
#for CharacterID in range(start, end):
for PublisherID in publisherList:
    url = "http://www.comicbookdb.com/publisher.php?ID=" + str(PublisherID)
    error = ScrapeFunctions.IsEmptyPage(url)
    # if page exists (not 404 page not found error)
    if not error:
        publisher = ScrapePublisher(url)
        ScrapeFunctions.PrintTable(publishersWriter, publisherColumnList, publisher,
            " ", ".*Click here for a history of this publisher's logos.*")
    time.sleep(0.5)

# lambda x: not (re.compile(".*[Aa]dd/remove.*").match(x) or
#   re.compile(".*Click here for a history of this publisher's logos.*").match(x)),
#   publisher[key]