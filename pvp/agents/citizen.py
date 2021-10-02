import math
import random
from operator import pos

from mesa import Agent


class Citizen(Agent):
    """
    A member of the general population, may or may not be in active rebellion.
    Summary of rule: If grievance - risk > threshold, rebel.

    Attributes:
        unique_id: unique int
        x, y: Grid coordinates
        hardship: Agent's 'perceived hardship (i.e., physical or economic
            privation).' Exogenous, drawn from U(0,1).
        regime_legitimacy: Agent's perception of regime legitimacy, equal
            across agents.  Exogenous.
        risk_aversion: Exogenous, drawn from U(0,1).
        threshold: if (grievance - (risk_aversion * arrest_probability)) >
            threshold, go/remain Active
        vision: number of cells in each direction (N, S, E and W) that agent
            can inspect
        condition: Can be "Quiescent" or "Active;" deterministic function of
            greivance, perceived risk, and
        grievance: deterministic function of hardship and regime_legitimacy;
            how aggrieved is agent at the regime?
        arrest_probability: agent's assessment of arrest probability, given
            rebellion

    """

    def __init__(
            self,
            unique_id,
            model,
            pos,
            hardship,
            regime_legitimacy,
            risk_aversion,
            threshold,
            vision,
            aggression,
            direction_bias,
    ):
        """
        Create a new Citizen.
        Args:
            unique_id: unique int
            x, y: Grid coordinates
            hardship: Agent's 'perceived hardship (i.e., physical or economic
                privation).' Exogenous, drawn from U(0,1).
            regime_legitimacy: Agent's perception of regime legitimacy, equal
                across agents.  Exogenous.
            risk_aversion: Exogenous, drawn from U(0,1).
            aggression : Exogenous, drawn from U(0,1).
            threshold: if (grievance - (risk_aversion * arrest_probability)) >
                threshold, go/remain Active
            vision: number of cells in each direction (N, S, E and W) that
                agent can inspect. Exogenous.
            model: model instance
        """
        super().__init__(unique_id, model)
        self.breed = "citizen"
        self.pos = pos
        self.hardship = hardship
        self.regime_legitimacy = regime_legitimacy
        self.risk_aversion = risk_aversion
        self.threshold = threshold
        self.direction_bias = direction_bias
        self.condition = "Quiescent"
        self.vision = vision
        self.jail_sentence = 0
        self.grievance = self.hardship * (1 - self.regime_legitimacy)
        self.arrest_probability = None
        self.aggression = aggression
        # TODO: include susceptibility to aggression into when they turn active
        self.susceptibility_to_aggression = self.random.random()

    def step(self):
        """
        Decide whether to activate, then move if applicable.
        """
        if self.jail_sentence:
            self.jail_sentence -= 1
            return  # no other changes or movements if agent is in jail.

        # TODO: random variable to create deviant behaviour
        """if self.jail_sentence:
            # self.jail_sentence -= 1
            self.model.arrested_agents.append(self)
            return  # no other changes or movements if agent is in jail.
        """

        # ADDED THIS LUKE:
        if self.risk_aversion < 0.0000000000000000000001 and self.condition != "Active":
            self.condition = "Deviant" ##

        if self.aggression > 0.3:  # TODO
            self.risk_aversion = self.risk_aversion / 2

        self.update_neighbors()
        self.update_estimated_arrest_probability()

        net_risk = self.risk_aversion * self.arrest_probability
        if (
                self.condition == "Quiescent"
                and abs(net_risk - self.arrest_probability) > self.threshold
        ):
            self.condition = "Active"
        elif (
                self.condition == "Active"
                and abs(net_risk - self.arrest_probability) <= self.threshold
        ):
            self.condition = "Quiescent"

        '''swap = False
        for agent in self.neighbors:
            if agent.breed == "citizen" and agent.jail_sentence > 0:
                swap = True
                break

        if self.susceptibility_to_aggression > 0.8 and swap:
            self.condition = "Active"'''

        if self.model.movement and self.empty_neighbors:
            if self.direction_bias != "Random":

                if len(self.empty_neighbors) > 0:
                    move = self.choose_direction(self.empty_neighbors)
                    if move != None:
                        print(self.pos, move, self.unique_id)
                        self.model.grid.move_agent(self, move)
            else:
                new_pos = self.random.choice(self.empty_neighbors)
                self.model.grid.move_agent(self, new_pos)

    def calc_direction(self, new_pos):
        if new_pos[1] < self.pos[1] and new_pos[0] == self.pos[0]:
            return "up"
        elif new_pos[1] > self.pos[1] and new_pos[0] == self.pos[0]:
            return "down"
        elif new_pos[1] == self.pos[1] and new_pos[0] > self.pos[0]:
            return "right"
        elif new_pos[1] == self.pos[1] and new_pos[0] < self.pos[0]:
            return "left"
        else:
            return None

    def choose_direction(self, possible_moves):
        choices = []
        if self.direction_bias == "Clockwise" or self.direction_bias == "Anti-clockwise":
            x_left = (self.model.width / 2) - 5
            x_right = self.model.width - x_left
            y_up = (self.model.height / 2) - 5
            y_down = self.model.height - y_up
            for x in possible_moves:
                direction = self.calc_direction(x)
                if self.pos[0] < x_left and self.pos[1] > y_up:
                    if self.direction_bias == "Anti-clockwise" and direction == "up":
                        choices.append(x)
                    elif self.direction_bias == "Clockwise" and direction == "down":
                        choices.append(x)
                if self.pos[0] < x_right and self.pos[1] < y_up:
                    if self.direction_bias == "Anti-clockwise" and direction == "right":
                        choices.append(x)
                    elif self.direction_bias == "Clockwise" and direction == "left":
                        choices.append(x)
                if self.pos[0] > x_right and self.pos[1] < y_down:
                    if self.direction_bias == "Anti-clockwise" and direction == "down":
                        choices.append(x)
                    elif self.direction_bias == "Clockwise" and direction == "up":
                        choices.append(x)
                if self.pos[0] > x_left and self.pos[1] > y_down:
                    if self.direction_bias == "Anti-clockwise" and direction == "left":
                        choices.append(x)
                    elif self.direction_bias == "Clockwise" and direction == "right":
                        choices.append(x)
        else:
            choices = [x for x in possible_moves if self.calc_direction(x) == self.direction_bias]
        if len(choices) != 0:
            return random.choice(choices)
        else:
            return None  #self.random.choice(possible_moves)

    def update_neighbors(self):
        """
        Look around and see who my neighbors are
        """
        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=False, radius=1
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]

    def update_estimated_arrest_probability(self):
        """
        Based on the ratio of cops to actives in my neighborhood, estimate the
        p(Arrest | I go active).

        """
        cops_in_vision = len([c for c in self.neighbors if c.breed == "cop"])
        actives_in_vision = 1.0  # citizen counts herself
        for c in self.neighbors:
            if (
                    c.breed == "citizen"
                    and c.condition == "Active"
                    and c.jail_sentence == 0
            ):
                actives_in_vision += 1
        self.arrest_probability = 1 - math.exp(
            -1 * self.model.arrest_prob_constant * (cops_in_vision / actives_in_vision)
        )
