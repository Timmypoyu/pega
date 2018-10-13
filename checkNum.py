import pymongo, pprint
import matplotlib.pyplot as plt
import dateutil.parser
from pymongo import MongoClient


client = MongoClient("mongodb://reader:PegaReader@172.28.146.20:27017/Conan")
db = client['Conan']
collection = db.test_station_moving_info

dateStr = "2018-07-01T00:00:00.000Z"
myDatetime = dateutil.parser.parse(dateStr)

print(myDatetime)


stationList = list(db.test_note_current.find({"Config":"4G57WF","Serial":{"$ne":0}},{"_id":0,"StationName":1}).sort("Serial", 1))

# Matching a pair of station
for j in stationList:
	for k in stationList: 
		pipeline = [
			{'$match' : { "Config": "Overall", "CutTime": { "$lt": myDatetime} , "End_Station": j["StationName"], "Start_Station": k["StationName"]
			}},
			{
			'$group': 
			{ 
			"_id" : { "End_Station": "$End_Station", "Start_Station": "$Start_Station"},
				"totalNumber": { "$sum": "$DurationBetweenStationSecStatistic.Num"},
				"count" : {"$sum": 1} 
			}}
		]
 
		dataList = list(collection.aggregate(pipeline))
		#print(dataList)

		dataList = [ x for x in dataList if x['totalNumber'] > 1000] 

		if dataList:
			print("List not empty")
			print("End_Station is: " + j["StationName"])
			print("Start_Station is: " + k["StationName"])
		
		del dataList 
			

#stationList = list(db.test_note_current.find({"Config":"4G57WF","Serial":{"$ne":0}},{"_id":0,"StationName":1}).sort("Serial", 1))
#dataList = list(collection.aggregate(pipeline))

#print(dataList[0])

#myList = []
#pprint.pprint(stationList)
#pprint.pprint(dataList)
#pprint.pprint(len(dataList))


#for i in dataList:
#	data = int(i["totalNumber"])
#	if data > 20: 
#		myList.append(data)


#print(myList)

#dataRange = max(myList) - min(myList)

#plt.hist(myList, color = 'blue', edgecolor = 'black',
#        bins = int(dataRange/1), alpha= 0.5)

#plt.title("Num Count")
#plt.xlabel("Numbers of SN through a pair of Station")
#plt.ylabel("nums")
#plt.show()

#plt.title("Config:Overall Num>21")
#plt.xlabel("Num")
#plt.ylabel("Number")
#plt.show()

