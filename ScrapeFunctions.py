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

#Search until ID is found
def FindID(string, aList):
    for x in range(63, len(aList)):
        if string in str(aList[x]):
            begin = str(aList[x]).find("ID=") + 3
            end = str(aList[x]).find("\">")
            return str(aList[x])[begin:end]

#Search until ID is found and return index
def FindIDIndex(string, aList):
    for x in range(63, len(aList)):
        if string in str(aList[x]):
            return x

#Search until all IDs are found
def FindAllID(string, aList, end):
    idList = []
    for x in range(63, end):
        if string in str(aList[x]):
            begin = str(aList[x]).find("ID=") + 3
            end = str(aList[x]).find("\">")
            idList.append(str(aList[x])[begin:end])
    return idList

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

def IsEmptyPage(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    error = soup.find("h2")
    error2 = str(soup.find("span", attrs={"class": "page_headline"})).find("You Must Be Logged In") != -1
    #print(error is not None)
    #print(error2)

    return error is not None or error2

def PrintTable(writer, keyList, dictionary, joinStr, lamda):
        try:
            valueList = []
            for key in keyList:
                if key in dictionary and type(dictionary[key]) is list:
                    valueList.append(
                        joinStr.join(
                            ListStringReplace("''", "\\'",
                                list(
                                    filter(
                                        lambda x: not (re.compile(lamda).match(x)),
                                        dictionary[key]
                                    )
                                )
                            )
                        )
                    )
                elif key in dictionary:
                    valueList.append(dictionary[key])
                else:
                    valueList.append(None)
            print(valueList)
            writer.writerow(valueList)
        except Exception as e:
            print(str(type(e)) + ": " + str(e))
            pass

def PrintJunctionTable(writer, ID, IDList):
    try:
        list = []
        for x in range(0, len(IDList)):
            list.append(ID)
            list.append(IDList[x])
            print(list)
            writer.writerow(list)
            list.clear()
    except Exception as e:
        print(str(type(e)) + ": " + str(e))
        pass

def Print3JunctionTable(writer, ID, TypeIDList, TypeIDCountList, IDList):
    try:
        list = []
        count = 0
        type = 0
        for x in range(0, len(IDList)):
            list.append(ID)

            if count == int(TypeIDCountList[type]):
                count = 0
                type +=1

            list.append(TypeIDList[type])
            list.append(IDList[x])
            count += 1
            print(list)
            writer.writerow(list)
            list.clear()
    except Exception as e:
        print(str(type(e)) + ": " + str(e))
        pass