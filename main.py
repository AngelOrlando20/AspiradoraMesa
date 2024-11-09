# import solara
# import matplotlib as plt
from models import VacuumModel
from agents import LukeAgent, DirtAgent
# from charts import GraphLukeAgents

from mesa.visualization import ChartModule, CanvasGrid, Slider, ModularServer


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


# Parameters for the model
M, N = 10, 10
num_agents = 3
dirty_percentage = 0.7

server_params = {
    "M": M,
    "N": N,
    "num_agents": num_agents,
    "dirty_percentage": dirty_percentage,
    "max_time": Slider("Max_Time", 100, 10, 250, 5)
}

testChart = ChartModule(
    [{"Label": "Dust", "Color": "Black"}], 
    canvas_width=200, canvas_height=150)
cleanPercentChart = ChartModule(
    [{"Label": "CleanPercentage", "Color": "Gray"}], 
    canvas_width=200, canvas_height=150)
# agentChart = GraphLukeAgents(num_agents, canvas_width=200, canvas_height=150)

# Set up the visualization
grid = CanvasGrid(agent_portrayal, M, N, 600, 600)
server = ModularServer(
    VacuumModel,
    [grid, testChart, cleanPercentChart],
    "Vacuum Model",
    server_params
)

server.port = 8521
server.launch()