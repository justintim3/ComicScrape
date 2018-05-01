#import libraries
import urllib.request as urllib2
import bs4
import re
import time
import csv

# traverses an HTML tag tree via depth first traversal
def Traverse(Tags):
    result = []
    for tag in Tags:
        if tag.string and tag.string.strip():
            result.append(tag.string.strip())
        elif hasattr(tag, "contents") and tag.contents:
            result.extend(Traverse(tag.contents))
        else:
            pass
    return result

# splits a list into a list of sublists based on a lambda that returns a boolean
def HigherOrderListSplit(sequence, l):
    result = []
    g = []
    for element in sequence:
        if l(element):
            result.append(g)
            g = []
        g.append(element)
    result.append(g)
    return result

def ScrapeCreator(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    info = soup.find_all("td", attrs={"valign": "top", "width": "850", "align": "left"})
    name_box = soup.find("span", attrs={"class": "page_headline"})

    info_box = HigherOrderListSplit(
        Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    creator = {"Name": name_box.text.strip()}

    creator.update({x[0][0:-1]: x[1:] for x in info_box}) #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x
    #print(creator)
    return creator

def ListToString(list):
    str = ""
    for x in range(0, len(list)):
        str += list[x]
        if x < len(list) - 1:
            str += ", "
    return str

with open("Creator.csv", "a", newline = "") as csv_file:
    writer = csv.writer(csv_file)

    keyList = [
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

    for CreatorID in range(1, 3):
        try:
            creator = ScrapeCreator("http://www.comicbookdb.com/creator.php?ID=" + str(CreatorID))

            print(creator)
            valueList = []

            for key in keyList:
                if type(creator[key]) is list:
                    valueList.append(
                        ListToString(
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
