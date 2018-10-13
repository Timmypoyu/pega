Over the course of four weeks, I have studied a few statistical method for comparison (T, F test), clustering method (Mostly K-means, Hierarchial clustering with python implementation), mongoDB, and about five weeks worth of machine learning course by Andrew Ng. 

1)

First upon observing the data in test_station_moving_info, I checked how many pairs of stations there is. 
(
	station.aggregate([ { $match:{ "DurationBetweenStationSecStatistic.Num": {'$gt': 2}, CutTime: { '$lt': ISODate("2018-07-00T00:00:00.000Z")}}}, {$group:{ _id: { End_Station: "$End_Station", Start_Station: "$Start_Station"}}}]).itcount()
)

Also, looking further into how many configs there are from 6/19.

2)

There are 1021 pairs of station before July, that has more than 1 SN passing by.
Then using the python script <set1.py>, I drew a few overlapping histograms to observe the overall distribution (X-axis: the amount of configs, Y-axis: Mean 移動的平均時間). I discover there is A LOT of noise, meaning that there is a lot of pairs of station that has only a few SN going through. 

3)

Andrew suggested that I summed up all of the overall number of SN of every pair of stations to avoid double-counting with my approach in (2)

db.getCollection('test_station_moving_info').aggregate([
    {
        $match:{Config: "Overall",  "DurationBetweenStationSecStatistic.Num": {'$gt': 21}}},
    {
        $group:
        {
            _id: {End_Station: "$End_Station", Start_Station: "$Start_Station"},
            totalNumber: { $sum: "$DurationBetweenStationSecStatistic.Num"},
            count: { $sum: 1}
        }
    }
  ]
)

Further more, to find matching pairs of station in test_note_current
<Command> db.test_note_current.find({Config:"4G57WF",Serial:{$ne:0}},{_id:0,StationName:1}).sort({Serial:1})

The command generate a list with which I loop through to find consecutive pairs of station using <checkNum.py> which generate a list of pairs of stations that meet three criteria: 
1) match list above 
2) has more than 1000 sn 
3) before July first 

4) 
I picked ten pairs (exclusing any pair with SW-Download) of stations, export them from mongodb using shell script <mongoexport_script.sh>, using <tableScript.py> to 1) find out all the configs that are shared among the ten station, 2) calculate the total average of each pairs of station for wach configs, 3) format the final set of data into a csv file ready to be fed into a clustering algorithm. 

5) 
K-Means vs Hierarchial clustering 

Andrew suggested that I figure out how to group the Configs, so I decided to use the ten stations generated in (3) as clustering features to cluster individual Configs. The difference between K-Means and Hierarchial clustering in using K-Means, I have to specify how many clusters I want, but in using Hierarchial clustering, I dont have to specify the number of clusters, instead hierarchial clustering would find the nearest config until all the data is one big cluster. 

For this step, I used <cluster.py> to draw dendrogram (樹枝圖), which I can then find out the configs belongs to which cluster according to the maximum distance I specify. 
