import pymongo, pprint
import matplotlib.pyplot as plt 
from pymongo import MongoClient


client = MongoClient("mongodb://reader:PegaReader@172.28.146.20:27017/Conan")
db = client['Conan']
collection = db.test_station_moving_info

# Matching a pair of station
pipeline = [
	{'$match' : {"End_Station": "S-OTA2", "Start_Station": "SW-DOWNLOAD"}}#,
#	{'$group' : { "_id": "$Config", 'Other': {"$push": "$DurationBetweenStationSecStatistic"}}}
]

# Pipeline2 
pipeline2 = [
        {'$match' : {"End_Station": "RF-OTA-1", "Start_Station": "VSWR-OTA"}}
]

# Pipeline3 
pipeline3 = [
        {'$match' : {"End_Station": "DISPLAY", "Start_Station": "BURNIN"}}
]


dataList = list(collection.aggregate(pipeline))
dataList2 = list(collection.aggregate(pipeline2))
dataList3 = list(collection.aggregate(pipeline3))


myList = []
myList2 = []
myList3 = []

for i in dataList: 
	if i["Config"] != "Overall":
		data = int(i["DurationBetweenStationSecStatistic"]['Mean'])
		if data < 20000:
			myList.append(data)

for i in dataList2:
        if i["Config"] != "Overall":
                data = int(i["DurationBetweenStationSecStatistic"]['Mean'])
                if data < 20000:
                        myList2.append(data)

for i in dataList3:
        if i["Config"] != "Overall":
                data = int(i["DurationBetweenStationSecStatistic"]['Mean'])
                if data < 20000:
                        myList3.append(data)

dataRange = max(myList) - min(myList)
print(max(myList))
print(max(myList2))
print(max(myList3))

plt.hist(myList, color = 'blue', edgecolor = 'black', 
	bins = int(dataRange/500), label='y', alpha= 0.5)

plt.hist(myList2, color = 'red', edgecolor = 'black',
        bins = int(dataRange/500), label='x', alpha=0.5)

plt.hist(myList3, color = 'green', edgecolor = 'black',
        bins = int(dataRange/500), label='z', alpha=0.5)

plt.title("End_Station: COEX2, Start_Station: COEX4")
plt.xlabel("secs")
plt.ylabel("configs")
plt.legend(loc = 'upper right')
plt.show()


