import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapeCreator(url, CreatorID):
    page = urllib2.urlopen(url + CreatorID)
    soup = bs4.BeautifulSoup(page, "html.parser")

    info = soup.find_all("td", attrs={"valign": "top", "width": "850", "align": "left"})
    name_box = soup.find("span", attrs={"class": "page_headline"})

    info_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    creator = {"CreatorID": CreatorID,
        "Name": name_box.text.strip()}

    creator.update({x[0][0:-1]: x[1:] for x in info_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return creator

with open("Creator.csv", "a", newline = "") as csv_file:
    writer = csv.writer(csv_file)

    keyList = [
        "CreatorID",
        "Name",
        "Bio",
        "Date of Birth",
        "Birthplace"
        #"Writer",
        #"Penciller",
        #"Inker",
        #"Colorist(",
        #"Letterer",
        #"Editor",
        #"Cover Artist"
    ]
    print(keyList)
    writer.writerow(keyList)

    for CreatorID in range(1, 21):
        try:
            creator = ScrapeCreator("http://www.comicbookdb.com/creator.php?ID=", str(CreatorID))

            print(creator)
            valueList = []

            for key in keyList:
                if type(creator[key]) is list:
                    valueList.append(
                        ScrapeFunctions.ListToString(
                            list(
                                filter(
                                    lambda x: not (re.compile(".*' on Amazon.*").match(x)),
                                    creator[key]
                                )
                            )
                        )
                    )
                else:
                    valueList.append(creator[key])

            print(valueList)
            writer.writerow(valueList)

            time.sleep(1)
        except Exception as e:
            print(str(type(e)) + ": " + str(e))
            pass