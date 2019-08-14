Almost all files have something useful:
Needs.py is the core file. It has the Need class, look at the atributes.
A need class has:

Name: name of the need  
type: physiological, social, cognitive  
weight: how strong the needs is compared to others  
value: the value, the defaultvalue is different for all needs.   
urge: difference target state and current state  
urgency: The need to satisfy the urge. Time that is left until satisfaction because - 
for example - a critical state has been reached or the situation askes for immediate satisfaction  
pleasure: is done by increasing the need value (that is satisfaction)  
pain: is done by lowering the needvalue (depletion)

Satisfaction is achieved by a consumption event (eating an apple). So this should 
incease the need.value.   

The api.py gives the opportunity to run seperate functions without the hassle. Try get_needs(). 
The first time you run this, you get the default states in a nested dict. 
With the steps and the update() you can change the states. I think right now, it does 
this randomly, as defined in simulation.py in the Step class.

Important for rest and hunger is the "decay". This is defined in common.py. Decay lowers the 
needs.value in time. Of course, if the value decreases, the demand increases. 
How this is exactly done, I'm not sure yet ( i think a sigmoidal function)

Gain: How fast the value increases
Loss: how fast the value decreases

Example: If you have a hight metabolism, it means you have a high weight, gain and loss and decay factor. 

### general remarks

An empty stomach is a depleted food need. This will lead to a pain signal. The pain increases. 

I think it is hard to use a small part of the code only, because it is so interdependant. 

The simulation is kind of weird. The values are weird (and different from the paper). The functions
for the simulation are in widget.py. 
   
The mainfile to work in is appelboer.py. 

The file that I use for experimentation is zandbak.py
