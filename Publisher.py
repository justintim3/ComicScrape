import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapePublisher(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    info = soup.find_all("td", attrs={"valign": "top", "align": "left"})

    name_box = soup.find("span", attrs={"class": "page_subheadline"})

    info_box = ScrapeFunctions.HigherOrderListSplit(
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    publisher = {
        "PublisherID": int(url[url.find("=") + 1:]),
        "Name": name_box.text.strip(),
    }

    publisher.update({x[0][0:-1]: x[1:] for x in info_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return publisher

with open("Publishers.csv", "a", newline = "") as csv_file:
    writer = csv.writer(csv_file)

    keyList = [
        "PublisherID",
        "Name",
        "Website",
        "Notes",
        "Titles"
    ]
    print(keyList)
    writer.writerow(keyList)

    for PublisherID in range(1, 21):
        try:
            publisher = ScrapePublisher("http://www.comicbookdb.com/publisher.php?ID=" + str(PublisherID))

            valueList = []

            for key in keyList:
                if key in publisher and type(publisher[key]) is list:
                    valueList.append(
                        ScrapeFunctions.ListToString(
                            list(
                                filter(
                                    lambda x: not (re.compile(".*[Aa]dd/remove.*").match(x) or
                                                   re.compile(".*Click here for a history of this publisher's logos.*").match(x)),
                                    publisher[key]
                                )
                            )
                        )
                    )
                elif key in publisher:
                    valueList.append(publisher[key])
                else:
                    valueList.append(None)

            for x in range(0, len(valueList)):
                if valueList[x] is not None:
                    print(valueList)
                    writer.writerow(valueList)
                    break

            time.sleep(1)
        except Exception as e:
            #print(str(type(e)) + ": " + str(e))
            pass