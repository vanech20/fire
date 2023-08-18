from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from mesa.visualization.UserParam import Slider

class Tree(Agent): #En esta clase se definen los posibles estados en los que puede estra un arbol 
    FINE = 0 
    BURNING = 1
    BURNED_OUT = 2
    def __init__(self, model: Model): #El metodo __init__ inicializa un arbol con su condición inicial (sano).
        super().__init__(model.next_id(), model)
        self.condition = self.FINE

    def step(self): #el metodo step define como es que se va a comportar el arbol en un paso de tiempo
        if self.condition == self.BURNING: #el arbol se encuentra en estado BURNING
            for neighbor in self.model.grid.iter_neighbors(self.pos, moore=False):
                if neighbor.condition == self.FINE: #si el arbol vecino esta en estado FINE cambiara su estado a BURNING debido a la propagacion de fuego
                    neighbor.condition = self.BURNING #el estado del arbol vecino cmabia a BURNING
            self.condition = self.BURNED_OUT #cambia su propia condicion a BURNED OUT

class Forest(Model): #La clase Forest hereda de Model y representa el entorno en el que se desarrolla la simulacion
    def __init__(self, height=50, width=50, density=0.20): #En este metodo se establece la configuracion inicial del bosque con altura, ancho y densidad.
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=False)
        for _,(x,y) in self.grid.coord_iter():
            if self.random.random() < density:
                tree = Tree(self)
                if x == 0:
                    tree.condition = Tree.BURNING
                self.grid.place_agent(tree, (x,y))
                self.schedule.add(tree)

    def step(self): #Este metodo llama al metodo step de schedule, lo que hace avanzar un paso de tiempo en la simulacion.
        self.schedule.step()

def agent_portrayal(agent): #esta funcion define como se representaran visualmente los agentes (arboles) en la interfaz de visualizacion
    if agent.condition == Tree.FINE:
        portrayal = {"Shape": "circle", "Filled": "true", "Color": "Green", "r": 0.75, "Layer": 0}
    elif agent.condition == Tree.BURNING:
        portrayal = {"Shape": "circle", "Filled": "true", "Color": "Red", "r": 0.75, "Layer": 0}
    elif agent.condition == Tree.BURNED_OUT:
        portrayal = {"Shape": "circle", "Filled": "true", "Color": "Gray", "r": 0.75, "Layer": 0}
    else:
        portrayal = {}

    return portrayal

grid = CanvasGrid(agent_portrayal, 50, 50, 450, 450) #Se crea una cuadricula visual que mostrara la simulacion.
server = ModularServer(Forest, [grid], "Forest", {
     "density": Slider("Tree density", 0.45, 0.01, 1.0, 0.01),
     "width":50, "height":50
 }) 

server.port = 8522 # The default
server.launch()
