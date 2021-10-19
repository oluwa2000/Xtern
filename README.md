# Xtern
Creating schedule using google API's
Xtern Project Write Up

For this project I used the skills I have learnt from python, pandas data frame, the google API and the Predict Hq API. 

The problem given was to find the most convenient work location to be used for xtern in next summer’s internship programs and to then find a list of events to be done around that location. My approach to this was to analyze all the suggested locations finding which restaurants would have the best ratings around them for the suggested locations. For this part I created a get_info function to get started.

Get_info function:
The get_info function takes in a specific location, which in our test cases will be locations of the various locations to which we are to choose from. It also takes in the miles of radius in which we will be choosing from and a variable for the type of event we will be looking for. I then used the google maps API to find nearby data for those specific details and collected specific data on the location events such as ratings, name of the event, total_ratings, e.t.c. i cleaned this data even further by removing duplicate events or restaurant names from my google API and only accepting locations who where operational. After obtaining this data it is then saved into an excel folder titled “Location details” for that specific location.

After I use the get info function, I then move to the Analysis functions.

Analyze function:
which takes in the dataset of the different locations. For deciding which location to pick from I decided to create a list of the different event types and use the get_info function using the locations from the data set, setting a radius of 15 miles as a random choice (I have made this variable). I then created tables for information on different events and restaurants for each location to compare them and choose which would be the best choice. After looking at the excel documents I decided to go with the ratings for each criteria of each location and create a new table with the average rating per criteria per location. This led to my "output.xlsx" file which I saved in my main repository.

after saving my output.xlsx file I utilized the plotly library to make visualiztions to see which location had the overall highest ratings in all categories by taking each locations total ratings and finding the mean for them and saving in it i na bar chart titled "analysis.html". This function also returns the location with the highest overall ratings for all categories of events which i decided to use as my convenient location. This led to my add_info function.

add_info:
My add_info function was used for the specific location chosen after my analysis. This uses the get_info method, a new top_ten method (for choosing the toping ten restaurants) and an event function (which gives me information on 5 eevents and a conference that can be visited). I first get information on that specific location and then filter out the top ten highested rated restauarants to choose from for the schedule. I then use the events function which uses the Open hq API to get information about upcoming events around that specific location in a 10km radius and makes sure to get events biweekly. The limitations to this API is that it does not seem to have information for events happening next summer 2022 so i relied on dates of events for the upcoming months of november and decemeber instead. After doing all of this i added these bits of information into a pandas dataframe and i saved it as schedule.xlsx. 
![image](https://user-images.githubusercontent.com/77019673/137935341-cf80c5e5-6eb3-45bb-8e37-a4ecf9ddf3e8.png)
