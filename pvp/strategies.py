from functools import partial
from random import choices

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agents.block import Block
from .agents.cop import Cop
from .agents.citizen import Citizen


def grid_adder(self, atype):
    self.unique_id += 1
    self.grid[self.y][self.x] = atype
    self.schedule.add(atype)


def random_strategy(self):
    citizenProb = self.numCitizens / self.numTotalSpaces
    freeProb = (self.numTotalSpaces - self.numFreeSpaces - self.barricade) / self.numTotalSpaces
    copProb = self.numCops / self.numTotalSpaces
    blockProb = self.barricade / self.numTotalSpaces

    rand = choices([0, 1, 2, 3], [freeProb, citizenProb, copProb, blockProb])
    if rand[0] == 1:
        grid_adder(self, self.citizen)
    elif rand[0] == 2:
        grid_adder(self, self.cop)
    elif rand[0] == 3:
        grid_adder(self, self.block)
    else:
        return -1
