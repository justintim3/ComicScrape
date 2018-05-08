import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapeCreator(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")
    info = soup.find_all("td", attrs={"valign": "top", "width": "850", "align": "left"})
    name_box = soup.find("span", attrs={"class": "page_headline"})
    info_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    img = soup.find_all("img")
    ImageURL = ScrapeFunctions.FindURL("graphics/comic_graphics/", img, 0, "comic_graphics/", "\"/")

    creator = {
        "CreatorID": int(url[url.find("=") + 1:]),
        "Name": name_box.text.strip(),
        "ImageURL": ImageURL
    }

    creator.update({x[0][0:-1]: x[1:] for x in info_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return creator


creatorsList = ScrapeFunctions.ReadCSV("CreatorIDs.csv")

creatorsFile = open("Creators.csv", "w", newline="", encoding="utf-8")
creatorsWriter = csv.writer(creatorsFile)
creatorColumnList = [
        "CreatorID",
        "Name",
        "ImageURL",
        "Bio",
        "Date of Birth",
        "Birthplace"
]
print(creatorColumnList)
creatorsWriter.writerow(creatorColumnList)

count = 0
#start = 858
#end = 859
#for CreatorID in range(start, end):
for CreatorID in creatorsList:
    # write to file after count and reload writer
    if count == 25:
        count = 0
        creatorsFile.flush()
    url = "http://www.comicbookdb.com/creator.php?ID=" + str(CreatorID)
    error = ScrapeFunctions.IsEmptyPage(url)
    # if page exists (not 404 page not found error)
    if not error:
        creator = ScrapeCreator(url)
        ScrapeFunctions.PrintTable(creatorsWriter, creatorColumnList, creator, " ", ".*View a chronological listing*")
    count += 1
    time.sleep(0.5)

creatorsFile.close()