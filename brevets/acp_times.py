"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

CLOSE = [(1000,11.428),(600,15),(400,15),(200,15),(0,15)]
OPEN = [(1000,28),(600,30),(400,32),(200,34),(0,34)]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    i=0
    total_time = 0

    for i in range(len(OPEN)):
	    if control_dist_km >= OPEN[i][0]:
	        km = control_dist_km - OPEN[i][0] # find distance inbetween
	        time = km / OPEN[i-1][1] # use distance to calculate time
	        total_time += time # add to running total
	        control_dist_km -= km # update total distance so far	      
	   	
	# converts time decimal into correctly formatted time (hours + minutes)
    brevet_start_time = arrow.get(brevet_start_time)
    hours = int(total_time) 
    minutes = round(60*(total_time-hours))
    opening_time = brevet_start_time.shift(hours=hours,minutes=minutes) # arrow object
	
    return opening_time.isoformat()
    


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    i=0
    total_time = 0

    for i in range(len(CLOSE)):
	    if control_dist_km >= CLOSE[i][0]:
	        km = control_dist_km - CLOSE[i][0] # find distance inbetween
	        time = km / CLOSE[i-1][1] # use distance to calculate time
	        total_time += time # add to running total
	        control_dist_km -= km # update total distance so far
	
    # converts time decimal into correctly formatted time (hours + minutes)
    brevet_start_time = arrow.get(brevet_start_time)
    hours = int(total_time)
    minutes = round(60*(total_time-hours))
    #print("hours are " + str(hours))
    #print("minutes are " + str(minutes))
    closing_time = brevet_start_time.shift(hours=hours,minutes=minutes)

    #DATE = arrow.Arrow(2013,5,5)
    #DATE = DATE.shift(hours=48,minutes=45)
    #DATE = DATE.shift(hours=40)
    
    #print("My time is " + closing_time.isoformat())
    #print("expected is " + DATE.isoformat())
    #print(closing_time.isoformat()==DATE.isoformat())
	
    return closing_time.isoformat()

#close_time(1000,700,'2013-05-05T00:00:00')
#close_time(600,600,'2013-05-05T00:00:00')
