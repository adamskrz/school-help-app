import xml.etree.ElementTree as ET  
from datetime import datetime
import requests

from secrets import TravelineID, TravelinePassword

def TravelineAPI(ATCOcode, TravelineID, TravelinePassword):
    requestID = '0'
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")   #generate timestamp for request

    #create XML get request compliant with the Traveline SIRI API
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Siri version="1.0" xmlns="http://www.siri.org.uk/"><ServiceRequest><RequestTimestamp>' \
        + timestamp \
        + '</RequestTimestamp><RequestorRef>' \
        + TravelineID \
        + '</RequestorRef><StopMonitoringRequest version="1.0"><RequestTimestamp>' \
        + timestamp \
        + '</RequestTimestamp><MessageIdentifier>' \
        + requestID \
        + '</MessageIdentifier><MonitoringRef>' \
        + ATCOcode \
        + '</MonitoringRef></StopMonitoringRequest></ServiceRequest></Siri>'
    
    #Send created POST request
    data = requests.post('http://nextbus.mxdata.co.uk/nextbuses/1.0/1', data=xml, auth=(TravelineID, TravelinePassword)).text

    #Load response XML data to object with xml module
    ns = {'bus': 'http://www.siri.org.uk/',}
    tree = ET.fromstring(data)
    root = tree.find("./bus:ServiceDelivery/bus:StopMonitoringDelivery", ns)

    #Load XML data into a dictionary
    currentInfo = []
    time = root.find('bus:ResponseTimestamp', ns).text
    for bus in root.findall('bus:MonitoredStopVisit', ns):
        trip = bus.find('bus:MonitoredVehicleJourney', ns)
        line = trip.find('bus:PublishedLineName', ns).text
        destination = trip.find('bus:DirectionName', ns).text
        operator = trip.find('bus:OperatorRef', ns).text
        live = True
        if operator[:5] == '_noc_':     #The end of the operator name is _noc_ if data is from schedules
            live = False                #Mark data as not live if _noc_ found
            operator = operator[5:]     #Shorten oprator text
        vehicleRef = None
        for timing in trip.findall('bus:MonitoredCall', ns):
            EDT = getattr(timing.find('bus:ExpectedDepartureTime', ns), 'text', None)
            ADT = timing.find('bus:AimedDepartureTime', ns).text 
            arrival = {"requestTime": time, "line": line, "operator": operator, "live": live, "vehicleRef": vehicleRef, "destination": destination, "EDT": EDT, "ADT": ADT}
            currentInfo.append(arrival)

    return currentInfo

if __name__ == "__main__":      #test data
    ATCOcode = '03700308'
    print(TravelineAPI(ATCOcode, TravelineID, TravelinePassword))


