import xml.etree.ElementTree as ET  
from datetime import datetime
import requests
from distutils import util
import secrets

def ReadingAPI(ATCOcode, apiKey):
    #Get departures for chosen stop
    data = requests.get("https://rtl2.ods-live.co.uk/api/siri/sm?key=" + apiKey + "&location=" + ATCOcode).text

    #Load departure information to object with xml module
    tree = ET.fromstring(data)
    ns = {'bus': 'http://www.siri.org.uk/siri',}
    root = tree.find("./bus:ServiceDelivery/bus:StopMonitoringDelivery", ns)

    #Parse XML data into dictionary
    currentInfo = []
    time = root.find('bus:ResponseTimestamp', ns).text
    for bus in root.findall('bus:MonitoredStopVisit', ns):
        trip = bus.find('bus:MonitoredVehicleJourney', ns)
        line = trip.find('bus:PublishedLineName', ns).text
        operator = trip.find('bus:OperatorRef', ns).text
        live = getattr(trip.find('bus:Monitored', ns), 'text', False)
        destination = trip.find('bus:DestinationName', ns).text
        vehicleRef = getattr(trip.find('bus:VehicleRef', ns), 'text', None)
        for timing in trip.findall('bus:MonitoredCall', ns):
            EDT = getattr(timing.find('bus:ExpectedDepartureTime', ns), 'text', None)
            ADT = timing.find('bus:AimedDepartureTime', ns).text
            arrival = {"requestTime": time, "line": line, "operator": operator, "live": util.strtobool(live), "vehicleRef": vehicleRef, 
            "destination": destination, "EDT": EDT, "ADT": ADT}
            currentInfo.append(arrival)
    
    return currentInfo      #return dictionary contents

if __name__ == "__main__":      #test data
    ATCO = "03700308"
    print(ReadingAPI(ATCO, secrets.readingAPIkey))

