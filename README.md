# Protesters vs Cops

## Requirements
- pip install -r requirements.txt

## How to run
- python3 run.py
- This should open a browser window with the required interface and parameters.

## Documentation
- [Here](https://subhadityamukherjee.github.io/DMASB07-ProtestersVsPolice/)

## Better commits + free documentation website :)
- This will auto format all the codes and sort the imports so you don't have to, creates a documentation website etc
- If you are running Linux/Mac/WSL, while pushing to the repository run
- chmod +x pusher.sh (just once. This makes it executable)
- Next time you want to push your changes just do ./pusher.sh "commit_name"

# Informal list of features
## General Agent Properties
- Moves to an empty cell

## Agent Types
### Block
- Easy ability to place arrangements of barricades
### Cop
- Delay for x steps after arresting to simulate time 
- "Vision" : Can see and capture agents in a particular radius
- Arrests agents taking into account jail capacity, occupancy
- Arresting protesters is hard and a cop only does so if there is atleast 1 more cop in their vision

### Citizen
- Hardship :
- Legitimacy :
- Risk Aversion : Decides how much or how little of a risk to take. This influences deviants
- Direction Bias : Emulates environments where only moving in a certain direction is possible
- Conditions
  - Active : Dangerous citizens, probably will be arrested
  - Quiescent : Peaceful protesters. Have a chance of deviancy
  - Deviants : Suddenly becoming aggressive. Maybe something triggered them
- Vision : Decides how many people they look at in a radius around them before moving
- Jail sentence : How long will someone stay inactive on the field
- Arrest Probability
- Aggression 
- Susceptibility to aggression : How easy it is for a citizen to get aggressive
- Special Factors:
  - If aggression > 0.3 then risk aversion is halved
  - If risk aversion < .01 and the agent is active => Deviant
  - Decide state by the absolute value of (netrisk - arrest probability) and comparing it with a threshold

## Environment Conditions
- Directions : Agents can only move if their next position falls on the chosen direction
  - Up, Down, Left, Right
  - Clockwise, Anti clockwise
- Types of distributions
  - Random
  - Blocks in the middle
  - Wall of cops in either side
  - Block of cops in the middle
  - Street environment
  - Circular (Emulated by warping)
## Environment Params
- jail capacity
- citizen_density: approximate % of cells occupied by citizens.
- cop_density: approximate % of calles occupied by cops.
- citizen_vision: number of cells in each direction (N, S, E and W) that citizen can inspect
- cop_vision: number of cells in each direction (N, S, E and W) that cop can inspect
- legitimacy:  (L) citizens' perception of regime legitimacy, equal across all citizens
- max_jail_term: (J_max)
- active_threshold: if (grievance - (risk_aversion * arrest_probability))> threshold, citizen rebels
- arrest_prob_constant: set to ensure agents make plausible arrestprobability estimates