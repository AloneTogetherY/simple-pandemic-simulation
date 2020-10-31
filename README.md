# A Simple Pandemic Simulation

Run ```python simulation.py``` with the default arguments or change them.

Possible arguments:<br />
  ```-simulation_steps``` Define the number of simulation steps<br />
   ```-no_of_points```  Define the number of points / population<br />
   ```-no_of_initial_infected```  Define the number of initially infected<br />
   ```-distance_tolerance``` Define the distance tolerance as a decimal<br />
   ```-death_rate``` Define the death rate as a percentage from 0.01 to 0.99<br />
   ```-immunity_rate``` Define the immunity rate as a percentage from 0.01 to 0.99<br />
   ```-min_time_to_recover``` Define the minimum time to recover in ms<br />
   ```-max_time_to_recover``` Define the maximum time to recover in ms<br />
   ```-min_time_to_death``` Define the minimum time to die in ms<br />
   ```-max_time_to_death``` Define the maximum time to die in ms<br />
   ```-interval``` Define the the delay between frames in ms<br />
   ```-save_file``` (True/False) Save simulation as gif <br /><br />
## Assumptions:<br />
* Whether a person was sick or not can be deduced from their recovered or died status.
* Non-infected points that near other infected points within the given distance tolerance are immediately infected.
* Which infected persons recover or die is randomly selected.
* Persons that have already been infected and recovered cannot be infected again.
## Example:<br />
* Coming
## ToDo:<br />
* Introduce an export function for the simulation data into json / csv. <br />

