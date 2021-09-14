Protesters and Police Team B07

We would like to simulate the behaviour of protesters and police with a multi-agent based model to investigate the interactions between these groups and how these interactions escalate to violent behaviour. We plan to vary the levels of aggressiveness of the protesters, the ratio of police agents versus protesters and potentially also the aggressiveness of police officers. We think this could lead to interesting insights in how these group dynamics interact with one another.  We will use data on how police are deployed, as well as information on group sizes and group dynamics to hopefully create realistic simulations that can offer new perspectives on the behaviour of police and protesters hopefully shed some light on how to decrease the chance of violence between these groups. We will be programming exclusively in Python and are planning on using the mesa library to visualise our simulation.

References: 
- J. M. Epstein. “Modeling civil violence: An agent-based computational approach”. In: Proceedings of the National Academy of Sciences 99. Supplement 3 (2002), pp. 7243–7250. DOI: 10.1073/pnas.092080199. 
- C. Warner and J. D. McCarthy. "Whatever can go wrong will: situational complexity and public order policing". In: Policing and Society, 24:5 (2014), pp. 566-587, DOI: 10.1080/10439463.2013.784308


---

- What is your chosen problem or challenge?
- What is the current state of the art?
- What is your new idea?


--- 
Simulate :
    behavior with police and protesters -> become violent. 

params :
    aggression (protesters, police), ratio

Objective :
    - factors to escalation
    - simulation, perspectives , different 
    - for what the police should do

Epstein:
- Variants of civil violence : central seeks to supress groups. centeral supress two groups 
- Hardship and legitimacy
- Cop vision 
- density cop, genocide etc

warner:
- mainly on finding the cause of protests -> event complexity
- configs of pretest events
- elite, political,
- non confrontational police
- preserve public order
- diversity, event size, strategy
- Arrests, force

Whats new with our project
- Different motive
- Protesters stop : factors (achived success, all caught, too hurt etc)
- Initial seed : (groups where police/ protesters started together)
- Parameters for sticking together
- Who first started the protest
- Aggression -> Both sides
- How we end