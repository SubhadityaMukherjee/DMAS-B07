import math

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
        # self.hardship = hardship
        # self.regime_legitimacy = regime_legitimacy
        self.risk_aversion = risk_aversion
        self.threshold = threshold
        self.condition = "Quiescent"
        self.vision = vision
        self.jail_sentence = 0
        # self.grievance = self.hardship * (1 - self.regime_legitimacy)
        self.arrest_probability = None
        self.aggression = aggression
        self.susceptibility_to_aggression = self.random.random()

    def step(self):
        """
        Decide whether to activate, then move if applicable.
        """
        if self.jail_sentence:
            # self.jail_sentence -= 1
            self.model.jailed_agents.append(self)
            return  # no other changes or movements if agent is in jail.

        if self.aggression > 0.3:  # TODO
            self.risk_aversion = self.risk_aversion / 2

        self.update_neighbors()
        self.update_estimated_arrest_probability()

        net_risk = self.risk_aversion * self.arrest_probability
        if (
            self.condition == "Quiescent"
            and (self.susceptibility_to_aggression - self.arrest_probability)
            > self.threshold
        ):
            self.condition = "Active"
        elif (
            self.condition == "Active"
            and (self.susceptibility_to_aggression - self.arrest_probability)
            <= self.threshold
        ):
            self.condition = "Quiescent"

        swap = False
        for agent in self.neighbors:
            if agent.breed == "citizen" and agent.jail_sentence > 0:
                swap = True
                break

        if self.susceptibility_to_aggression > 0.8 and swap:
            self.condition = "Active"

        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

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
