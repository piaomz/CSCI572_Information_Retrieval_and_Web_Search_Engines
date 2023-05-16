import json
import csv


def readJson(filename):
    with open(filename, 'r') as openfile:
        json_object = json.load(openfile)
        return json_object


def readtxt(filename):
    queries = []
    with open('100QueriesSet4.txt') as f:
        while(True):
            line = f.readline()
            if(line):
                line = line[:-2]
                queries.append(line)
            else:
                break
    f.close()
    return queries


def writeCVS(filename):
    file = open(filename, mode='w')
    writer = csv.writer(
        file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    return writer
    #writer.writerow(['John Smith', 'Accounting', 'November'])
    #writer.writerow(['Erica Meyers', 'IT', 'March'])


def removeDiffer(URLs):
    for i in range(len(URLs)):
        # remove http and https
        if(URLs[i][:7] == 'http://'):
            URLs[i] = URLs[i][7:]
        elif(URLs[i][:8] == 'https://'):
            URLs[i] = URLs[i][8:]
        # remove www.
        if(URLs[i][:4] == 'www.'):
            URLs[i] = URLs[i][4:]
        # remove / in the end
        if(URLs[i][-1] == '/'):
            URLs[i] = URLs[i][:-1]
    return URLs


def calculateOverlap(googleURLs, myURLs):
    counter = {}
    countofOverlap = 0
    for url in googleURLs:
        if(url in counter.keys()):
            counter[url] = 1
        else:
            counter[url] = 0
    for url in myURLs:
        if(url in counter.keys()):
            counter[url] = 1
        else:
            counter[url] = 0
    for key in counter.keys():
        if(counter[key] == 1):
            countofOverlap += 1
    return countofOverlap, 100.0 * countofOverlap / len(googleURLs)


def calculateRho(googleURLs, myURLs):
    countOfOverlap = 0
    sumOfDi2 = 0
    for gurl in googleURLs:
        for murl in myURLs:
            if(gurl == murl):
                grank = googleURLs.index(gurl)+1
                mrank = myURLs.index(murl)+1
                sumOfDi2 += (grank-mrank)*(grank-mrank)
                # print(grank,mrank,(grank-mrank)*(grank-mrank))
                countOfOverlap += 1
                break
    if(countOfOverlap == 0):
        rho = 0
    elif(countOfOverlap == 1):
        if(sumOfDi2 == 0):
            rho = 1
        else:
            rho = 0
    else:
        rho = 1 - 6.0*sumOfDi2 / \
            (countOfOverlap*(countOfOverlap*countOfOverlap-1))
    return rho


queries = readtxt("100QueriesSet4.txt")
googleRes = readJson('Google_Result4.json')
myRes = readJson('hw1.json')
writer = writeCVS('hw1.csv')
writer.writerow(
    ["Queries", "Number of Overlapping Results", "Percent Overlap", "Spearman Coefficient"])
aveNumOfOl = 0.0
aveOl = 0.0
aveRho = 0.0
count = 0
for query in queries[:]:
    count += 1
    googleURLs = googleRes[query]
    myURLs = myRes[query]
    # remove the elements in url that dont matter
    googleURLs = removeDiffer(googleURLs)
    myURLs = removeDiffer(myURLs)
    # print(googleURLs)
    # print(myURLs)
    NumofOl, ol = calculateOverlap(googleURLs, myURLs)
    rho = calculateRho(googleURLs, myURLs)
    aveNumOfOl += NumofOl
    aveOl += ol
    aveRho += rho
    writer.writerow(["Query "+str(count), NumofOl, ol, rho])
    print(query, NumofOl, ol, rho)

aveNumOfOl /= len(queries)
aveOl /= len(queries)
aveRho /= len(queries)
writer.writerow(["Averages", aveNumOfOl, aveOl, aveRho])
print("average:", aveNumOfOl, aveOl, aveRho)
