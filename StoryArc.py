import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions


def ScrapeStoryArc(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    issue_box = soup.find("td", attrs={"align": "left", "valign": "top", "width": "884"})

    html = soup.find_all("a")
    end = ScrapeFunctions.FindIDIndex("storyarc_history.php?", html)
    IssueIDList = ScrapeFunctions.FindAllID("\"issue.php", html, end)
    CharacterIDList = ScrapeFunctions.FindAllID("\"character.php", html, end)
    TitleTag = soup.findAll("span", attrs={"class": "page_headline"})
    StringTitle = str(TitleTag)

    #"ImageURL": ImageURL[ImageURL.find("_graphics") + 10:ImageURL.find("target") - 2],

    arc = {
        "ArcTitle": StringTitle[StringTitle.find("page_headline") + 15: StringTitle.find("</span>")],
        "Issues": IssueIDList,
        "Character": CharacterIDList
    }
    
    return arc


start = 3
end = 10

storyArcList = [
        "ArcTitle",
        "Issues",
        "Character",
]


with open("StoryArc.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    print(storyArcList)
    writer.writerow(storyArcList)
    for ArcID in range(start, end):
        url = "http://www.comicbookdb.com/storyarc.php?ID=" + str(ArcID)
        error = ScrapeFunctions.IsEmptyPage(url)
        # if page exists (not 404 page not found error)
        if error is False:
            arc = ScrapeStoryArc(url)
            ScrapeFunctions.PrintTable(writer, storyArcList, arc, ", ", ".*[Aa]dd/remove.*")
        time.sleep(1)

