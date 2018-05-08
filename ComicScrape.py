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

    link = soup.find_all("a")
    img = soup.find_all("img")
    end = ScrapeFunctions.FindURLIndex("review_add.php?", link)
    ImageURL = ScrapeFunctions.FindURL("graphics/comic_graphics/", img, 0, "comic_graphics/", "\" width=")
    SeriesID = ScrapeFunctions.FindURL("title.php", link, 63, "ID=", "\">")
    PublisherID = ScrapeFunctions.FindURL("publisher", link, 63, "ID=", "\">")
    CharacterIDList = ScrapeFunctions.FindAllURLs("\"character.php", link, 63, end, "ID=", "\">")
    CreatorIDList = ScrapeFunctions.FindAllURLs("\"creator.php", link, 63, end, "ID=", "\">")
    StoryArcIDList = ScrapeFunctions.FindAllURLs("\"storyarc.php", link, 63, end, "ID=", "\">")

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
        "0", "1", "2", "3", "4", "5", "6"
    ]

    comic = {
        "ComicID": int(url[url.find("=") + 1:]),
        "Series": series_box.text.strip().split(" - ")[0],
        "SeriesID": SeriesID,
        #"Publisher": publisher,
        "PublisherID": PublisherID,
        "Issue Number": series_box.text.strip().split(" - #")[1],
        "Issue Title": title,
        "ImageURL": ImageURL,
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

publisherID = set()
seriesID = set()
storyArcID = set()
creatorID = set()
characterID = set()

comicsFile = open("Comics.csv", "w", newline="", encoding="utf-8")
comicCreatorsFile = open("ComicCreators.csv", "w", newline="", encoding="utf-8")
comicCharactersFile = open("ComicCharacters.csv", "w", newline="", encoding="utf-8")
publisherIDs = open("PublisherIDs.csv", "w", newline="", encoding="utf-8")
seriesIDs = open("SeriesIDs.csv", "w", newline="", encoding="utf-8")
storyArcIDs = open("StoryArcIDs.csv", "w", newline="", encoding="utf-8")
creatorIDs = open("CreatorIDs.csv", "w", newline="", encoding="utf-8")
characterIDs = open("CharacterIDs.csv", "w", newline="", encoding="utf-8")

comicsWriter = csv.writer(comicsFile)
comicCreatorsWriter = csv.writer(comicCreatorsFile)
comicCharactersWriter = csv.writer(comicCharactersFile)
publisherIDsWriter = csv.writer(publisherIDs)
seriesIDsWriter = csv.writer(seriesIDs)
storyArcIDsWriter = csv.writer(storyArcIDs)
creatorIDsWriter = csv.writer(creatorIDs)
characterIDsWriter = csv.writer(characterIDs)

comicColumnList = [
    "ComicID",
    "PublisherID",
    "SeriesID",
    "Issue Number",
    "Issue Title",
    "ImageURL",
    "Cover Date",
    "Cover Price",
    "Format",
    "Synopsis"
]
comicCharIDColumnList = [
    "ComicID",
    "CharacterID"
]
comicCreatorIDColumnList = [
    "ComicID",
    "CreatorTypeID",
    "CreatorID"
]

print(comicColumnList)
comicsWriter.writerow(comicColumnList)
comicCreatorsWriter.writerow(comicCreatorIDColumnList)
comicCharactersWriter.writerow(comicCharIDColumnList)
publisherIDsWriter.writerow(["PublisherID"])
seriesIDsWriter.writerow(["SeriesID"])
storyArcIDsWriter.writerow(["StoryArcID"])
creatorIDsWriter.writerow(["CreatorID"])
characterIDsWriter.writerow(["CharacterID"])

for ComicID in range(start, end):
    url = "http://www.comicbookdb.com/issue.php?ID=" + str(ComicID)
    error = ScrapeFunctions.IsEmptyPage(url)
    #if page exists (not 404 page not found error)
    if not error:
        comic = ScrapeComic(url)
        ScrapeFunctions.PrintTable(comicsWriter, comicColumnList, comic, ", ", ".*[Aa]dd/remove.*")
        ScrapeFunctions.PrintJunctionTable(comicCharactersWriter, ComicID, comic["CharacterIDList"])
        ScrapeFunctions.Print3JunctionTable(
            comicCreatorsWriter,
            ComicID,
            comic["CreatorTypeIDList"],
            comic["CreatorTypeIDCountList"],
            comic["CreatorIDList"])
        for publisher in comic["PublisherID"]:
            publisherID.add(publisher)
        for series in comic["SeriesID"]:
            seriesID.add(series)
        for arc in comic["StoryArcIDList"]:
            storyArcID.add(arc)
        for creator in comic["CreatorIDList"]:
            creatorID.add(creator)
        for character in comic["CharacterIDList"]:
            characterID.add(character)
    time.sleep(0.5)

print(seriesID)
print(storyArcID)
print(characterID)

ScrapeFunctions.PrintColumn(publisherIDsWriter, list(publisherID))
ScrapeFunctions.PrintColumn(seriesIDsWriter, list(seriesID))
ScrapeFunctions.PrintColumn(storyArcIDsWriter, list(storyArcID))
ScrapeFunctions.PrintColumn(creatorIDsWriter, list(creatorID))
ScrapeFunctions.PrintColumn(characterIDsWriter, list(characterID))

comicsFile.close()
comicCreatorsFile.close()
comicCharactersFile.close()
publisherIDs.close()
seriesIDs.close()
storyArcIDs.close()
creatorIDs.close()
characterIDs.close()
