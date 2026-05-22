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

BREVET_SPEED_TABLE = [
    (0, 200, 34, 15),
    (200, 400, 32, 15),
    (400, 600, 30, 15),
    (600, 1000, 28, 11.428),
    (1000, 1300, 26, 13.333)
]


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
   if control_dist_km < 0 or brevet_dist_km < 0:
       return arrow.get(brevet_start_time).isoformat()

   location = min(control_dist_km, brevet_dist_km)
   total_hours = 0.0

   for start, end, max_speed, min_speed in BREVET_SPEED_TABLE:
      if location > start:
         section = min(location, end) - start
         total_hours += section / max_speed
      else:
            break
   
   total_minutes = round(total_hours * 60)
   start_time = arrow.get(brevet_start_time)
   return start_time.shift(minutes=total_minutes).isoformat()


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
   if control_dist_km < 0 or brevet_dist_km < 0:
      return arrow.get(brevet_start_time).isoformat()

   location = abs(control_dist_km)
   start_time = arrow.get(brevet_start_time)

   # for closing at 0 km is 1 hour after start
   if location == 0:
       return start_time.shift(hours=1).isoformat()
   
   # for special finish times for certain brevet distance
   FINISH_TIMES = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}
   if location >= brevet_dist_km:
       hours = FINISH_TIMES.get(brevet_dist_km, 0)
       return start_time.shift(hours=hours).isoformat()
   
   # for when >60km a special calculation is needed
   if location < 60:
      total_minutes = round((1 + (location / 20)) * 60)
      return start_time.shift(minutes=total_minutes).isoformat()
   
   total_hours = 0.0
   for start, end, max_speed, min_speed in BREVET_SPEED_TABLE:
      if location > start:
           section = min(location, end) - start
           total_hours += section / min_speed
      else: 
         break
   
   total_minutes = round(total_hours * 60)
   return start_time.shift(minutes=total_minutes).isoformat()