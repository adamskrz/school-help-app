import csv


def StopInfo(searchTerm):
    search = searchTerm.strip("0")
    file = open('AllStops.csv')
    csv_file = csv.DictReader(file)

    for row in csv_file:
        if row['ATCOCode'] == search or row['NaptanCode'] == search:
            return row

if __name__ == "__main__":
    searchTerm = '03700308'
    print(StopInfo(searchTerm))

