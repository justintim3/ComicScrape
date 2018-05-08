import urllib.request as urllib2
import bs4
import time
import csv
import ScrapeFunctions


def ScrapeStoryArc(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    issue_box = soup.find("td", attrs={"align": "left", "valign": "top", "width": "884"})

    html = soup.find_all("a")
    end = ScrapeFunctions.FindURLIndex("storyarc_history.php?", html)
    IssueIDList = ScrapeFunctions.FindAllURLs("\"issue.php", html, 63, end, "ID=", "\">")
    CharacterIDList = ScrapeFunctions.FindAllURLs("\"character.php", html, 63, end, "ID=", "\">")
    TitleTag = soup.findAll("span", attrs={"class": "page_headline"})
    StringTitle = str(TitleTag)

    arc = {
        "ArcTitle": StringTitle[StringTitle.find("page_headline") + 15: StringTitle.find("</span>")],
        "Issues": IssueIDList,
        "Character": CharacterIDList
    }

    return arc


storyArcList = ScrapeFunctions.ReadCSV("StoryArcIDs.csv")

storyArcsFile = open("StoryArcs.csv", "w", newline="")
storyArcsWriter = csv.writer(storyArcsFile)
storyArcColumncList = [
    "ArcTitle",
    "Issues",
    "Character",
]
print(storyArcColumncList)
storyArcsWriter.writerow(storyArcColumncList)

for StoryArcID in storyArcList:
    url = "http://www.comicbookdb.com/storyarc.php?ID=" + str(StoryArcID)
    error = ScrapeFunctions.IsEmptyPage(url)
    # if page exists (not 404 page not found error)
    if not error:
        storyArc = ScrapeStoryArc(url)
        ScrapeFunctions.PrintTable(storyArcsWriter, storyArcColumncList, storyArc, " ", ".*' on Amazon.*")
    time.sleep(0.5)

storyArcsFile.close()