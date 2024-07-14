

column|values|description
-|-|:------
ID|string|unique identifier for journey
eva_nr|int|unique identifier for train stops
category|1-7|    1 to 2: primary junction<br>3: main stations from big and medium sized cities <br> 4: metropolitarian areas (high regional traffic)<br>5 to 6: small train stations<br>7: small simple train stops
path|string|list of all previous stops before the current
station|string|station name
state,city,zip|string,string,int|adress
long,lat|float|geolocation
arrival_plan, departure_plan|datetime|timestamp planned arrival and departure
arrival_change, departure_change|datetime|timestamp changed arrival and departure
arrival/departure_delay_m|int|resulting delay in minutes
arrival/departure_delay_check|string|categorical identifier if a delay is present (>6 min)
info|string|info about the change

