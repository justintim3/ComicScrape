import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions
import functools

def ScrapeCreator(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    info = soup.find_all("td", attrs={"valign": "top", "width": "850", "align": "left"})
    name_box = soup.find("span", attrs={"class": "page_headline"})

    info_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    creator = {
        "CreatorID": int(url[url.find("=") + 1:]),
        "Name": name_box.text.strip()}

    creator.update({x[0][0:-1]: x[1:] for x in info_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return creator

with open("Creators.csv", "a", newline = "") as csv_file:
    writer = csv.writer(csv_file)

    keyList = [
        "CreatorID",
        "Name",
        "Bio",
        "Date of Birth",
        "Birthplace"]
        #"Writer",
        #"Penciller",
        #"Inker",
        #"Colorist(",
        #"Letterer",
        #"Editor",
        #"Cover Artist"

    print(keyList)
    writer.writerow(keyList)
    start = 1
    end = 21

    for CreatorID in range(start, end):
        try:
            creator = ScrapeCreator("http://www.comicbookdb.com/creator.php?ID=" + str(CreatorID))

            valueList = []

            for key in keyList:
                if key in creator and type(creator[key]) is list:
                    valueList.append(
                        " ".join(
                            list(
                                filter(
                                    lambda x: not (re.compile(".*' on Amazon.*").match(x)),
                                    creator[key]
                                )
                            )
                        )
                    )
                elif key in creator:
                    valueList.append(creator[key])
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