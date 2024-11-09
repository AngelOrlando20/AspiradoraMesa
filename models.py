from mesa import Model, DataCollector
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from agents import LukeAgent, DirtAgent
import random


def dust_collector(model: Model):
    dust = [agent.dust for agent in model.schedule.agents]
    return dust[0]


def clean_percent_collector(model: Model):
    return model.percentage_dirty_cells()


def get_agent_dust(model: Model):
    return 0


class VacuumModel(Model):
    def __init__(self, M, N, num_agents, dirty_percentage, max_time):
        self.num_agents = num_agents
        self.M = M
        self.N = N
        self.grid = MultiGrid(M, N, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.max_time = max_time

        self.running = True
        behaviors = ["random", "bfs", "djikstra", "random_dust"]

        
        # Add vacuum agents
        for i in range(self.num_agents):
            # Seleccionar un comportamiento aleatorio para cada agente
            metodo = random.choice(behaviors)
            agent = LukeAgent(i, self, metodo=metodo)
            
            # Asignar una posición aleatoria en la cuadrícula
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
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
            model_reporters={"Dust": dust_collector, 
                             "CleanPercentage": clean_percent_collector },
            agent_reporters={ "agent_dust" : lambda l: l.dust, "agent_moves": lambda l: l.movements }
        )


    def percentage_dirty_cells(self):
        amount_dirty = len(self.dirty_cells)
        return 1 - float(amount_dirty) / self.grid.num_cells


    def step(self):
        if (self.schedule.time >= self.max_time - 2):
            self.running = False
            return
        
        print(self.datacollector.get_agent_vars_dataframe())
        
        self.datacollector.collect(self)
        self.schedule.step()

    def clean_cell(self, pos):
        if pos in self.dirty_cells:
            self.dirty_cells.remove(pos)

    def is_cell_dirty(self, pos):
        return pos in self.dirty_cells