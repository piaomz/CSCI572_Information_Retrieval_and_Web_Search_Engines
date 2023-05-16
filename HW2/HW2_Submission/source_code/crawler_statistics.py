import csv


def main():
    fetch_stat()
    urls_stat()
    visit_stat()

    output_txt()


def output_txt():
    with open('res/CrawlReport_usatoday.txt', mode='w') as file:
        file.writelines("Name: Mingzhe Piao\n")
        file.writelines("USC ID: 2538642079\n")
        file.writelines("News site crawled: usatoday.com\n")
        file.writelines("Number of threads: 7\n\n")
        file.writelines("Fetch Statistics\n")
        file.writelines("================\n")
        file.writelines("fetches attempted: "+str(fetches_attempt)+"\n")
        file.writelines("fetches succeeded: "+str(fetches_succeeded)+"\n")
        file.writelines("fetches failed or aborted: "+str(fetches_fa)+"\n\n")
        file.writelines("Outgoing URLs:\n")
        file.writelines("==============\n")
        file.writelines("Total URLs extracted: "+str(total)+"\n")
        file.writelines("unique URLs extracted: " +
                        str(len(list(unique_urls.keys())))+"\n")
        file.writelines("unique URLs within News Site: " +
                        str(insite_count)+"\n")
        file.writelines("unique URLs outside News Site: " +
                        str(outsite_count)+"\n\n")
        file.writelines("Status Codes:\n")
        file.writelines("=============\n")
        for key in sorted(list(status_code_count.keys())):
            textcode = ""
            if(key == "200"):
                textcode = "OK"
            elif(key == "301"):
                textcode = "Moved Permanently"
            elif(key == "302"):
                textcode = "Found"
            elif(key == "303"):
                textcode = "See Other"
            elif(key == "307"):
                textcode = "Temporary Redirect"
            elif(key == "308"):
                textcode = "Permanent Redirect"
            elif(key == "404"):
                textcode = "Not Found"
            elif(key == "500"):
                textcode = "Internal Server Error"
            file.write(key+" "+textcode+": "+str(status_code_count[key])+'\n')
        file.writelines("\n")
        file.writelines("File Sizes:\n")
        file.writelines("===========\n")
        file.writelines("< 1KB: "+str(KB1)+'\n')
        file.writelines("1KB ~ <10KB: "+str(KB10)+'\n')
        file.writelines("10KB ~ <100KB: "+str(KB100)+'\n')
        file.writelines("100KB ~ <1MB: "+str(MB1)+'\n')
        file.writelines(">= 1MB: "+str(MTMB1)+'\n\n')
        file.writelines("Content Types:\n")
        file.writelines("==============\n")
        for key in content_type.keys():
            file.writelines(key+": "+str(content_type[key])+'\n')


def fetch_stat():
    with open('res/fetch_usatoday.csv', mode='r')as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        global fetches_attempt
        global fetches_succeeded
        global fetches_fa
        global status_code_count
        fetches_attempt = 0
        fetches_succeeded = 0
        fetches_fa = 0
        status_code_count = {}

        next(csvFile)
        # displaying the contents of the CSV file
        for lines in csvFile:
            fetches_attempt += 1
            if(int(lines[1]) < 300 and int(lines[1]) >= 200):
                fetches_succeeded += 1
            else:
                fetches_fa += 1
            if(lines[1] not in status_code_count.keys()):
                status_code_count[lines[1]] = 1
            else:
                status_code_count[lines[1]] += 1
            # print(lines)
        print(fetches_attempt, fetches_succeeded, fetches_fa)
        print(status_code_count)


def visit_stat():
    with open('res/visit_usatoday.csv', mode='r')as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        next(csvFile)

        global KB1
        global KB10
        global KB100
        global MB1
        global MTMB1
        global content_type
        global outlinks
        KB1 = 0
        KB10 = 0
        KB100 = 0
        MB1 = 0
        MTMB1 = 0
        content_type = {}
        outlinks = 0

        for lines in csvFile:
            if(int(lines[1]) < 1024):
                KB1 += 1
            elif(int(lines[1]) < 10*1024):
                KB10 += 1
            elif(int(lines[1]) < 100*1024):
                KB100 += 1
            elif(int(lines[1]) < 1024*1024):
                MB1 += 1
            else:
                MTMB1 += 1
            if(lines[3] not in content_type.keys()):
                content_type[lines[3]] = 1
            else:
                content_type[lines[3]] += 1
            outlinks += int(lines[2])

        print(KB1, KB10, KB100, MB1, MTMB1)
        print(content_type)
        print(outlinks)


def urls_stat():
    with open('res/urls_usatoday.csv', mode='r')as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        next(csvFile)
        global total
        global unique_urls
        global insite_count
        global outsite_count
        total = 0
        unique_urls = {}
        insite_count = 0
        outsite_count = 0
        for lines in csvFile:
            total += 1
            unique_urls[lines[0]] = 2
            if(lines[1] == "OK"):
                unique_urls[lines[0]] = 0
            else:
                unique_urls[lines[0]] = 1
        for key in unique_urls.keys():
            if(unique_urls[key] == 0):
                insite_count += 1
            else:
                outsite_count += 1
        print(total, len(list(unique_urls.keys())), insite_count, outsite_count)


if __name__ == "__main__":
    main()
