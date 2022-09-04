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
    dbCursor = dbConn.cursor();
    dbCursorStop = dbConn.cursor();
    dbCursorTotalRide = dbConn.cursor();
    dbCursorDateRange = dbConn.cursor();
    dbCursorTotalRidership = dbConn.cursor();
    dbCursorWeekdayRider = dbConn.cursor();
    dbCursorSaturdayRider = dbConn.cursor();
    dbCursorSunOrHoliRider = dbConn.cursor(); #db cursor for sunday or holiday

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
    dbCursorSaturdayRider.execute(SqlSaturdayRidership);
    dbCursorSunOrHoliRider.execute(SqlSundayOrHoliRidership);

  #############################################

    ####Fetching############
    fetchStation = dbCursor.fetchone();
    fetchStops = dbCursorStop.fetchone();
    fetchTotalRide= dbCursorTotalRide.fetchone();
    fetchDateRange= dbCursorDateRange.fetchall();
    fetchTotalRidership = dbCursorTotalRidership.fetchone();
    fetchWeekdayRider = dbCursorWeekdayRider.fetchone();
    fetchSaturdayRider= dbCursorSaturdayRider.fetchone();
    fetchSunHoliRider = dbCursorSunOrHoliRider.fetchone();
   #Fetching #############################################
    
  
    #row5 = dbT.fetchall()
    print("  # of stations:", f"{ fetchStation[0]:,}")
    print("  # of stops:", f"{fetchStops[0]:,}")
    print("  # of stops:", f"{ fetchTotalRide[0]:,}")

    for row in fetchDateRange:
       print("  date range: ", row[0], "-", row[1])
    
    print("  Total ridership:", f"{fetchTotalRidership[0]:,}")

    weekdayRiderPercentage= ((fetchWeekdayRider[0]/fetchTotalRidership[0]) * 100)
    formatWeekdayRiderPercentage = "{:.2f}".format(weekdayRiderPercentage)

    saturdayRiderPercantage = (fetchSaturdayRider[0] / fetchTotalRidership[0]) * 100;
    formatSaturdayRiderPercantage = "{:.2f}".format(saturdayRiderPercantage);
    sunOrHolidayRiderPercentage = (fetchSunHoliRider[0] / fetchTotalRidership[0]) * 100;
    formatSunOrHolidayRiderPercantage= "{:.2f}".format(sunOrHolidayRiderPercentage);
    print("  Weekly ridership:", f"{fetchWeekdayRider[0]:,}", "("+formatWeekdayRiderPercentage+ "%)")
    print("  Saturday ridership:", f"{ fetchSaturdayRider[0]:,}", "("+formatSaturdayRiderPercantage+ "%)")
  
    print("  Sunday/holiday ridership:", f"{ fetchSunHoliRider[0]:,}", "("+formatSunOrHolidayRiderPercantage+ "%)")

  


# This function   retrive Station ID and Station_Name
# from the Station Table
#  Its accept the wildcard user input from the  user and retrive the information 
  
def commandOneFunction(dbConn, value):
  dbCursor = dbConn.cursor();
  sqlUserStations = """Select Station_ID, Station_Name from Stations Where  Station_Name like ? """
# the question mark here will be replace by the value during SQL search query when its executed
  
  dbCursor.execute(sqlUserStations, [value])
  fetchStation = dbCursor.fetchall();

  if(len(fetchStation) == 0):
    print("**No stations found...");

  for row in fetchStation:
    print(row[0], ":", row[1])

    
def calculateTotalRider(dbConn):
  dbCusorForTotalRider= dbConn.cursor();
  SqlForTotalRider = """ select Sum(Num_Riders) from Ridership;"""
  dbCusorForTotalRider.execute(SqlForTotalRider);
  fetchdbCusorForTotalRider = dbCusorForTotalRider.fetchone();
  return fetchdbCusorForTotalRider[0];
  


def commandTwoFunction(dbConn):
   dbCusorForStationAndNumber= dbConn.cursor();

   SqlForStationAndNumber = """Select Station_Name, 
   sum(Num_Riders) as NumberOfRider from Ridership 
   inner join Stations  on Stations.Station_ID = Ridership.Station_ID 
   group by Station_Name 
   order by Station_Name asc"""
  
   dbCusorForStationAndNumber.execute(SqlForStationAndNumber); # Execution of the  Sql 
   fetchdbCusorForStationAndNumber = dbCusorForStationAndNumber.fetchall();
   totalsumOfRider = calculateTotalRider(dbConn);  # this function  returns the sum of all  the riders 
  
  #printing to the console   
   for row in fetchdbCusorForStationAndNumber:
     percantageofRider =  (row[1] / totalsumOfRider) * 100; # multiplication of 100 here just to make it percentage
     print(row[0],  ":", f"{row[1]:,}", f"({percantageofRider:.2f}%)");  # this is just the formatted output  as following 
     #  Station_Name, Total rider, and   percentage of the rider out of total 



def commandThereeFunction(dbConn):
  dbCursorMostBusiestStation =  dbConn.cursor();
  sqlForMostBusiestStation = """Select Station_Name,  sum(Num_Riders) as NumberOfRider from Ridership 
         inner join Stations  on Stations.Station_ID = Ridership.Station_ID
         group by Station_Name
         order by NumberOfRider  Desc
         limit 10; """

  dbCursorMostBusiestStation.execute(sqlForMostBusiestStation);
  fetchMostBusiestStation = dbCursorMostBusiestStation.fetchall();
  totalsumOfRider = calculateTotalRider(dbConn);

  for row in  fetchMostBusiestStation:
    percantageofBusy =  (row[1] / totalsumOfRider) * 100;
    print(row[0], ":", f"{row[1]:,}", f"({ percantageofBusy:.2f}%)")




def CommandFourFunction(dbConn): 
  dbCursorLeastBusyStation =  dbConn.cursor();
  sqlForLeastBusiestStation = """Select Station_Name,  sum(Num_Riders) as NumberOfRider from Ridership 
          inner join Stations  on Stations.Station_ID = Ridership.Station_ID
          group by Station_Name
          order by NumberOfRider  asc
          limit 10;"""
  dbCursorLeastBusyStation.execute(sqlForLeastBusiestStation);
  fetchLeastBusiestStation = dbCursorLeastBusyStation.fetchall();
  totalsumOfRider = calculateTotalRider(dbConn);
  
  for row in fetchLeastBusiestStation :
    percantageofBusy =  (row[1] / totalsumOfRider) * 100;
    print(row[0], ":", f"{row[1]:,}", f"({ percantageofBusy:.2f}%)")

    
    

  



  
  
  
  
    
    
    
     

  

   
  
  
  
    

    


     
    

   

  

  

  
   
  





  

  
  


    
    

  

  





  
##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
print_stats(dbConn)  # calling the generic stats function 
print(); 

# This wil 
while(True):
  GenericInputVal = input("Please enter a command (1-9, x to exit):")

  if(GenericInputVal== 'x'):
    break;


  if(int(GenericInputVal) > 0 and int(GenericInputVal) < 10):
    if(int(GenericInputVal) == 1):
      commandOneInput= input("Enter partial station name (wildcards _ and %):")
      commandOneFunction(dbConn,commandOneInput)

    if(int(GenericInputVal) == 2):
      commandTwoFunction(dbConn);
      
    if(int(GenericInputVal) == 3):
      commandThereeFunction(dbConn);

    if(int(GenericInputVal) == 4):
      CommandFourFunction(dbConn);
      
    
      
  else:
    print("**Error, unknown command, try again...");

    


    
   

  
   
  






 



#
# done
#