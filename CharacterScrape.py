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

    character = {}

    try:
        character = {
            "CharacterID": int(url[url.find("=") + 1:]),
            "Name": name_box.text.strip()}
    except Exception as e:
        pass

    character.update({x[0][0:-1]: x[1:] for x in info_box})         #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return character

with open("Characters.csv", "a", newline = "") as csv_file:
    writer = csv.writer(csv_file)

    keyList = [
        "CharacterID",
        "Name",
        "Real Name",
        "Powers",
        "Weaknesses",
        "Bio"
    ]
    print(keyList)
    writer.writerow(keyList)
    start = 1
    end = 21

    for CharacterID in range(start, end):
        try:
            character = ScrapeCharacter("http://www.comicbookdb.com/character.php?ID=" + str(CharacterID))

            valueList = []

            for key in keyList:
                if key in character and type(character[key]) is list:
                    valueList.append(
                        " ".join(
                            list(
                                filter(
                                    lambda x: not (re.compile(".*' on Amazon.*").match(x)),
                                    character[key]
                                )
                            )
                        )
                    )
                elif key in character:
                    valueList.append(character[key])
                else:
                    valueList.append(None)

            for x in range(0, end - start):
                if valueList[x] is not None:
                    print(valueList)
                    writer.writerow(valueList)
                    break

            time.sleep(1)
        except Exception as e:
            #print(str(type(e)) + ": " + str(e))
            pass