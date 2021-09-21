from random import choices

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import Block, Citizen, Cop


def random_strategy(self, x, y, freeProb, citizenProb, copProb, blockProb):
    rand = choices([0, 1, 2, 3], [freeProb, citizenProb, copProb, blockProb])
    if rand[0] == 1:
        citizen = Citizen(
            self.unique_id,
            self,
            (x, y),
            hardship=self.random.random(),
            regime_legitimacy=self.legitimacy,
            risk_aversion=self.random.random(),
            threshold=self.active_threshold,
            vision=self.citizen_vision,
            aggression=self.aggression,
        )
        self.unique_id += 1
        self.grid[y][x] = citizen
        self.schedule.add(citizen)
    elif rand[0] == 2:
        cop = Cop(self.unique_id, self, (x, y), vision=self.cop_vision)
        self.unique_id += 1
        self.grid[y][x] = cop
        self.schedule.add(cop)
    elif rand[0] == 3:
        block = Block(self.unique_id, self, (x, y))
        self.unique_id += 1
        self.grid[y][x] = block
        self.schedule.add(block)
    else:
        return -1
