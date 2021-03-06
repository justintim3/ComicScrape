import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapeComic(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")
    newlineReplace = "|_|"
    while True:
        try:
            info = soup.find_all("td", attrs={"valign": "top", "align": "left"})
            creators = soup.find_all("td", attrs={"valign": "top", "width": "366", "align": "left"})
            miscellaneous = soup.find_all("td", attrs={"colspan": "3", "valign": "top"})
            series_box = soup.find("span", attrs={"class": "page_headline"})
            issue_box = soup.find("span", attrs={"class": "page_subheadline"})

            info_box = ScrapeFunctions.HigherOrderListSplit(
                ScrapeFunctions.Traverse(info, newlineReplace),
                lambda x: re.compile(".*:$").match(x)
            )[1:]  # list with delimited list using list comprehension
            creators_box = ScrapeFunctions.HigherOrderListSplit(
                ScrapeFunctions.Traverse(creators, newlineReplace),
                lambda x: re.compile(".*:$").match(x)
            )[1:] #list with delimited list using list comprehension
            miscellaneous_box = ScrapeFunctions.HigherOrderListSplit(
                ScrapeFunctions.Traverse(miscellaneous, newlineReplace),
                lambda x: re.compile(".*:$").match(x)
            )[1:]

            id = url[url.find("ID=") + 3:]
            link = soup.find_all("a")
            #img = soup.find_all("img")
            end = ScrapeFunctions.FindURLIndex("review_add.php?", link)
            ImageURL = ScrapeFunctions.FindURL2("graphics/comic_graphics/", link, 0, id + "_", -len(id) - 1, "\" target=")
            #ImageURL = ScrapeFunctions.FindURL2("graphics/comic_graphics/", link, 0, "comic_graphics/", 0, "\" target=")
            SeriesID = ScrapeFunctions.FindURL("title.php", link, 63, "ID=", "\">")
            PublisherID = ScrapeFunctions.FindURL("publisher", link, 63, "ID=", "\">")
            CharacterIDList = ScrapeFunctions.FindAllURLs("\"character.php", link, 63, end, "ID=", "\">")
            CreatorIDList = ScrapeFunctions.FindAllURLs("\"creator.php", link, 63, end, "ID=", "\">")
            StoryArcIDList = ScrapeFunctions.FindAllURLs("\"storyarc.php", link, 63, end, "ID=", "\">")

            index = 0
            for x in range(20, len(info_box[12])):
               if "<span class='st_facebook_hcount' displayText='Facebook'></span>" in info_box[12][x]:
                   index = x - 2
                   break
            if info_box[12][index] == ")":
               index = index - 1
            publisher = info_box[12][index]

            #remove
            title = issue_box.text.strip().replace("\"", "")
            if title == "Rating":
                title = ""

            creatorTypeIDList = [
                "1", "2", "3", "4", "5", "6", "7"
            ]

            comic = {
                "ComicID": int(id),
                "Series": series_box.text.strip().split(" - ")[0],
                "SeriesID": SeriesID,
                "Publisher": publisher,
                "PublisherID": PublisherID,
                "Issue Number": series_box.text.strip().split(" - #")[1],
                "Issue Title": title,
                "ImageURL": ImageURL,
                "StoryArcIDList": StoryArcIDList,
                "CreatorIDList": CreatorIDList,
                "CharacterIDList": CharacterIDList,
                "CreatorTypeIDList": creatorTypeIDList
            }
        except Exception:
            print("Error: " + id)
            continue
        break
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
            if comic[creatorTypeList[x]]:
                sum = 0
                for element in comic[creatorTypeList[x]]:
                    if element != newlineReplace:
                        sum = sum + 1
                creatorTypeIDCountList.append(sum)
            else:
                creatorTypeIDCountList.append(0)
        except Exception as e:
            creatorTypeIDCountList.append(0)
    comic.update({"CreatorTypeIDCountList": creatorTypeIDCountList})
    return comic


publisherID = set()
seriesID = set()
storyArcID = set()
creatorID = set()
characterID = set()

comicsFile = open("Comics.csv", "w", newline="", encoding="utf-8")
publisherIDs = open("PublisherIDs.csv", "w", newline="", encoding="utf-8")
seriesIDs = open("SeriesIDs.csv", "w", newline="", encoding="utf-8")
storyArcIDs = open("StoryArcIDs.csv", "w", newline="", encoding="utf-8")
creatorIDs = open("CreatorIDs.csv", "w", newline="", encoding="utf-8")
characterIDs = open("CharacterIDs.csv", "w", newline="", encoding="utf-8")
#JunctionTables
comicSeriesFile = open("ComicSeries.csv", "w", newline="", encoding="utf-8")
comicCreatorsFile = open("ComicCreators.csv", "w", newline="", encoding="utf-8")
comicCharactersFile = open("ComicCharacters.csv", "w", newline="", encoding="utf-8")
comicPublishersFile = open("ComicPublishers.csv", "w", newline="", encoding="utf-8")
comicStoryArcsFile = open("ComicStoryArcs.csv", "w", newline="", encoding="utf-8")

comicsWriter = csv.writer(comicsFile)
publisherIDsWriter = csv.writer(publisherIDs)
seriesIDsWriter = csv.writer(seriesIDs)
storyArcIDsWriter = csv.writer(storyArcIDs)
creatorIDsWriter = csv.writer(creatorIDs)
characterIDsWriter = csv.writer(characterIDs)
#JunctionTables
comicSeriesWriter = csv.writer(comicSeriesFile)
comicCreatorsWriter = csv.writer(comicCreatorsFile)
comicCharactersWriter = csv.writer(comicCharactersFile)
comicPublishersWriter = csv.writer(comicPublishersFile)
comicStoryArcsWriter = csv.writer(comicStoryArcsFile)

comicColumnList = [
    "ComicID",
    "SeriesID",
    "Series",
    "Issue Number",
    "Issue Title",
    "PublisherID",
    "Publisher",
    "ImageURL",
    "Cover Date",
    "Cover Price",
    "Format",
    "Synopsis"
]
comicSeriesIDColumnList = [
    "ComicID",
    "SeriesID"
]
comicCreatorIDColumnList = [
    "ComicID",
    "CreatorTypeID",
    "CreatorID"
]
comicCharIDColumnList = [
    "ComicID",
    "CharacterID"
]
comicPubIDColumnList = [
    "ComicID",
    "PublisherID"
]
comicStoryArcIDColumnList = [
    "ComicID",
    "StoryArcID"
]

print(comicColumnList)
comicsWriter.writerow(comicColumnList)
publisherIDsWriter.writerow(["PublisherID"])
seriesIDsWriter.writerow(["SeriesID"])
storyArcIDsWriter.writerow(["StoryArcID"])
creatorIDsWriter.writerow(["CreatorID"])
characterIDsWriter.writerow(["CharacterID"])

comicSeriesWriter.writerow(comicSeriesIDColumnList)
comicCreatorsWriter.writerow(comicCreatorIDColumnList)
comicCharactersWriter.writerow(comicCharIDColumnList)
comicPublishersWriter.writerow(comicPubIDColumnList)
comicStoryArcsWriter.writerow(comicStoryArcIDColumnList)

start = 1
end = 201
#for ComicID in range(start, end):
ComicID = start
while(ComicID < end):
    url = "http://www.comicbookdb.com/issue.php?ID=" + str(ComicID)
    error = ScrapeFunctions.IsEmptyPage(url)
    #if page exists (not 404 page not found error)
    if not error:
        comic = ScrapeComic(url)
        ScrapeFunctions.PrintTable(comicsWriter, comicColumnList, comic, " ", ".*[Aa]dd/remove.*", "|_|")
        ScrapeFunctions.PrintJunctionTable(comicSeriesWriter, ComicID, [int(comic["SeriesID"])])
        ScrapeFunctions.PrintJunctionTable(comicCharactersWriter, ComicID, comic["CharacterIDList"])
        ScrapeFunctions.PrintJunctionTable(comicPublishersWriter, ComicID, [int(comic["PublisherID"])])
        ScrapeFunctions.PrintJunctionTable(comicStoryArcsWriter, ComicID, comic["StoryArcIDList"])
        ScrapeFunctions.Print3JunctionTable(
            comicCreatorsWriter,
            ComicID,
            comic["CreatorTypeIDList"],
            comic["CreatorTypeIDCountList"],
            comic["CreatorIDList"])
        #Add ID's to set to ensure unique IDs
        publisherID.add(int(comic["PublisherID"]))
        seriesID.add(int(comic["SeriesID"]))
        for arc in comic["StoryArcIDList"]:
            storyArcID.add(arc)
        for creator in comic["CreatorIDList"]:
            creatorID.add(creator)
        for character in comic["CharacterIDList"]:
            characterID.add(character)
    else:
        end = end + 1
    ComicID = ComicID + 1
    time.sleep(0.5)

#print(publisherID)
#print(seriesID)
#print(storyArcID)
#print(characterID)

ScrapeFunctions.PrintColumn(publisherIDsWriter, list(publisherID))
ScrapeFunctions.PrintColumn(seriesIDsWriter, list(seriesID))
ScrapeFunctions.PrintColumn(storyArcIDsWriter, list(storyArcID))
ScrapeFunctions.PrintColumn(creatorIDsWriter, list(creatorID))
ScrapeFunctions.PrintColumn(characterIDsWriter, list(characterID))

comicsFile.close()
publisherIDs.close()
seriesIDs.close()
storyArcIDs.close()
creatorIDs.close()
characterIDs.close()
comicSeriesFile.close()
comicCreatorsFile.close()
comicCharactersFile.close()
comicPublishersFile.close()
