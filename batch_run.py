# from pvp.server import *
from mesa.batchrunner import BatchRunner
import pandas as pd

from pvp.model import ProtestersVsPolice

# JUST CHANGE THESE
iterations = 3 # no of times to run exp with same params
max_steps = 250 # no of steps in a single exper

model_params_batch = {
    "max_iters":max_steps,
    "grid_density":0.8,
    "ratio": 0.8,
    "jail_capacity":50,
    "environment": "Random distribution",
    "wrap": "Wrap around",
    "direction_bias": "Random",
    "height": 40,
    "width": 40,
    "citizen_vision": 7,
    "cop_vision": 7,
    "legitimacy": 0.8,
    "max_jail_term": 1000,
    "barricade": 50,
    "funmode": False,  # Set to True for sound effects
}

# IGNORE BELOW

nice_param_string = [f"{x}_{model_params_batch[x]}" for x in model_params_batch.keys()]

df_final = pd.DataFrame(index=["Quiescent","Active", "Deviant", "Jailed"])
for i in range(iterations):
    batch_run = BatchRunner(ProtestersVsPolice,
                            fixed_parameters= model_params_batch,
                            iterations=1,
                            max_steps=max_steps,
                            )
    batch_run.run_all()

    data_collector_agents = batch_run.get_collector_model()
    tes = data_collector_agents[list(data_collector_agents.keys())[-1]]
    df_final = df_final.append(tes.iloc[-1])
    df_final = df_final.dropna()

print(df_final.mean())