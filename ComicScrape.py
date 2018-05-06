import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapeComic(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    info = soup.find_all("td", attrs={"valign": "top", "align": "left"})
    creators = soup.find_all("td", attrs={"valign": "top", "width": "366", "align": "left"})
    miscellaneous = soup.find_all("td", attrs={"colspan": "3", "valign": "top"})

    series_box = soup.find("span", attrs={"class": "page_headline"})
    issue_box = soup.find("span", attrs={"class": "page_subheadline"})
    info_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:]  # list with delimited list using list comprehension
    creators_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(creators),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension
    miscellaneous_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(miscellaneous),
        lambda x: re.compile(".*:$").match(x)
    )[1:]

    html = soup.find_all("a")
    end = ScrapeFunctions.FindIDIndex("review_add.php?", html)
    ImageURL = ScrapeFunctions.FindID("graphics/comic_graphics/", html)
    SeriesID = ScrapeFunctions.FindID("title.php", html)
    PublisherID = ScrapeFunctions.FindID("publisher", html)
    CharacterIDList = ScrapeFunctions.FindAllID("\"character.php", html, end)
    CreatorIDList = ScrapeFunctions.FindAllID("\"creator.php", html, end)
    StoryArcIDList = ScrapeFunctions.FindAllID("\"storyarc.php", html, end)

    #publisher
    #index = 0
    #for x in range(20, len(info_box[12])):
    #    if "<span class='st_facebook_hcount' displayText='Facebook'></span>" in info_box[12][x]:
    #        index = x - 1
    #        break
    #if info_box[12][index] == ")":
    #    index = index - 1
    #publisher = info_box[12][index]

    #remove
    title = issue_box.text.strip().replace("\"", "")
    if title == "Rating":
        title = ""

    creatorTypeIDList = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6"
    ]

    comic = {
        "ComicID": int(url[url.find("=") + 1:]),
        "Series": series_box.text.strip().split(" - ")[0],
        "SeriesID": SeriesID,
        #"Publisher": publisher,
        "PublisherID": PublisherID,
        "Issue Number": series_box.text.strip().split(" - #")[1],
        "Issue Title": title,
        "ImageURL": ImageURL[ImageURL.find("_graphics") + 10:ImageURL.find("target") - 2],
        "StoryArcIDList": StoryArcIDList,
        "CreatorIDList": CreatorIDList,
        "CharacterIDList": CharacterIDList,
        "CreatorTypeIDList": creatorTypeIDList
    }

    comic.update({x[0][0:-1]: x[1:] for x in creators_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x
    comic.update({x[0][0:-1]: x[1:] for x in miscellaneous_box})   #Cover Date, Cover Price

    creatorTypeList = [
        "Writer(s)",
        "Penciller(s)",
        "Inker(s)",
        "Colorist(s)",
        "Letterer(s)",
        "Editor(s)",
        "Cover Artist(s)"
    ]
    creatorTypeIDCountList = []
    for x in range(0, 7):
        try:
            creatorTypeIDCountList.append(len(comic[creatorTypeList[x]]))
        except Exception as e:
            creatorTypeIDCountList.append(0)

    comic.update({"CreatorTypeIDCountList": creatorTypeIDCountList})

    return comic

start = 1
end = 101

keyList = [
    "ComicID",
    "PublisherID",
    "SeriesID",
    "Issue Number",
    "Issue Title",
    "ImageURL",
    "Cover Date",
    "Cover Price",
    "Format",
    "Synopsis",
    "StoryArcIDList",
    "CreatorIDList",
    "CharacterIDList"
]

with open("Comics.csv", "a", newline="") as csv_file:
    writer = csv.writer(csv_file)
    print(keyList)
    writer.writerow(keyList)
    for ComicID in range(start, end):
        url = "http://www.comicbookdb.com/issue.php?ID=" + str(ComicID)
        error = ScrapeFunctions.IsEmptyPage(url)
        #if page exists (not 404 page not found error)
        if not error:
            comic = ScrapeComic(url)
            ScrapeFunctions.PrintTable(writer, keyList, comic, ", ", ".*[Aa]dd/remove.*")
        time.sleep(1)

comicCharIDList = [
    "ComicID",
    "CharacterID"
]
with open("ComicCharacters.csv", "a", newline="") as csv_file:
    writer = csv.writer(csv_file)
    print(comicCharIDList)
    writer.writerow(comicCharIDList)
    for ComicID in range(start, end):
        url = "http://www.comicbookdb.com/issue.php?ID=" + str(ComicID)
        error = ScrapeFunctions.IsEmptyPage(url)
        #if page exists (not 404 page not found error)
        if error is False:
            comic = ScrapeComic(url)
            ScrapeFunctions.PrintJunctionTable(writer, ComicID, comic["CharacterIDList"])
        time.sleep(1)

comicCreatorIDList = [
    "ComicID",
    "CreatorTypeID",
    "CreatorID"
]

with open("ComicCreators.csv", "a", newline="") as csv_file:
    writer = csv.writer(csv_file)
    print(comicCreatorIDList)
    writer.writerow(comicCreatorIDList)
    for ComicID in range(start, end):
        url = "http://www.comicbookdb.com/issue.php?ID=" + str(ComicID)
        error = ScrapeFunctions.IsEmptyPage(url)
        # if page exists (not 404 page not found error)
        if error is False:
            comic = ScrapeComic(url)
            ScrapeFunctions.Print3JunctionTable(
                writer,
                ComicID,
                comic["CreatorTypeIDList"],
                comic["CreatorTypeIDCountList"],
                comic["CreatorIDList"])
        time.sleep(1)


