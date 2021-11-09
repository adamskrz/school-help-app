import json
import requests
import secrets

def TfLAPI(ATCOcode, appID, appKey):
    #create GET request for the selected stop
    auth = {'app_id': appID,  'app_key': appKey}
    data = requests.get("https://api.tfl.gov.uk/StopPoint/" + ATCOcode + "/arrivals", params = auth)

    #load server response JSON data to dictionary with json module
    jsonData = json.loads(data.text)

    #convert dictionary to program format
    currentInfo = []
    for bus in jsonData:
        arrival = {"requestTime": bus['timestamp'], "line": bus['lineName'], "operator": "TfL", "live": True, "destination" : bus['towards'], "vehicleRef": bus['vehicleId'], "EDT": bus['expectedArrival']}
        currentInfo.append(arrival)     #add single bus data to complete data

    return currentInfo

if __name__ == "__main__":      #test data
    ATCO = "03700308"
    print(TfLAPI(ATCO, secrets.TfLappID, secrets.TfLappKey))


