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

    index = 0
    for x in range(20, len(info_box[12])):
        if "<span class='st_facebook_hcount' displayText='Facebook'></span>" in info_box[12][x]:
            index = x - 1
            break
    if info_box[12][index] == ")":
        index = index - 1
    publisher = info_box[12][index]

    title = issue_box.text.strip().replace("\"", "")
    if title == "Rating":
        title = ""

    comic = {
        "ComicID": int(url[url.find("=") + 1:]),
        "Publisher": publisher,
        "Series": series_box.text.strip().split(" - ")[0],
        "Issue Number": series_box.text.strip().split(" - #")[1],
        "Issue Title": title
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
    start = 1
    end = 101

    for ComicID in range(start, end):
        try:
            url = "http://www.comicbookdb.com/issue.php?ID=" + str(ComicID)
            comic = ScrapeComic(url)
            error = ScrapeFunctions.EmptyPage(url)

            if error is False:
                valueList = []

                for key in keyList:
                    if key in comic and type(comic[key]) is list:
                        valueList.append(
                            ", ".join(
                                ScrapeFunctions.ListStringReplace("''", "\\'",
                                    list(
                                        filter(
                                            lambda x: not (re.compile(".*[Aa]dd/remove.*").match(x)),
                                            comic[key]
                                        )
                                    )
                                )
                            )
                        )
                    elif key in comic:
                        valueList.append(comic[key])
                    else:
                        valueList.append(None)

                print(valueList)
                writer.writerow(valueList)

            time.sleep(1)
        except Exception as e:
            #print(str(type(e)) + ": " + str(e))
            pass