# Project 4:  Brevet time calculator with Ajax

Reimplement the RUSA ACP controle time calculator with flask and ajax.

Credits to Micheal Young.

Edited by Max Grice

DOCROOT=/brevets

## ACP controle times

That's "controle" with an 'e', because it's French, although "control"
is also accepted.  Controls are points where   
a rider must obtain proof of passage, and control[e] times are the
minimum and maximum times by which the rider must  
arrive at the location.   

The algorithm for calculating controle times is described at
https://rusa.org/octime_alg.html .  Additional background information
is in https://rusa.org/pages/rulesForRiders. 

We are essentially replacing the calculator at
https://rusa.org/octime_acp.html .  We can also use that calculator
to clarify requirements and develop test data.  

More specifically, this algorithm makes use of a table which contains minimum and maximum speeds for given control locations in km, including 200km, 400km, 600km, and 1000km. Calculating the controls opening time requires dividing the first 200km (or less if the control time is less than 200) by its corresponding maximum speed and so on until we reach the specified control time. Each speed segment is then added together to get the total time taken. The exact same procedure is used for the closing time except that we are now using the minimum speed instead. For more clarification, an example is shown below:

A an opening time for a control at 550km is 200/34 + 200/32 + 150/30 = 17H08.

After calculating both opening and closing times for a given control distance, this value is then updated accordingly in the html table of distances and times. 
