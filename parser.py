'''
 * Date: 14-12-14
 * Desc: Parser for csv card-lists
 * Author: H. Skjevling
'''

import csv
import threading
import sys
import traceback

class CardListCsvParser:

    def __init__(self):
        self.cryptDict = dict()
        self.libraryDict = dict()
        self.setsDict = dict()
        self.initialized = False

    def parseCrypt(self):
        with open("Resources/vtescrypt.csv", newline="", encoding="utf-8-sig") as csvFile:
            try:
                d = dict()
                reader = csv.DictReader(csvFile, delimiter=",", quotechar="\"", lineterminator="\n")
                for row in reader:
                    if row["Adv"] == "Advanced":
                        row["Name"] += "(ADV)"
                    d[row["Name"]] = row
                    #print("")
                    #print(row.keys())
            except:
                print("\nParsing crypt failed at row " + str(len(self.cryptDict)+1) + ": \n" + str(row))
                raise
            finally:
                return d

    def parseLibrary(self):
        with open("Resources/vteslib.csv", newline="", encoding="utf-8-sig") as csvFile:
            try:
                d = dict()
                reader = csv.DictReader(csvFile, delimiter=",", quotechar="\"", lineterminator="\n")
                for row in reader:
                    d[row["Name"]] = row
                    #print("")
                    #print(row.keys())
            except:
                print("\nParsing library failed at row " + str(len(self.libraryDict)+1) + ": \n" + str(row))
                raise
            finally:
                return d

    def parseSets(self):
        with open("Resources/vtessets.csv", newline="", encoding="utf-8-sig") as csvFile:
            try:
                d = dict()
                reader = csv.DictReader(csvFile, delimiter=",", quotechar="\"", lineterminator="\n")
                for row in reader:
                    d[row["Abbrev"]] = row
            except:
                print("\nParsing sets failed at row " + str(len(self.setsDict)+1) + ": \n" + str(row))
                raise
            finally:
                return d

    def parseBoosterDistribution(self):
        with open("Resources/vtesboosters.csv", newline="", encoding="utf-8-sig") as csvFile:
            try:
                d = dict()
                reader = csv.DictReader(csvFile, delimiter=",", quotechar="\"", lineterminator="\n")
                for row in reader:
                    d[row["Set"]] = row
            except:
                print("\nParsing sets failed at row " + str(len(self.setsDict)+1) + ": \n" + str(row))
                raise
            finally:
                return d

    def initialize(self):
        print("Initializing Parser")
        self.cryptDict = self.parseCrypt()
        self.libraryDict = self.parseLibrary()
        self.setsDict = self.parseSets()
        self.initialized = True

    def getCard(self, cardName):
        if self.initialized == False:
            print("Parser not initialized!")

        tmpCardName = cardName
        if tmpCardName.endswith("*"):
            tmpCardName = cardName.replace("*", "").lower()
        for k in self.cryptDict.keys():
            if k.lower().startswith(tmpCardName):
                return self.cryptDict[k]
        for k in self.libraryDict.keys():
            if k.lower().startswith(tmpCardName):
                return self.libraryDict[k]
        for k in self.setsDict.keys():
            if k.lower().startswith(tmpCardName):
                print("Found set by name: " + k)
                return self.setsDict[k]
        '''
        else:
          if cardName in self.cryptDict:
            return self.cryptDict[cardName]
          elif cardName in self.libraryDict:
            return self.libraryDict[cardName]
          elif cardName in self.setsDict:
            return self.setsDict[cardName]
         '''

        print("Could not find card by name: " + cardName)
        return None