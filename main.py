#Name: Mosrour Tafadar
#  CS 341 Fall 2022
# University of Illinois

import sqlite3
import matplotlib.pyplot as plt


##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
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
    SqlWeekdayRidership = "Select sum(Num_Riders) from Ridership Where Type_of_day = \"W\";"
    SqlSaturdayRidership = "Select sum(Num_Riders) from Ridership Where Type_of_day = \"A\";"
    SqlSundayOrHoliRidership = "Select sum(Num_Riders) from Ridership Where Type_of_day = \"U\";"

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

    #row5 = dbT.fetchall()
    print("  # of stations:", f"{ fetchStation[0]:,}")
    print("  # of stops:", f"{fetchStops[0]:,}")
    print("  # of  ride entries:", f"{ fetchTotalRide[0]:,}")

    for row in fetchDateRange:
        print("  date range: ", row[0], "-", row[1])

    print("  Total ridership:", f"{fetchTotalRidership[0]:,}")

    weekdayRiderPercentage = ((fetchWeekdayRider[0] / fetchTotalRidership[0]) *
                              100)
    formatWeekdayRiderPercentage = "{:.2f}".format(weekdayRiderPercentage)

    saturdayRiderPercantage = (fetchSaturdayRider[0] /
                               fetchTotalRidership[0]) * 100
    formatSaturdayRiderPercantage = "{:.2f}".format(saturdayRiderPercantage)
    sunOrHolidayRiderPercentage = (fetchSunHoliRider[0] /
                                   fetchTotalRidership[0]) * 100
    formatSunOrHolidayRiderPercantage = "{:.2f}".format(
        sunOrHolidayRiderPercentage)
    print("  Weekly ridership:", f"{fetchWeekdayRider[0]:,}",
          "(" + formatWeekdayRiderPercentage + "%)")
    print("  Saturday ridership:", f"{ fetchSaturdayRider[0]:,}",
          "(" + formatSaturdayRiderPercantage + "%)")

    print("  Sunday/holiday ridership:", f"{ fetchSunHoliRider[0]:,}",
          "(" + formatSunOrHolidayRiderPercantage + "%)")


# This function   retrive Station ID and Station_Name
# from the Station Table
#  Its accept the wildcard user input from the  user and retrive the information


def commandOneFunction(dbConn, value):
    dbCursor = dbConn.cursor()
    sqlUserStations = """Select Station_ID, Station_Name from Stations Where  Station_Name like ? """
    # the question mark here will be replace by the value during SQL search query when its executed

    dbCursor.execute(sqlUserStations, [value])
    fetchStation = dbCursor.fetchall()

    if (len(fetchStation) == 0):
        print("**No stations found...")

    for row in fetchStation:
        print(row[0], ":", row[1])


def calculateTotalRider(dbConn):
    dbCusorForTotalRider = dbConn.cursor()
    SqlForTotalRider = """ select Sum(Num_Riders) from Ridership;"""
    dbCusorForTotalRider.execute(SqlForTotalRider)
    fetchdbCusorForTotalRider = dbCusorForTotalRider.fetchone()
    return fetchdbCusorForTotalRider[0]


def commandTwoFunction(dbConn):
    dbCusorForStationAndNumber = dbConn.cursor()

    SqlForStationAndNumber = """Select Station_Name, 
   sum(Num_Riders) as NumberOfRider from Ridership 
   inner join Stations  on Stations.Station_ID = Ridership.Station_ID 
   group by Station_Name 
   order by Station_Name asc"""

    dbCusorForStationAndNumber.execute(SqlForStationAndNumber)
    # Execution of the  Sql
    fetchdbCusorForStationAndNumber = dbCusorForStationAndNumber.fetchall()
    totalsumOfRider = calculateTotalRider(dbConn)
    # this function  returns the sum of all  the riders

    #printing to the console
    for row in fetchdbCusorForStationAndNumber:
        percantageofRider = (row[1] / totalsumOfRider) * 100
        # multiplication of 100 here just to make it percentage
        print(row[0], ":", f"{row[1]:,}", f"({percantageofRider:.2f}%)")
        # this is just the formatted output  as following
        #  Station_Name, Total rider, and   percentage of the rider out of total


def commandThereeFunction(dbConn):
    dbCursorMostBusiestStation = dbConn.cursor()
    sqlForMostBusiestStation = """Select Station_Name,  sum(Num_Riders) as NumberOfRider from Ridership 
         inner join Stations  on Stations.Station_ID = Ridership.Station_ID
         group by Station_Name
         order by NumberOfRider  Desc
         limit 10; """

    dbCursorMostBusiestStation.execute(sqlForMostBusiestStation)
    fetchMostBusiestStation = dbCursorMostBusiestStation.fetchall()
    totalsumOfRider = calculateTotalRider(dbConn)

    for row in fetchMostBusiestStation:
        percantageofBusy = (row[1] / totalsumOfRider) * 100
        print(row[0], ":", f"{row[1]:,}", f"({ percantageofBusy:.2f}%)")


def CommandFourFunction(dbConn):
    dbCursorLeastBusyStation = dbConn.cursor()
    sqlForLeastBusiestStation = """Select Station_Name,  sum(Num_Riders) as NumberOfRider from Ridership 
          inner join Stations  on Stations.Station_ID = Ridership.Station_ID
          group by Station_Name
          order by NumberOfRider  asc
          limit 10;"""
    dbCursorLeastBusyStation.execute(sqlForLeastBusiestStation)
    fetchLeastBusiestStation = dbCursorLeastBusyStation.fetchall()
    totalsumOfRider = calculateTotalRider(dbConn)

    for row in fetchLeastBusiestStation:
        percantageofBusy = (row[1] / totalsumOfRider) * 100
        print(row[0], ":", f"{row[1]:,}", f"({ percantageofBusy:.2f}%)")


def commandFiveFunction(dbConn, value):
    dbCursorColorBelongStationName = dbConn.cursor()
    SqlForColorBelongStationName = """Select Stop_Name, Direction, ADA from Stops
      inner join StopDetails   on StopDetails.Stop_ID  = Stops.Stop_ID
      inner join Lines On Lines.Line_ID = StopDetails.Line_ID
      where color = ? 
      order by Stop_Name ASC;"""

    dbCursorColorBelongStationName.execute(SqlForColorBelongStationName,
                                           [value])
    fetchColorBelongStationName = dbCursorColorBelongStationName.fetchall()

    if (len(fetchColorBelongStationName) == 0):
        print("**No such line...")

    for row in fetchColorBelongStationName:
        if (row[2] == 1):
            AccessibleValue = "Yes"

        else:
            AccessibleValue = "No"
        print(row[0], ":", "direction = ", row[1], "(accessible?",
              AccessibleValue + ")")


def commandSixFunction(dbConn):
    dbcusorRiderBasedOnMonth = dbConn.cursor()
    SqlForRiderBasedOnMonth = """Select  strftime('%m', Ride_Date) as Month, sum(Num_Riders)  
     from  Ridership 
     group By Month;"""
    dbcusorRiderBasedOnMonth.execute(SqlForRiderBasedOnMonth)
    fetchRiderBasedOnMonth = dbcusorRiderBasedOnMonth.fetchall()

    print("** ridership by month **")

    for row in fetchRiderBasedOnMonth:
        print(row[0], ":", f"{row[1]:,}")

    plotInput = input("plot: (y/n)")

    if (plotInput == 'y'):
        x= []
        y = []
        for row in fetchRiderBasedOnMonth:
          x.append(row[0]);
          y.append([row[1]])
          
        plt.xlabel("month")
        plt.ylabel("number of riders (x*10^8")
        plt.title("monthly ridership")
        plt.ion()
        plt.plot(x,y)
        plt.show()

def commandSevenFunction(dbConn):
   dbcusorRiderBasedOnYear = dbConn.cursor()
   sqlRiderBasedOnYear =  """Select  strftime('%Y', Ride_Date) as Year, sum(Num_Riders)
                from  Ridership 
                group By Year
                order by Year asc;"""

   dbcusorRiderBasedOnYear.execute(sqlRiderBasedOnYear);
   fetchRiderBasedonYear = dbcusorRiderBasedOnYear.fetchall();

   print("** ridership by year **")
   for row in fetchRiderBasedonYear:
      print(row[0], ":", f"{row[1]:,}")

   plotInput = input("plot: (y/n)")
   if (plotInput == 'y'):
        x= []
        y = []
        for row in fetchRiderBasedonYear:
          val = row[0][2:4]
          x.append(val);
          y.append([row[1]])
          
        plt.xlabel("year")
        plt.ylabel("number of riders (x*10^8")
        plt.title("yearly ridership")
        plt.ion()
        plt.plot(x,y)
        plt.show()
  
       


def  CheckforNumberOfStation(dbConn, Val):
     dbcusorRiderBasedOnMonth = dbConn.cursor(); 
     sqlforStationValue = """Select Station_Name from Stations
     Where Station_Name like ? """
     dbcusorRiderBasedOnMonth.execute(sqlforStationValue, [Val]);
     fetchStationValue = dbcusorRiderBasedOnMonth.fetchall();

     if(len(fetchStationValue) == 0 ):
       print("**No station found...");
       return False;

     if(len(fetchStationValue) > 1):
       print("**Multiple stations found...");
       return False;

     if(len(fetchStationValue) == 1):
       return True;
       
     return;


def  CommandEightFunction(dbConn, year, firstStationName, secondStationName):
  dbcusorStation = dbConn.cursor(); 
  dbcusorStationNameByDate = dbConn.cursor(); 

  
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

  SqlforGraph = """Select Date(Ride_Date) , sum(Num_Riders) from Ridership  inner join  Stations  on Stations.Station_ID = Ridership.Station_ID Where strftime('%Y', Ride_Date) = ? AND Station_Name like ? Group By  Ride_Date""";



  
  
  dbcusorStation.execute(sqlforGenerictStation, [firstStationName])
  fetchStation =  dbcusorStation.fetchall();

  dbcusorStationNameByDate.execute(sqlforMainQueryStationOne, [year, firstStationName])
  fetchFirstStation = dbcusorStationNameByDate.fetchall();

  dbcusorStation.execute(sqlforGenerictStation, [secondStationName])
  fetchStation2 = dbcusorStation.fetchall();

  dbcusorStationNameByDate.execute(sqlforMainQueryStationOne, [year,secondStationName])
  fetchFirstStation2 = dbcusorStationNameByDate.fetchall();


  dbcusorStationNameByDate.execute(SqlforGraph , [year, firstStationName])
  fetchForPlot1 = dbcusorStationNameByDate.fetchall(); 
  dbcusorStationNameByDate.execute(SqlforGraph , [year, secondStationName])
  fetchForPlot2 = dbcusorStationNameByDate.fetchall(); 

  

  



  for row in fetchStation:
     print("Station 1: ", row[0], row[1])
     legendForFirstStation = row[1];
    
  
  for row in fetchFirstStation: 
    print( row[0],  row[1])
     

  for row in fetchStation2:
    print("Station 2: ", row[0], row[1])
    legendForSecondStation = row[1];

  for row in fetchFirstStation2: 
    print( row[0],  row[1])


  
     

  plotInput = input("plot: (y/n)")
  if (plotInput == 'y'):
    x1= []
    y1 = []
    y2 = []
    day  = 1;
    plt.clf(); # this function clear any previous plot 
  
    for row in fetchForPlot1:
      x1.append(day)
      y1.append(row[1])
      day = day + 1;

    for row in fetchForPlot2:
      y2.append(row[1])

    plt.xlabel("day")
    plt.ylabel("number of riders")
    plt.title("riders each day of " + year)
    
    plt.ion() # this function works in  a way that the  terminal does not hang after plot
    plt.plot(x1,y1,  label= legendForFirstStation)
    plt.plot(x1,y2, label= legendForSecondStation)
    plt.legend(loc="upper right")
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

    if (int(GenericInputVal) > 0 and int(GenericInputVal) < 10):
        if (int(GenericInputVal) == 1):
            commandOneInput = input(
                "Enter partial station name (wildcards _ and %):")
            commandOneFunction(dbConn, commandOneInput)

        if (int(GenericInputVal) == 2):
            commandTwoFunction(dbConn)

        if (int(GenericInputVal) == 3):
            commandThereeFunction(dbConn)

        if (int(GenericInputVal) == 4):
            CommandFourFunction(dbConn)

        if (int(GenericInputVal) == 5):
            commandFiveInput = input( "Enter a line color (e.g. Red or Yellow): ")
            commandFiveFunction(dbConn, commandFiveInput)

        if (int(GenericInputVal) == 6):
            commandSixFunction(dbConn)

        if (int (GenericInputVal) == 7):
           commandSevenFunction(dbConn);

        if(int(GenericInputVal) == 8):
          commandInputYear  = (input( "Year to compare against?"));
          commandStationNameInput = input("Enter station 1 (wildcards _ and %):");
          if(CheckforNumberOfStation(dbConn, commandStationNameInput) == True):
            commandStationNameInput2 = input("Enter station (wildcards _ and %):");
            if(CheckforNumberOfStation(dbConn, commandStationNameInput2) == True):
              CommandEightFunction(dbConn, commandInputYear , commandStationNameInput,commandStationNameInput2)
              

  
    else:
       print("**Error, unknown command, try again...")

#
# done
#
