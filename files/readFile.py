import os
import csv


class ReadFile:
    def __init__(self, directory, file=''):
        self.file = file
        self.path = directory
        self.listdir = os.listdir(directory)
        self.totalCount = {}

    def getProductList(self):
        print(self.listdir)

    def listFiles(self):
        return self.listdir

    def numberOfFiles(self):
        for singleFile in self.listdir:
            nameBreakdown = singleFile.split("_")
            if nameBreakdown[0] in self.totalCount:
                self.totalCount[nameBreakdown[0]] += 1
            else:
                self.totalCount[nameBreakdown[0]] = 1
        return len(self.totalCount)

    def readShopifyContent(self):
        csvFileContent = []
        with open(self.path + os.path.sep + self.file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if(row['Title'] != ""):
                    csvFileContent.append(row)
        return csvFileContent

    def readEleventaContent(self):
        csvFileContent = []
        with open(self.path + os.path.sep + self.file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                csvFileContent.append(row)
        return csvFileContent

    def createCSVFile(self, filepath, filename, keys, data):
        with open(filepath + os.path.sep + filename, mode="w") as csv_file:
            fieldnames = keys
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
