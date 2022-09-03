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

  ######## This portion is designated for SQL Quesries ### 
    sqlNumberofStations = "Select count(*) From Stations;"
    SqlNumberofStops = "Select count(Stop_ID) from Stops;"
    SqlNumberofTotalRide = "Select count(Num_Riders) from Ridership;"
    SqlDateRange = " Select Date(Min(Ride_Date)) as FromDate, Date(max(Ride_Date)) ToDate from Ridership;"
    SqlTotalRidership = "Select sum(num_Riders) from Ridership;"

     


  


  
  #######  --- #############################################

  
    print("General stats:")
    dbCursor.execute(sqlNumberofStations)
    dbCursorStop.execute(SqlNumberofStops)
    dbCursorTotalRide.execute(SqlNumberofTotalRide)
    dbCursorDateRange.execute(SqlDateRange)
    dbCursorTotalRidership.execute(SqlTotalRidership)
    fetchStation = dbCursor.fetchone();
    fetchStops = dbCursorStop.fetchone();
    fetchTotalRide= dbCursorTotalRide.fetchone();
    fetchDateRange= dbCursorDateRange.fetchall();
    fetchTotalRidership = dbCursorTotalRidership.fetchone();
  
    #row5 = dbT.fetchall()
    print("  # of stations:", f"{ fetchStation[0]:,}")
    print("  # of stops:", f"{fetchStops[0]:,}")
    print("  # of stops:", f"{ fetchTotalRide[0]:,}")

    for row in fetchDateRange:
       print("  date range: ", row[0], "-", row[1])
    
    print("  Total ridership:", f"{fetchTotalRidership[0]:,}")


      


      

  

  
  

  
   

  
    


##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

#
# done
#