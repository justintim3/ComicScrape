import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapeCharacter(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")
    while True:
        try:
            name_box = soup.find("span", attrs={"class": "page_headline"})
            info = soup.find_all("td", attrs={"valign": "top", "align": "left"})
            info_box = ScrapeFunctions.HigherOrderListSplit(
                ScrapeFunctions.Traverse(info, '|_|'),
                lambda x: re.compile(".*:$").match(x)
            )[1:] #list with delimited list using list comprehension

            id = url[url.find("ID=") + 3:]
            img = soup.find_all("img")
            ImageURL = ScrapeFunctions.FindURL2("graphics/comic_graphics/", img, 0, id + "_", -len(id) - 1, "\"/>")

            character = {
                "CharacterID": int(id),
                "Name": name_box.text.strip(),
                "ImageURL": ImageURL
            }
        except Exception:
            print("Error: " + id)
            continue
        break
    character.update({x[0][0:-1]: x[1:] for x in info_box})         #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x
    #for x in character:
        #print(character[x])

    return character

characterList = ScrapeFunctions.ReadCSV("CharacterIDs.csv", 0)

charactersFile = open("Characters.csv", "w", newline="", encoding="utf-8")
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
print(characterColumnList)
charactersWriter.writerow(characterColumnList)

count = 0
#start = 96
#end = 97
#for CharacterID in range(start, end):
for CharacterID in characterList:
    # write to file after count and reload writer
    if count == 25:
        count = 0
        charactersFile.flush()
    url = "http://www.comicbookdb.com/character.php?ID=" + str(CharacterID)
    error = ScrapeFunctions.IsEmptyPage(url)
    # if page exists (not 404 page not found error)
    if not error:
        character = ScrapeCharacter(url)
        ScrapeFunctions.PrintTable(charactersWriter, characterColumnList, character, " ", ".*' on Amazon.*", '|_|')
    count += 1
    time.sleep(0.5)

charactersFile.close()