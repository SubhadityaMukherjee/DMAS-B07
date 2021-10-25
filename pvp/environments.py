# %%
from functools import partial
from random import choices

import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from numpy.random.mtrand import normal
from sklearn.cluster import KMeans

from .agents import *

# from sklearn.datasets import make_blobs


# %%

"""
Refactor random adder to work with parts of the grid 
Add ability to spawn based on values (aka iterate over grid, pick preallocated values and spawn there)
Add more strategies
"""


def grid_adder(self, atype):
    """
    Refactored adding to the grid. Just increments unique id and adds the object to the grid and schedule
    """
    if not atype == None:
        self.unique_id += 1
        self.grid.grid[self.x][self.y] = atype
        self.schedule.add(atype)


def middle_block(self, typea="block"):
    """
    walk around / block in the middle
    """
    x_start = self.width / 3
    y_start = self.height / 3
    x_end = self.width - x_start
    y_end = self.height - y_start
    num_blocks = 0
    for (_, x, y) in self.grid.coord_iter():
        if x_start <= x <= x_end and y_start <= y <= y_end:
            self.x, self.y = x, y
            if typea == "block":
                grid_adder(self, Block(self.unique_id, self, (x, y)))
            elif typea == "cop":
                grid_adder(
                    self, Cop(self.unique_id, self, (x, y), vision=self.cop_vision)
                )
            num_blocks += 1

    free = (self.numTotalSpaces - num_blocks) * self.grid_density
    citizenProb = (free * self.ratio) / self.numTotalSpaces
    freeProb = (self.numTotalSpaces - free - num_blocks) / self.numTotalSpaces
    copProb = (free - (free * self.ratio)) / self.numTotalSpaces
    blockProb = num_blocks / self.numTotalSpaces

    for (_, x, y) in self.grid.coord_iter():
        self.citizen = Citizen(
            self.unique_id,
            self,
            (x, y),
            hardship=self.random.random(),
            regime_legitimacy=self.legitimacy,
            risk_aversion=self.random.random(),
            threshold=self.active_threshold,
            vision=self.citizen_vision,
            aggression=self.aggression,
            direction_bias=self.direction_bias,
        )
        self.x, self.y = x, y
        self.cop = Cop(self.unique_id, self, (x, y), vision=self.cop_vision)
        self.block = Block(self.unique_id, self, (x, y))
        agent_dict = {0: None, 1: self.citizen, 2: self.cop}
        agent_dict_d = {0: None, 1: self.citizen, 2: self.block}
        if x < x_start or x > x_end or y < y_start or y > y_end:
            if typea == "block":
                rand = choices([0, 1, 2], [freeProb, citizenProb, copProb])
                grid_adder(self, agent_dict[rand[0]])
            elif typea == "cop":
                rand = choices([0, 1, 2], [freeProb, citizenProb, blockProb])
                grid_adder(self, agent_dict_d[rand[0]])


def random_strategy(self):  # random distribution
    """
    Randomly places objects (original)
    """
    citizenProb = self.numCitizens / self.numTotalSpaces
    freeProb = (
        self.numTotalSpaces - self.numFreeSpaces - self.barricade
    ) / self.numTotalSpaces
    copProb = self.numCops / self.numTotalSpaces
    blockProb = self.barricade / self.numTotalSpaces

    for (_, x, y) in self.grid.coord_iter():
        self.citizen = Citizen(
            self.unique_id,
            self,
            (x, y),
            hardship=self.random.random(),
            regime_legitimacy=self.legitimacy,
            # risk_aversion=np.random.normal(),
            risk_aversion=self.random.random(),
            direction_bias=self.direction_bias,
            threshold=self.active_threshold,
            vision=self.citizen_vision,
            aggression=self.aggression,
        )
        self.cop = Cop(self.unique_id, self, (x, y), vision=self.cop_vision)
        self.block = Block(self.unique_id, self, (x, y))

        self.x, self.y = x, y
        rand = choices([0, 1, 2, 3], [freeProb, citizenProb, copProb, blockProb])
        # rand = np.random.choice([0, 1, 2, 3], p=[freeProb, citizenProb, copProb, blockProb])

        agent_dict = {0: None, 1: self.citizen, 2: self.cop, 3: self.block}
        grid_adder(self, agent_dict[rand[0]])

# %%
def side_strategy(self, side="left", agent="cop"):  # wall of cops
    """
    Left/right side : all of one type (eg all cops on the left)
    Rest filled randomly
    Create zero array
    Flatten the array and put the cops
    Reshape back
    """
    h, w = self.height, self.width
    self.temp_grid = np.reshape(self.grid.grid, -1)  # flatten

    if side == "left":  # Set cops
        self.temp_grid[: int(self.numCops)] = 2
    else:
        self.temp_grid[-int(self.numCops) :] = 2

    self.temp_grid = np.reshape(self.temp_grid, (h, w))
    citizenProb = self.numCitizens / self.numTotalSpaces
    freeProb = (
        self.numTotalSpaces - self.numFreeSpaces - self.barricade
    ) / self.numTotalSpaces
    copProb = self.numCops / self.numTotalSpaces
    blockProb = self.barricade / self.numTotalSpaces

    for (_, x, y) in self.grid.coord_iter():
        self.citizen = Citizen(
            self.unique_id,
            self,
            (x, y),
            hardship=self.random.random(),
            regime_legitimacy=self.legitimacy,
            risk_aversion=self.random.random(),
            direction_bias=self.direction_bias,
            threshold=self.active_threshold,
            vision=self.citizen_vision,
            aggression=self.aggression,
        )

        self.cop = Cop(self.unique_id, self, (x, y), vision=self.cop_vision)
        self.block = Block(self.unique_id, self, (x, y))

        agent_dict = {0: None, 1: self.citizen, 2: self.cop, 3: self.block}

        self.x, self.y = x, y

        if self.temp_grid[y][x] == 2:
            grid_adder(self, agent_dict[2])

        else:
            rand = choices([0, 1, 3], [freeProb, citizenProb, blockProb])
            grid_adder(self, agent_dict[rand[0]])


def streets(self):
    # middle
    y_start = self.height / 6
    y_end = self.height - y_start
    x_mid = self.width / 2
    # sides
    x_end = self.width / 6
    x_start = self.width - x_end

    num_blocks = 0
    for (_, x, y) in self.grid.coord_iter():
        if (
            x >= x_start
            or x <= x_end
            or ((x == x_mid or x == (x_mid + 1)) and y_start <= y <= y_end)
        ):
            self.x, self.y = x, y
            grid_adder(self, Block(self.unique_id, self, (x, y)))
            num_blocks += 1

    free = (self.numTotalSpaces - num_blocks) * self.grid_density
    citizenProb = (free * self.ratio) / self.numTotalSpaces
    freeProb = (self.numTotalSpaces - free - num_blocks) / self.numTotalSpaces
    copProb = (free - (free * self.ratio)) / self.numTotalSpaces
    blockProb = num_blocks / self.numTotalSpaces

    for (_, x, y) in self.grid.coord_iter():
        self.citizen = Citizen(
            self.unique_id,
            self,
            (x, y),
            hardship=self.random.random(),
            regime_legitimacy=self.legitimacy,
            risk_aversion=self.random.random(),
            threshold=self.active_threshold,
            vision=self.citizen_vision,
            aggression=self.aggression,
            direction_bias=self.direction_bias,
        )
        self.x, self.y = x, y
        self.cop = Cop(self.unique_id, self, (x, y), vision=self.cop_vision)
        agent_dict = {0: None, 1: self.citizen, 2: self.cop}
        if x_start > x > x_end and (
            x != x_mid and x != (x_mid + 1) or (y < y_start or y > y_end)
        ):
            rand = choices([0, 1, 2], [freeProb, citizenProb, copProb])
            grid_adder(self, agent_dict[rand[0]])
