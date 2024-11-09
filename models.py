from mesa import Model, DataCollector
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from agents import LukeAgent, DirtAgent
import random


def dust_collector(model: Model):
    dust = [agent.dust for agent in model.schedule.agents]
    return dust[0]


class VacuumModel(Model):
    def __init__(self, M, N, num_agents, dirty_percentage):
        self.num_agents = num_agents
        self.grid = MultiGrid(M, N, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        
        # Add vacuum agents
        for i in range(self.num_agents):
            agent = LukeAgent(i, self)
            self.grid.place_agent(agent, (1, 1))
            self.schedule.add(agent)
        
        # Add dirt agents (representing dirty cells)
        self.dirty_cells = set()
        num_dirty_cells = int(M * N * dirty_percentage)
        for i in range(num_dirty_cells):
            x, y = random.randint(0, M-1), random.randint(0, N-1)
            if (x, y) not in self.dirty_cells:
                dirt = DirtAgent(i + num_agents, self)
                self.grid.place_agent(dirt, (x, y))
                self.dirty_cells.add((x, y))

        
        self.datacollector = DataCollector(
            model_reporters={"Dust": dust_collector }
        )


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def clean_cell(self, pos):
        if pos in self.dirty_cells:
            self.dirty_cells.remove(pos)

    def is_cell_dirty(self, pos):
        return pos in self.dirty_cells