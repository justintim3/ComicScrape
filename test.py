
import re
search = "\r\n"
url = "abcdef" + search + "ghi" + search + "jk"

#print(url)

ylist = [x.start() for x in re.finditer(search, url)]
ylist.reverse()
#print(ylist)

def RemoveSubstr(sub, str):
    length = 0
    if sub is "\r\n":
        length = 2
    else:
        length = len(sub)

    occurances = [x.start() for x in re.finditer(sub, str)]
    occurances.reverse()

    for i in range(0, len(occurances)):
        str = str[0:occurances[i]] + str[(occurances[i] + length):]

    return str


url = RemoveSubstr("cd", url)

print(url)


#url = "dfgfdg\r\n\r\ndfgdfgdfgdfg"
#x = "\r"
#print(url.find(x))

#url = len(x)
#print(url[url.find("=") + 1:])