from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from .agent import Block, Citizen, Cop
from .model import EpsteinCivilViolence

COP_COLOR = "#000000"
AGENT_QUIET_COLOR = "#0066CC"
AGENT_REBEL_COLOR = "#CC0000"
JAIL_COLOR = "#757575"
BARRICADE_COLOR = "#00FF00"


def citizen_cop_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "x": agent.pos[0],
        "y": agent.pos[1],
        "Filled": "true",
    }

    if type(agent) is Citizen:
        color = (
            AGENT_QUIET_COLOR if agent.condition == "Quiescent" else AGENT_REBEL_COLOR
        )
        color = JAIL_COLOR if agent.jail_sentence else color
        portrayal["Color"] = color
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0

    elif type(agent) is Block:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = BARRICADE_COLOR
        portrayal["h"] = 0.9
        portrayal["w"] = 0.9
        portrayal["Layer"] = 0

    elif type(agent) is Cop:
        portrayal["Color"] = COP_COLOR
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
    return portrayal


model_params = {
    "grid_density": UserSettableParameter(  # TODO: make grid density
        param_type="slider",
        name="Grid density",
        value=0.8,
        min_value=0,
        max_value=1,
        step=0.01,
        description="",
    ),
    "ratio": UserSettableParameter(  # TODO: make citizen to cop ratio
        param_type="slider",
        name="Citizen to cop ratio",
        value=0.8,
        min_value=0,
        max_value=1,
        step=0.001,
        description="",
    ),
    "height": 40,
    "width": 40,
    "citizen_vision": 7,
    "cop_vision": 7,
    "legitimacy": 0.8,
    "max_jail_term": 1000,
    "jail_capacity": 500,
    "strategy": "random",
    "barricade": 50,
}


class AgentLeftElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        cop = 0
        citizen = 0
        block = 0
        for agent in model.schedule.agents:
            if agent.breed == "citizen":
                citizen += 1
            if agent.breed == "cop":
                cop += 1
            if agent.breed == "Block":
                block += 1
        stats = f"""Number of citizens: {str(citizen)}, Number of cops: {str(cop)}, Number of blocks: {str(block)}"""
        return stats


chart = ChartModule(
    [{"Label": "jailed", "Color": "Black"}], data_collector_name="datacollector"
)

canvas_element = CanvasGrid(citizen_cop_portrayal, 40, 40, 480, 480)
server = ModularServer(
    EpsteinCivilViolence,
    [canvas_element, AgentLeftElement()],
    "Epstein Civil Violence",
    model_params,
)
