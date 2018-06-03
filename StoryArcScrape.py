import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions


def ScrapeStoryArc(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    info = soup.find_all("td", attrs={"valign": "top", "width": "884", "align": "left"})
    info_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(info, ""),
        lambda x: re.compile(".*:$").match(x)
    )[1:]  # list with delimited list using list comprehension
    TitleTag = soup.find_all("span", attrs={"class": "page_headline"})
    StoryArcTitle = str(TitleTag)
    id = url[url.find("ID=") + 3:]

    arc = {
        "StoryArcID": int(id),
        "StoryArcTitle": StoryArcTitle[StoryArcTitle.find("page_headline") + 15: StoryArcTitle.find("</span>")]
    }
    arc.update({x[0][0:-1]: x[1:] for x in info_box})  # build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return arc


storyArcList = ScrapeFunctions.ReadCSV("StoryArcIDs.csv", 0)

storyArcsFile = open("StoryArcs.csv", "w", newline="")
storyArcsWriter = csv.writer(storyArcsFile)
storyArcColumnList = [
    "StoryArcID",
    "StoryArcTitle",
    "Notes"
]
print(storyArcColumnList)
storyArcsWriter.writerow(storyArcColumnList)

for StoryArcID in storyArcList:
    url = "http://www.comicbookdb.com/storyarc.php?ID=" + str(StoryArcID)
    error = ScrapeFunctions.IsEmptyPage(url)
    # if page exists (not 404 page not found error)
    if not error:
        storyArc = ScrapeStoryArc(url)
        ScrapeFunctions.PrintTable(storyArcsWriter, storyArcColumnList, storyArc, " ", ".*' on Amazon.*", " ")
    time.sleep(0.5)

storyArcsFile.close()