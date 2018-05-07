import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapeCharacter(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    name_box = soup.find("span", attrs={"class": "page_headline"})
    info = soup.find_all("td", attrs={"valign": "top", "align": "left"})
    info_box = ScrapeFunctions.HigherOrderListSplit (
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    img = soup.find_all("img")
    ImageURL = ScrapeFunctions.FindURL("graphics/comic_graphics/", img, 0, "comic_graphics/", "\"/")

    character = {
        "CharacterID": int(url[url.find("=") + 1:]),
        "Name": name_box.text.strip(),
        "ImageURL": ImageURL
    }

    character.update({x[0][0:-1]: x[1:] for x in info_box})         #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return character

characterList = ScrapeFunctions.ReadCSV("CharacterIDs.csv")
print(characterList)

charactersFile = open("Characters.csv", "w", newline="")
charactersWriter = csv.writer(charactersFile)
characterColumnList = [
    "CharacterID",
    "Name",
    "Real Name",
    "ImageURL",
    "Powers",
    "Weaknesses",
    "Bio"
]
charactersWriter.writerow(characterColumnList)

#start = 1
#end = 11
#for CharacterID in range(start, end):
for CharacterID in characterList:
    url = "http://www.comicbookdb.com/character.php?ID=" + str(CharacterID)
    error = ScrapeFunctions.IsEmptyPage(url)
    # if page exists (not 404 page not found error)
    if not error:
        character = ScrapeCharacter(url)
        ScrapeFunctions.PrintTable(charactersWriter, characterColumnList, character, " ", ".*' on Amazon.*")
    time.sleep(0.5)

charactersFile.close()