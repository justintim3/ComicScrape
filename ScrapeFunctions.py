import urllib.request as urllib2
import bs4
import csv
import re
import time

# traverses an HTML tag tree via depth first traversal and returns a list of text
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

def TraverseLinks(Tags):
    result = []
    for tag in Tags:
        if not (tag.string and tag.string.strip()):
            result.append(tag)
        elif hasattr(tag, "contents") and tag.contents:
            print("test")
            result.extend(TraverseLinks(tag.contents))
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

def ListToString(list):
    str = ""
    for x in range(0, len(list)):
        str += list[x]
        if x < len(list) - 1:
            str += " "
    return str

def NewLineReplace(list):
    for x in range(0, len(list)):
        str(list[x]).replace("\r", "").replace("\n", "")
    return list

def ListStringReplace(sub, repl, list):
    for x in range(0, len(list)):
        list[x] = str(list[x]).replace(sub, repl)
    return list

def EmptyPage(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    error = soup.find("h2")
    #print(error)
    return error is not None

def RunScrape(Excel, keyList, rangeTuple, Function, url):
    with open(Excel, "a", newline="") as csv_file:
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
                character = Function(url + str(CharacterID))

                valueList = []

                for key in keyList:
                    if key in character and type(character[key]) is list:
                        valueList.append(
                            ListToString(
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

                for x in range(0, len(valueList)):
                    if valueList[x] is not None:
                        print(valueList)
                        writer.writerow(valueList)
                        break

                time.sleep(1)
            except Exception as e:
                print(str(type(e)) + ": " + str(e))
                pass