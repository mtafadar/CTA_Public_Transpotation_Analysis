#Name: Mosrour Tafadar
#  CS 341 Fall 2022
# University of Illinois


import sqlite3
import matplotlib.pyplot as plt


##################################################################
#
# print_stats
#
# SQL queries to retrieve and output basic stats.
# This functions retrive 
# 1. Total number of Station 
# 2.  Total number of Stops
# 3.  Total number of ride entries 
# 4.  Date range (from ride started to when ride ended)
# 5.  Total Ridership 
# 6. Weekday Ridership (Monday - Friday)
# 7. Saturday Ridership 
# 8. Sunday  or Holiday Ridership 
#
####################################################################

def print_stats(dbConn):

   ####### I did seperate cursor so that its easy to read and understand ######
    dbCursor = dbConn.cursor()  
    dbCursorStop = dbConn.cursor()
    dbCursorTotalRide = dbConn.cursor()
    dbCursorDateRange = dbConn.cursor()
    dbCursorTotalRidership = dbConn.cursor()
    dbCursorWeekdayRider = dbConn.cursor()
    dbCursorSaturdayRider = dbConn.cursor()
    dbCursorSunOrHoliRider = dbConn.cursor()
    #db cursor for sunday or holiday

    ######## This portion is designated for SQL Quesries ###
    sqlNumberofStations = "Select count(*) From Stations;"
    SqlNumberofStops = "Select count(Stop_ID) from Stops;"
    SqlNumberofTotalRide = "Select count(Num_Riders) from Ridership;"
    SqlDateRange = " Select Date(Min(Ride_Date)) as FromDate, Date(max(Ride_Date)) ToDate from Ridership;"
    SqlTotalRidership = "Select sum(num_Riders) from Ridership;"
    SqlWeekdayRidership = "Select sum(Num_Riders) from Ridership Where Type_of_day = \"W\";" # W stand for weekday 
    SqlSaturdayRidership = "Select sum(Num_Riders) from Ridership Where Type_of_day = \"A\";" # A stands for Saturday 
    SqlSundayOrHoliRidership = "Select sum(Num_Riders) from Ridership Where Type_of_day = \"U\";" # u stands for Sunday or Holiday 

    #######  --- #############################################

    print("General stats:")

    ###########Executing ########
    dbCursor.execute(sqlNumberofStations)
    dbCursorStop.execute(SqlNumberofStops)
    dbCursorTotalRide.execute(SqlNumberofTotalRide)
    dbCursorDateRange.execute(SqlDateRange)
    dbCursorTotalRidership.execute(SqlTotalRidership)
    dbCursorWeekdayRider.execute(SqlWeekdayRidership)
    dbCursorSaturdayRider.execute(SqlSaturdayRidership)
    dbCursorSunOrHoliRider.execute(SqlSundayOrHoliRidership)

    #############################################

    ####Fetching############
    fetchStation = dbCursor.fetchone()
    fetchStops = dbCursorStop.fetchone()
    fetchTotalRide = dbCursorTotalRide.fetchone()
    fetchDateRange = dbCursorDateRange.fetchall()
    fetchTotalRidership = dbCursorTotalRidership.fetchone()
    fetchWeekdayRider = dbCursorWeekdayRider.fetchone()
    fetchSaturdayRider = dbCursorSaturdayRider.fetchone()
    fetchSunHoliRider = dbCursorSunOrHoliRider.fetchone()
    #Fetching #############################################

  ##### Outputting  generic stats ############ 
   # f here of  for formating purpose (it is a way to format  string that is more readable and fast)
    print("  # of stations:", f"{ fetchStation[0]:,}")
    print("  # of stops:", f"{fetchStops[0]:,}")
    print("  # of  ride entries:", f"{ fetchTotalRide[0]:,}")
    for row in fetchDateRange:
        print("  date range: ", row[0], "-", row[1])
    print("  Total ridership:", f"{fetchTotalRidership[0]:,}")
    weekdayRiderPercentage = ((fetchWeekdayRider[0] / fetchTotalRidership[0]) *
                              100)
    formatWeekdayRiderPercentage = "{:.2f}".format(weekdayRiderPercentage)


  #   the * with 100 is just for to get the percentage of the rider for weekday, Saturday  or Sunday or holiday 
    saturdayRiderPercantage = (fetchSaturdayRider[0] /
                               fetchTotalRidership[0]) * 100
    formatSaturdayRiderPercantage = "{:.2f}".format(saturdayRiderPercantage)
    sunOrHolidayRiderPercentage = (fetchSunHoliRider[0] /
                                   fetchTotalRidership[0]) * 100 
    formatSunOrHolidayRiderPercantage = "{:.2f}".format(
        sunOrHolidayRiderPercentage)
    print("  Weekday ridership:", f"{fetchWeekdayRider[0]:,}",
          "(" + formatWeekdayRiderPercentage + "%)")
    print("  Saturday ridership:", f"{ fetchSaturdayRider[0]:,}",
          "(" + formatSaturdayRiderPercantage + "%)")

    print("  Sunday/holiday ridership:", f"{ fetchSunHoliRider[0]:,}",
          "(" + formatSunOrHolidayRiderPercantage + "%)")




# This function   retrive Station ID and Station_Name
# from the Station Table
#  Its accept the wildcard user input from the  user and retrive the information
# The first parameter  is used for executing  Sql    query and 2nd parameter  take wildcard user input for station name

def station_name_from_user(dbConn, value):

    count = 0
    dbCursor = dbConn.cursor()
    sqlUserStations = """Select Station_ID, Station_Name from Stations Where  
     Station_Name like ? 
    order by Station_Name ASC"""
    # the question mark here will be replace by the value during SQL search query when its executed
    dbCursor.execute(sqlUserStations, [value]) # the value  here   will be excuted in place of ? 
    fetchStation = dbCursor.fetchall()
    if (len(fetchStation) == 0):
        print(" **No stations found...")
    # if (len(fetchStation) == 1):
    #     print("", fetchStation[0][0], ":", fetchStation[0][1])
    else:
        for row in fetchStation:
            if (count == 0):   # this is primarily for  matching the gradescope output style :) 
                print("", row[0], ":", row[1]) 
                count = count + 1
            else:
                print(row[0], ":", row[1])



#######
#
#This   function sum the total number of Rider of all time and return that value 
# The parameter   is for executing the Sql query 
#
#######
        
def calculate_total_rider(dbConn):
    dbCusorForTotalRider = dbConn.cursor()
    SqlForTotalRider = """ select Sum(Num_Riders) from Ridership;"""
    dbCusorForTotalRider.execute(SqlForTotalRider)
    fetchdbCusorForTotalRider = dbCusorForTotalRider.fetchone()
    return fetchdbCusorForTotalRider[0] # returning total # of riders 


######
# This functio query and print ridership at each station, in ascending order by station name
# It also print  each value of the station and percentage of the station across the total L ridership
#
#####
def  ridership_at_each_station(dbConn):
    dbCusorForStationAndNumber = dbConn.cursor()
     # This sql command  query sum of rider base on Station
    SqlForStationAndNumber = """Select Station_Name, 
   sum(Num_Riders) as NumberOfRider from Ridership 
   inner join Stations  on Stations.Station_ID = Ridership.Station_ID 
   group by Station_Name 
   order by Station_Name asc"""

    dbCusorForStationAndNumber.execute(SqlForStationAndNumber)
    # Execution of the  Sql
    fetchdbCusorForStationAndNumber = dbCusorForStationAndNumber.fetchall()
    totalsumOfRider = calculate_total_rider(dbConn)
    # this function  returns the sum of all  the riders

    #printing to the console
    print(" ** ridership all stations **")
    for row in fetchdbCusorForStationAndNumber:
        percantageofRider = (row[1] / totalsumOfRider) * 100
        # multiplication of 100 here just to make it percentage
        print(row[0], ":", f"{row[1]:,}", f"({percantageofRider:.2f}%)")
        # this is just the formatted output  as following
        #  Station_Name, Total rider, and   percentage of the rider out of total


######
#
# this function shows the top-10 busiest stations in terms of ridership, in descending order
#
#######
def top_ten_busiest_stations(dbConn):
    dbCursorMostBusiestStation = dbConn.cursor()
    # this query retrive the top 10 most businest  station and number of rider 
    sqlForMostBusiestStation = """Select Station_Name,  sum(Num_Riders) as NumberOfRider from Ridership 
         inner join Stations  on Stations.Station_ID = Ridership.Station_ID
         group by Station_Name
         order by NumberOfRider  Desc
         limit 10; """

    dbCursorMostBusiestStation.execute(sqlForMostBusiestStation)
    fetchMostBusiestStation = dbCursorMostBusiestStation.fetchall()
    totalsumOfRider = calculate_total_rider(dbConn) # getting the total rider 

    print(" ** top-10 stations **")

    for row in fetchMostBusiestStation:
        percantageofBusy = (row[1] / totalsumOfRider) * 100 # calculating the percentage
        print(row[0], ":", f"{row[1]:,}", f"({ percantageofBusy:.2f}%)") # f here is for formatting 


######
#
# this function shows least-10 busiest stations in terms of ridership, in ascending order by
#
#######

def least_busy_stations(dbConn):
    dbCursorLeastBusyStation = dbConn.cursor()
   # this query retrive the least  stations in terms of number of rider
    sqlForLeastBusiestStation = """Select Station_Name,  sum(Num_Riders) as NumberOfRider from Ridership 
          inner join Stations  on Stations.Station_ID = Ridership.Station_ID
          group by Station_Name
          order by NumberOfRider  asc
          limit 10;"""
    dbCursorLeastBusyStation.execute(sqlForLeastBusiestStation)
    fetchLeastBusiestStation = dbCursorLeastBusyStation.fetchall()
    totalsumOfRider = calculate_total_rider(dbConn) # getting total number of rider 

    print(" ** least-10 stations **")
    #  printing in a formateed way 
    for row in fetchLeastBusiestStation:
        percantageofBusy = (row[1] / totalsumOfRider) * 100 # calculating percentage
        print(row[0], ":", f"{row[1]:,}", f"({ percantageofBusy:.2f}%)")


###########
#  a line color from the user and output all stop names that are part of that line, in ascending order. If
# the line does not exist,
# This function take   line color from user output all stops that part of that line in ascending order
#  It also output stop’s direction and whether handicap-accessible
#
###########
def information_about_stations(dbConn, value):
    dbCursorColorBelongStationName = dbConn.cursor()
    # ADA -> 1 : handicap-accessible
    # ADA -> 0 : handicap-not-accessible
    SqlForColorBelongStationName = """Select Stop_Name, Direction, ADA from Stops
      inner join StopDetails   on StopDetails.Stop_ID  = Stops.Stop_ID
      inner join Lines On Lines.Line_ID = StopDetails.Line_ID
      where color = ?
      order by Stop_Name ASC;"""

    dbCursorColorBelongStationName.execute(SqlForColorBelongStationName,
                                           [value]) # value is user input (line color)
    fetchColorBelongStationName = dbCursorColorBelongStationName.fetchall()
    if (len(fetchColorBelongStationName) == 0):
        print("**No such line...")
    for row in fetchColorBelongStationName:
        if (row[2] == 1):
            AccessibleValue = "yes" #printing out whether handicap accessible  

        else:
            AccessibleValue = "no"
        print(row[0], ":", "direction = ", row[1], "(accessible?",
              AccessibleValue + ")")
      
#######
#
# This function Outputs total ridership by month, in ascending order 
# After the output, the user is given the option to plot the data
#  if the user input "y" then the  plot  shows 
# 
#######

def ridership_base_on_month(dbConn):
    dbcusorRiderBasedOnMonth = dbConn.cursor()
     #strftime is a sql built in function to grab desirable date format (in this case its month)
    SqlForRiderBasedOnMonth = """Select  strftime('%m', Ride_Date) as Month, sum(Num_Riders)  
     from  Ridership 
     group By Month;"""
    dbcusorRiderBasedOnMonth.execute(SqlForRiderBasedOnMonth)
    fetchRiderBasedOnMonth = dbcusorRiderBasedOnMonth.fetchall()
    print(" ** ridership by month **")
    for row in fetchRiderBasedOnMonth:
        print(row[0], ":", f"{row[1]:,}") #printing  with formatted 

    plotInput = input("Plot? (y/n)")  # taking input if user wants to see the input
    print();
    if (plotInput == 'y'): # if "y" we  will process  the ploting
        plt.clf()
        x = [] # variable to fetch x and y coordinate variable 
        y = []
        for row in fetchRiderBasedOnMonth:
            x.append(row[0])   # fetching the data
            y.append([row[1]])  # fetching the data 
       # setting up the plot  
        plt.xlabel("month") 
        plt.ylabel("number of riders (x*10^8")
        plt.title("monthly ridership")
        plt.ion() # for interactive mode of plot (so that it does not hang on terminal  after plot)
        plt.plot(x, y)
        plt.show()



def commandSevenFunction(dbConn):
    dbcusorRiderBasedOnYear = dbConn.cursor()
    sqlRiderBasedOnYear = """Select  strftime('%Y', Ride_Date) as Year, sum(Num_Riders)
                from  Ridership 
                group By Year
                order by Year asc;"""

    dbcusorRiderBasedOnYear.execute(sqlRiderBasedOnYear)
    fetchRiderBasedonYear = dbcusorRiderBasedOnYear.fetchall()

    print(" ** ridership by year **")
    for row in fetchRiderBasedonYear:
        print(row[0], ":", f"{row[1]:,}")

    plotInput = input("Plot? (y/n)")
    print();
    if (plotInput == 'y'):
        plt.clf()
        x = []
        y = []
        for row in fetchRiderBasedonYear:
            val = row[0][2:4]
            x.append(val)
            y.append([row[1]])

        plt.xlabel("year")
        plt.ylabel("number of riders (x*10^8")
        plt.title("yearly ridership")
        plt.ion()
        plt.plot(x, y)
        plt.show()


def CheckforNumberOfStation(dbConn, Val):
    dbcusorRiderBasedOnMonth = dbConn.cursor()
    sqlforStationValue = """Select Station_Name from Stations
     Where Station_Name like ? """
    dbcusorRiderBasedOnMonth.execute(sqlforStationValue, [Val])
    fetchStationValue = dbcusorRiderBasedOnMonth.fetchall()

    if (len(fetchStationValue) == 0):
        print(" **No station found...")
        return False

    if (len(fetchStationValue) > 1):
        print(" **Multiple stations found...")
        return False

    if (len(fetchStationValue) == 1):
        return True

    return


def CommandEightFunction(dbConn, year, firstStationName, secondStationName):
    dbcusorStation = dbConn.cursor()
    dbcusorStationNameByDate = dbConn.cursor()

    sqlforGenerictStation = """Select Station_ID, Station_Name From Stations 
  Where Station_Name  like  ? """

    sqlforMainQueryStationOne = """SELECT 
  Date(R.Ride_Date), 
   R.Num_Riders
FROM 
(
  SELECT
    Ride_Date,
    sum(Num_Riders) as Num_Riders,
    ROW_NUMBER() OVER (ORDER BY Ride_Date  ASC) AS rn_up,
    ROW_NUMBER() OVER (ORDER BY Ride_Date DESC) AS rn_down
  FROM Ridership
  inner join Stations as s  on s.Station_ID = Ridership.Station_ID
  Where strftime('%Y', Ride_Date) = ? AND s.Station_Name like ?
  group by Ride_Date
) AS R
WHERE R.rn_up <= 5 OR R.rn_down <= 5
ORDER BY R.Ride_Date ASC;"""

    SqlforGraph = """Select Date(Ride_Date) , sum(Num_Riders) from Ridership  inner join  Stations  on Stations.Station_ID = Ridership.Station_ID Where strftime('%Y', Ride_Date) = ? AND Station_Name like ? Group By  Ride_Date"""

    dbcusorStation.execute(sqlforGenerictStation, [firstStationName])
    fetchStation = dbcusorStation.fetchall()

    dbcusorStationNameByDate.execute(sqlforMainQueryStationOne,
                                     [year, firstStationName])
    fetchFirstStation = dbcusorStationNameByDate.fetchall()

    dbcusorStation.execute(sqlforGenerictStation, [secondStationName])
    fetchStation2 = dbcusorStation.fetchall()

    dbcusorStationNameByDate.execute(sqlforMainQueryStationOne,
                                     [year, secondStationName])
    fetchFirstStation2 = dbcusorStationNameByDate.fetchall()

    dbcusorStationNameByDate.execute(SqlforGraph, [year, firstStationName])
    fetchForPlot1 = dbcusorStationNameByDate.fetchall()
    dbcusorStationNameByDate.execute(SqlforGraph, [year, secondStationName])
    fetchForPlot2 = dbcusorStationNameByDate.fetchall()

    for row in fetchStation:
        print(" Station 1: ", row[0], row[1])
        legendForFirstStation = row[1]

    for row in fetchFirstStation:
        print(row[0], row[1])

    for row in fetchStation2:
        print("Station 2: ", row[0], row[1])
        legendForSecondStation = row[1]

    for row in fetchFirstStation2:
        print(row[0], row[1])

    plotInput = input("Plot? (y/n)")
    print();
    if (plotInput == 'y'):
        x1 = []
        y1 = []
        y2 = []
        day = 1
        plt.clf()
        # this function clear any previous plot

        for row in fetchForPlot1:
            x1.append(day)
            y1.append(row[1])
            day = day + 1

        for row in fetchForPlot2:
            y2.append(row[1])

        plt.xlabel("day")
        plt.ylabel("number of riders")
        plt.title("riders each day of " + year)

        plt.ion(
        )  # this function works in  a way that the  terminal does not hang after plot
        plt.plot(x1, y1, label=legendForFirstStation)
        plt.plot(x1, y2, label=legendForSecondStation)
        plt.legend(loc="upper right")
        plt.show()


def commandNineFunction(dbConn, StationName):
    dbcusorStation = dbConn.cursor()
    SqlforStationName = """Select  distinct(Station_Name), Latitude, 
       Longitude from Stations
       Inner Join Stops on Stations.Station_ID =  Stops.Station_ID
       Inner join  StopDetails on  StopDetails.Stop_ID = Stops.Stop_ID
       Inner join Lines on StopDetails.Line_ID = Lines.Line_ID
       Where  Color = ?
       order by Station_Name ASC"""

    dbcusorStation.execute(SqlforStationName, [StationName])
    fetchStation = dbcusorStation.fetchall()

    if (len(fetchStation) == 0):
        print("**No such line...")
        return

    for row in fetchStation:
        print(row[0], ": ", "(" + str(row[1]) + ",", str(row[2]) + ")")

    plotInput = input("plot? (y/n)")
    print();
    if (plotInput == 'y'):
        x = []
        y = []
        for row in fetchStation:
            y.append(row[1])
            x.append(row[2])
        image = plt.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
        plt.imshow(image, extent=xydims)
        plt.title(StationName + " line")  # StationName here is Color
        # neeed To change the variable name  StationName = color
        plt.ion()
        plt.plot(x, y, "o", c=StationName)

        for row in fetchStation:
            plt.annotate(row[0], (row[2], row[1]))
        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])
        plt.show()


##################################################################
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
print_stats(dbConn)  # calling the generic stats function
print()

# This wil
while (True):
    GenericInputVal = input("Please enter a command (1-9, x to exit):")

    if (GenericInputVal == 'x'):
        break

    try:
        if (int(GenericInputVal) > 0 and int(GenericInputVal) < 10):
            if (int(GenericInputVal) == 1):
                print()
                commandOneInput = input(
                    "Enter partial station name (wildcards _ and %):")
                station_name_from_user(dbConn, commandOneInput)

            if (int(GenericInputVal) == 2):
                ridership_at_each_station(dbConn)

            if (int(GenericInputVal) == 3):
                top_ten_busiest_stations(dbConn)

            if (int(GenericInputVal) == 4):
                least_busy_stations(dbConn)

            if (int(GenericInputVal) == 5):
                print()
                commandFiveInput = input(
                    "Enter a line color (e.g. Red or Yellow): ")
                if (commandFiveInput.lower() == "purple-express"):
                    commandFiveInput = "Purple-Express"
                    information_about_stations(dbConn, commandFiveInput)
                else:
                    inputFormatFive = commandFiveInput[1:].lower()
                    inputFormatFive2 = commandFiveInput[0].upper()
                    completeFormatSearchFive = inputFormatFive2 + inputFormatFive
                    information_about_stations(dbConn, completeFormatSearchFive)

            if (int(GenericInputVal) == 6):
                ridership_base_on_month(dbConn)

            if (int(GenericInputVal) == 7):
                commandSevenFunction(dbConn)

            if (int(GenericInputVal) == 8):
                print();
                commandInputYear = (input("Year to compare against?"))
                print();
                commandStationNameInput = input(
                    "Enter station 1 (wildcards _ and %):")
                
                if (CheckforNumberOfStation(dbConn,
                                            commandStationNameInput) == True): 
                    print();
                    commandStationNameInput2 = input(
                        "Enter station 2 (wildcards _ and %):")                      
                                              
                    if (CheckforNumberOfStation(
                            dbConn, commandStationNameInput2) == True):
                        CommandEightFunction(dbConn, commandInputYear,
                                             commandStationNameInput,
                                             commandStationNameInput2)

            if (int(GenericInputVal) == 9):
                print();
                commandInputStation = (
                    input("Enter a line color (e.g. Red or Yellow): "))
                
              
              

                # inputFormat = commandInputStation[1:].lower()
                # inputFormat2 = commandInputStation[0].upper()
                # completeFormatSearch = inputFormat2 + inputFormat
                # 
                if (commandInputStation.lower() == "purple-express"):
                 commandInputStation = "Purple-Express"
                 commandNineFunction(dbConn, commandInputStation)
                else:
                  inputFormat = commandInputStation[1:].lower()
                  inputFormat2 = commandInputStation[0].upper()
                  completeFormatSearch = inputFormat2 + inputFormat
                  commandNineFunction(dbConn,completeFormatSearch);
                    

              

                
        else:
            print(" **Error, unknown command, try again...")

    except:
        print(" **Error, unknown command, try again...")

#
# done
#
