import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapeComic(url, ComicID):
    page = urllib2.urlopen(url + ComicID)
    soup = bs4.BeautifulSoup(page, "html.parser")

    creators = soup.find_all("td", attrs={"valign": "top", "width": "366", "align": "left"})
    miscellaneous = soup.find_all("td", attrs={"colspan": "3", "valign": "top"})

    publisher_box = soup.find("a", attrs={"class": "test"})
    series_box = soup.find("span", attrs={"class": "page_headline"})
    issue_box = soup.find("span", attrs={"class": "page_subheadline"})
    creators_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(creators),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension
    miscellaneous_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(miscellaneous),
        lambda x: re.compile(".*:$").match(x)
    )[1:]

    comic = {
        "ComicID": ComicID,
        "Publisher": publisher_box.text.strip(),
        "Series": series_box.text.strip().split(" - ")[0],
        "Issue Number": series_box.text.strip().split(" - ")[1],
        "Issue Title": issue_box.text.strip().replace("\"", "")
    }

    comic.update({x[0][0:-1]: x[1:] for x in creators_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x
    comic.update({x[0][0:-1]: x[1:] for x in miscellaneous_box})   #Cover Date, Cover Price

    return comic

with open("Comics.csv", "a", newline = "") as csv_file:
    writer = csv.writer(csv_file)

    keyList = [
        "ComicID",
        "Publisher",
        "Series",
        "Issue Number",
        "Issue Title",
        "Writer(s)",
        "Penciller(s)",
        "Inker(s)",
        "Colorist(s)",
        "Letterer(s)",
        "Editor(s)",
        "Cover Artist(s)",
        "Cover Date",
        "Cover Price",
        "Format",
        "Synopsis",
        "Story Arc(s)",
        "Characters"
    ]
    print(keyList)
    writer.writerow(keyList)

    for ComicID in range(1, 21):
        try:
            comic = ScrapeComic("http://www.comicbookdb.com/issue.php?ID=", str(ComicID))

            valueList = []

            for key in keyList:
                if type(comic[key]) is list:
                    valueList.append(
                        ScrapeFunctions.ListToString(
                            list(
                                filter(
                                    lambda x: not (re.compile(".*[Aa]dd/remove.*").match(x)),
                                    comic[key]
                                )
                            )
                        )
                    )
                else:
                    valueList.append(comic[key])

            print(valueList)
            writer.writerow(valueList)

            time.sleep(1)
        except Exception as e:
            #print(str(type(e)) + ": " + str(e))
            pass