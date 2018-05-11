import urllib.request as urllib2
import bs4
import re
import time
import csv
import ScrapeFunctions


creatorsList = ScrapeFunctions.ReadCSV("CreatorIDs.csv", 0)
print(creatorsList)

desiredColumns = 3
ScrapeFunctions.EditColumn("Characters.csv", desiredColumns)

