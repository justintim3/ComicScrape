import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions

def ScrapeSeries(url):
    page = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(page, "html.parser")

    name_box = soup.find("span", attrs={"class": "page_headline"})
    info = soup.find_all("td", attrs={"valign": "top", "align": "left"})
    info_box = ScrapeFunctions.HigherOrderListSplit (
        ScrapeFunctions.Traverse(info),
        lambda x: re.compile(".*:$").match(x)
    )[1:] #list with delimited list using list comprehension

    link = soup.find_all("a")
    publisher = ScrapeFunctions.FindURL("publisher.php", link, 63, "ID=", "\">")

    series = {
        "SeriesID": int(url[url.find("=") + 1:]),
        "Series Name": name_box.text.strip(),
        "PublisherID": publisher
    }

    series.update({x[0][0:-1]: x[1:] for x in info_box})         #build a dictionary with keys x[0][0:-1], values x[1:] for all elements x

    return series

seriesList = ScrapeFunctions.ReadCSV("SeriesIDs.csv")

seriesFile = open("Series.csv", "w", newline="", encoding="utf-8")
seriesPubFile = open("SeriesPublisher.csv", "w", newline="", encoding="utf-8")
seriesWriter = csv.writer(seriesFile)
seriesPubWriter = csv.writer(seriesPubFile)
seriesColumnList = [
    "SeriesID",
    "Series Name",
    "PublisherID",
    "Publication Date",
    "Country",
    "Language",
    "Notes"
]

seriesPubColumnList = [
    "SeriesID",
    "PublisherID"
]
print(seriesColumnList)
seriesWriter.writerow(seriesColumnList)
seriesPubWriter.writerow(seriesPubColumnList)

#start = 1
#end = 21
#for CharacterID in range(start, end):
for SeriesID in seriesList:
    url = "http://www.comicbookdb.com/title.php?ID=" + str(SeriesID)
    error = ScrapeFunctions.IsEmptyPage(url)
    # if page exists (not 404 page not found error)
    if not error:
        series = ScrapeSeries(url)
        ScrapeFunctions.PrintTable(seriesWriter, seriesColumnList, series, " ", ".*' on Amazon.*")
        ScrapeFunctions.PrintJunctionTable(seriesPubWriter, SeriesID, series["PublisherID"])
    time.sleep(0.5)

seriesFile.close()
seriesPubFile.close()