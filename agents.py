from mesa import Agent
import heapq
import random


class DirtAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class LukeAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.movements = 0
        self.dust = 0

        self.metodo = "djikstra"
        # Variable para algoritmo: random with memory.
        self.memory = []
        # Variable para algoritmo: snake.
        self.direction = (0, 1)
        self.path = []

    
    def step(self):
        # Revisar si la aspiradora está sobre tierra y borrar el polvo
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, DirtAgent):
                self.model.grid.remove_agent(obj)
                self.model.clean_cell(self.pos)
                self.dust += 1
        
        if len(self.path) == 0:
            if self.metodo == "bfs":
                self.path = self.bfs()
            elif self.metodo == "djikstra":
                self.path = self.dijkstra()
            elif self.metodo == "random_dust":
                self.path = self.dirt_directed_move()
            elif self.metodo == "random":
                self.path = self.randomStep()

        self.follow_path()


    def randomStep(self):
        """Movimiento aleatorio en las celdas vecinas."""
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        if self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)
            self.movements += 1
    

    def dirt_directed_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

        # Calculate the dirt level in each neighboring cell
        dirt_levels = []
        for neighbor in possible_steps:
            cell_contents = self.model.grid.get_cell_list_contents([neighbor])
            dirt_level = sum(1 for obj in cell_contents if isinstance(obj, DirtAgent))
            dirt_levels.append(dirt_level)

        # Choose the direction with the highest dirt level
        max_dirt_index = dirt_levels.index(max(dirt_levels))
        new_position = possible_steps[max_dirt_index]

        if max(dirt_levels) == 0:
            new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)
        self.movements += 1


    def bfs(self):
        """Algoritmo de búsqueda en amplitud para encontrar una celda sucia."""
        queue = [(self.pos, [])]  # Tupla de la posición actual y el camino recorrido
        visited = set()
        
        while queue:
            current_position, path = queue.pop(0)

            # Verifica si la celda está sucia
            cell_contents = self.model.grid.get_cell_list_contents([current_position])
            if any(isinstance(obj, DirtAgent) for obj in cell_contents):
                return path
            
            # Marcar la posición como visitada
            visited.add(current_position)
            
            # Añadir posiciones vecinas no visitadas a la cola
            neighbors = self.model.grid.get_neighborhood(current_position, moore=True, include_center=False)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        
        return []
    

    def dijkstra(self):
        """Algoritmo de Dijkstra para encontrar la celda sucia más cercana."""
        heap = [(0, self.pos, [])]  # Tupla de (distancia acumulada, posición actual, camino)
        visited = set()
        
        while heap:
            distance, current_position, path = heapq.heappop(heap)
            
            # Verifica si la celda está sucia
            cell_contents = self.model.grid.get_cell_list_contents([current_position])
            if any(isinstance(obj, DirtAgent) for obj in cell_contents):
                return path
            
            # Marcar la posición como visitada
            visited.add(current_position)
            
            # Añadir posiciones vecinas no visitadas al heap
            neighbors = self.model.grid.get_neighborhood(current_position, moore=True, include_center=False)
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_distance = distance + 1  # Cada paso tiene una distancia de 1
                    heapq.heappush(heap, (new_distance, neighbor, path + [neighbor]))
        return []


    def follow_path(self):
        """Sigue el camino calculado hasta la celda sucia."""
        next_position = self.path.pop(0)
        self.model.grid.move_agent(self, next_position)
        self.movements += 1