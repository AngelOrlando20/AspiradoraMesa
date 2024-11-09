# import solara
# import matplotlib as plt
from models import VacuumModel
from agents import LukeAgent, DirtAgent

from mesa.visualization import ChartModule, CanvasGrid, ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if isinstance(agent, LukeAgent):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
    elif isinstance(agent, DirtAgent):
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2
        portrayal["Layer"] = 0
    return portrayal


testChart = ChartModule(
    [{"Label": "Dust", "Color": "Black"}], 
    canvas_width=400, canvas_height=300)

# Parameters for the model
M, N = 10, 10
num_agents = 3
dirty_percentage = 0.3

server_params = {
    "M": M,
    "N": N,
    "num_agents": num_agents,
    "dirty_percentage": dirty_percentage,
}

# Set up the visualization
grid = CanvasGrid(agent_portrayal, M, N, 600, 600)
server = ModularServer(
    VacuumModel,
    [grid, testChart],
    "Vacuum Model",
    server_params
)

server.port = 8521
server.launch()