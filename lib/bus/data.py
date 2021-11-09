if __name__=='__main__':
    from helper import traveline, ReadingBuses, TfL, api_secrets
else:
    from .helper import traveline, ReadingBuses, TfL, api_secrets

import pickle
from datetime import timezone
from datetime import datetime
from datetime import timedelta


def AllBusData(ATCOcode,debug = False):
    
    if debug:
        """ For testing, debug flag can be set to True, then the function will
        return some past data instead of requesting new data from APIs """
        result = []
        with open('testdata.data', 'rb') as filehandle:
            result = pickle.load(filehandle)
        return result
    else:
        #defining Reading Buses and TfL operator codes, based on Traveline NOC database
        ReadingNOCcodes = ['GBRB', 'GLRB', 'KENN', 'NEWB', 'RBUS', 'THVB']
        TfLNOCcodes = ['ABLO', 'ALNO', 'ALSO', 'BTRI', 'CTPL', 'DLBU', 'ELBG', 'LGEN', 'LONC', 'MBGA', 'GAHL', 'LUTD', 'FWYK', 'METR', 'MTLN', 'SULV', ]

        

        #request bus time data from
        travelineData = traveline.TravelineAPI(ATCOcode, api_secrets.TravelineID, api_secrets.TravelinePassword)
        
        # by default, program assumes there are no services by TfL or RDB
        readingFlag = False
        londonFlag = False

        combinedData = []

        for bus in travelineData: 
            # iterating through buses from Traveline, each bus is represented as a dictionary
            if bus['operator'] in TfLNOCcodes:
                londonFlag = True
                #if the bus is operated by TfL, flag this and ignore the data
            else:
                if bus['operator'] in ReadingNOCcodes:
                    readingFlag = True
                    #if a bus is operated by RDB, flag this, but use the data anyway
                if bus['requestTime'] != None:
                    #if there is a request time, parse it and replace it with a python timedate object
                    timeObject = datetime.strptime(bus['requestTime'], "%Y-%m-%dT%H:%M:%S.%f%z")
                    bus['requestTime'] = timeObject
                if bus['ADT'] != None: 
                    #if there is a scheduled time, parse it and replace it with a python timedate object
                    ADTobject = datetime.strptime(bus['ADT'], "%Y-%m-%dT%H:%M:%S.%f%z")
                    bus['ADT'] = ADTobject
                    #also set the best guess time to the planed departure
                    bus['departure'] = ADTobject
                if bus['EDT'] != None: 
                    #if there is a live time, parse it and replace it with a python timedate object
                    EDTobject = datetime.strptime(bus['EDT'], "%Y-%m-%dT%H:%M:%S.%f%z")
                    bus['EDT'] = EDTobject
                    #as there is a live time, set the best guess time to this
                    bus['departure'] = EDTobject
                if bus['EDT'] != None and bus['ADT'] != None:
                    #if there is a scheduled and live time, calculate delay
                    bus['delay'] = bus['EDT'] - bus['ADT']

                combinedData.append(bus)

        if readingFlag == True:
            #if a bus operated by RDB was detected, get their data as well
            readingData = ReadingBuses.ReadingAPI(ATCOcode, api_secrets.readingAPIkey)
            for bus in readingData:
                #iterate through RDB data as woth traveline data
                updatedFlag = False
                if bus['requestTime'] != None:
                    timeObject = datetime.strptime(bus['requestTime'], "%Y-%m-%dT%H:%M:%S%z")
                    bus['requestTime'] = timeObject
                if bus['ADT'] != None: 
                    ADTobject = datetime.strptime(bus['ADT'], "%Y-%m-%dT%H:%M:%S%z")
                    bus['ADT'] = ADTobject
                    bus['departure'] = ADTobject
                if bus['EDT'] != None: 
                    EDTobject = datetime.strptime(bus['EDT'], "%Y-%m-%dT%H:%M:%S%z")
                    bus['EDT'] = EDTobject
                    bus['departure'] = EDTobject
                if bus['EDT'] != None and bus['ADT'] != None:
                    bus['delay'] = bus['EDT'] - bus['ADT']
                
                for oldBus in combinedData:
                    # compare each bus from the traveline data with this new data to find a match
                    if bus['ADT'] == oldBus['ADT'] and bus['line'] == oldBus['line']:
                        #if the bus' line and scheduled time match between RDB and Traveline data
                        # update the travelline dtat attributes with the new RDB ones
                        oldBus['live'] = bus['live']
                        oldBus['vehicleRef'] = bus['vehicleRef']
                        oldBus['destination'] = bus['destination']
                        oldBus['departure'] = bus['departure']
                        oldBus['EDT'] = bus['EDT']
                        updatedFlag = True
                        #if the bus was a match and updated a existing data point, flag this

                if updatedFlag == False:
                    #if a match with existing data was not flagged, add this new data
                    combinedData.append(bus)

        if londonFlag == True:
            #if any london buses were found to operate at the stop, call the TfL API
            londonData = TfL.TfLAPI(ATCOcode, api_secrets.TFLappID, api_secrets.TFLappKey)
            for bus in londonData:
                #iterate through buses gained from TfL API
                if bus['requestTime'] != None:
                    #parse request time to datetime object
                    timeObject = datetime.strptime(bus['requestTime'][:25], "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
                    bus['requestTime'] = timeObject

                if bus['EDT'] != None: 
                    #parse live time to datetime object
                    EDTobject = datetime.strptime(bus['EDT'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    bus['EDT'] = EDTobject
                    bus['departure'] = EDTobject
                
                combinedData.append(bus) #add processed data to list

        result = sorted(combinedData,key=lambda x : x['departure']) # sort data by departure time

        return result

def prettyPrint(result):
    #print out the bus times in a human readable way for debug purposes
    for bus in result:
        print('Line ' + bus['line'] + ' leaves at ' + bus['departure'].astimezone(tz=None).strftime("%H:%M:%S") + ('!' if bus['live'] else ""))
        min, sec = divmod((bus['departure']-bus['requestTime']).total_seconds(),60)
        print('Operator: ' + bus['operator'] + ' ' + str(int(min)) + " mins " + str(int(sec)) + " seconds")
        if 'delay' in bus:
            if bus['delay'] != None:
                min, sec = divmod((bus['delay']).total_seconds(),60)
                print('Delay: ' + str(int(min)) + " mins " + str(int(sec)) + " seconds")
        print("")


if __name__ == "__main__":
    #module testing data
    ATCOcode = '03700308'
    result = AllBusData(ATCOcode,True)

    print(result)

    prettyPrint(result)