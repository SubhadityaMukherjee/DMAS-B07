import math
import random

from mesa import Agent


class Citizen(Agent):

    def __init__(
        self,
        unique_id,
        model,
        pos,
        risk_aversion,
        threshold,
        vision,
        aggression,
        direction_bias,
    ):

        super().__init__(unique_id, model)
        self.breed = "citizen"
        self.pos = pos
        self.risk_aversion = risk_aversion
        self.threshold = threshold
        self.direction_bias = direction_bias
        self.condition = "Quiescent"
        self.vision = vision
        self.jail_sentence = False
        self.steps_active = 0
        self.arrest_probability = None
        self.aggression = aggression

    def step(self):
        """
        Decide whether to activate, then move if applicable.
        """

        if self.risk_aversion < 0.05:
            self.condition = "Deviant"

        self.update_neighbors()
        self.update_estimated_arrest_probability()
        self.update_aggression_threshold_after_arrest()

        net_risk = self.risk_aversion * self.arrest_probability
        if (
            self.condition
            == "Quiescent"
            and abs(net_risk - self.arrest_probability) > self.threshold
        ):
            self.condition = "Active"
        elif (
            self.condition == "Active"
            and abs(net_risk - self.arrest_probability) <= self.threshold
        ):
            self.condition = "Quiescent"
        elif (
            self.condition == "Deviant"
            and abs(net_risk - self.arrest_probability) <= self.threshold
        ):
            self.condition = "Quiescent"


        if self.model.movement and self.empty_neighbors:
            if self.direction_bias != "Random":

                if len(self.empty_neighbors) > 0:
                    move = self.choose_direction(self.empty_neighbors)
                    if move is not None:
                        self.model.grid.move_agent(self, move)
            else:
                new_pos = self.random.choice(self.empty_neighbors)
                self.model.grid.move_agent(self, new_pos)

        if self.condition == "Active" or self.condition == "Deviant":
            self.steps_active += 1
        elif self.condition == "Quiescent":
            self.steps_active = 0

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
        x_left = (self.model.width / 2) - 5
        y_up = (self.model.height / 2) - 5
        x_right = self.model.width - x_left
        y_down = self.model.height - y_up

        if (
            self.direction_bias == "Clockwise"
            or self.direction_bias == "Anti-clockwise"
        ):
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
            choices = [
                x
                for x in possible_moves
                if self.calc_direction(x) == self.direction_bias
            ]
        if len(choices) != 0:
            return random.choice(choices)
        else:
            return self.random.choice(possible_moves)

    def update_neighbors(self):

        self.neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=False, radius=1
        )
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [
            c for c in self.neighborhood if self.model.grid.is_cell_empty(c)
        ]

    def update_estimated_arrest_probability(self):

        cops_in_vision = len([c for c in self.neighbors if c.breed == "cop"])
        actives_in_vision = 1.0
        for c in self.neighbors:
            if (
                c.breed == "citizen" and c.condition == "Active" and not c.jail_sentence
            ):
                actives_in_vision += 1
        self.arrest_probability = 1 - math.exp(
            -1 * self.model.arrest_prob_constant * (cops_in_vision / actives_in_vision)
        )

    def update_aggression_threshold_after_arrest(self):

        neighbors = self.model.grid.get_cell_list_contents(
            self.model.grid.get_neighborhood(self.pos, moore=False, radius=self.vision)
        )

        arrestees_in_vision = 0
        for c in neighbors:
            if (
                c.breed == "citizen" and c.condition == "Deviant" and c.jail_sentence
            ):
                arrestees_in_vision += 1
        if arrestees_in_vision > 0:
            self.threshold /= 2
