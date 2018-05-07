import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions
import functools

def ScrapeCreator(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    info = soup.find_all("td", attrs={"valign": "top", "width": "850", "align": "left"})
    name_box = soup.find("span", attrs={"class": "page_headline"})

    info_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    creator = {
        "CreatorID": int(url[url.find("=") + 1:]),
        "Name": name_box.text.strip()}

    creator.update({x[0][0:-1]: x[1:] for x in info_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return creator



creatorsList = ScrapeFunctions.ReadCSV("CreatorIDs.csv")
print(creatorsList)

creatorsFile = open("Creators.csv", "w", newline="")
creatorsWriter = csv.writer(creatorsFile)
creatorColumnList = [
        "CreatorID",
        "Name",
        "Bio",
        "Date of Birth",
        "Birthplace"
]
creatorsWriter.writerow(creatorColumnList)

for CreatorID in creatorsList:
    url = "http://www.comicbookdb.com/creator.php?ID=" + str(CreatorID)
    error = ScrapeFunctions.IsEmptyPage(url)
    # if page exists (not 404 page not found error)
    if not error:
        creator = ScrapeCreator(url)
        ScrapeFunctions.PrintTable(creatorsWriter, creatorColumnList, creator, " ", ".*' on Amazon.*")
    time.sleep(0.5)

creatorsFile.close()
