from numpy import ndarray 

class Automaton(object):
    """
    Base class of cellular automata
    """

    def __init__(self, grid, states, **kwargs):
        self.grid = grid
        self.states = states
    
    def get_neighborhood(self, cell):
        """
        Abstract method, intended to return the neighborhood of the provided cell
        """
        raise Exception("Not implemented")

    def rule(self, *args):
        """
        Abstract method, intended to execute an automaton rule
        """
        raise Exception("Not implemented")
        
    def run_rule(self, *args):
        """
        Run the automaton's rule
        """
        self.rule(*args)

class Tilemap2dAutomaton(Automaton):
    """
    2d tilemap cellular automaton implementation
    """

    def __init__(self, grid, states, **kwargs):
        super(Tilemap2dAutomaton, self).__init__(grid, states, **kwargs)

    def tile_within_bounds(self, x, y):
        """
        Internal method to determine bounds of classic 2d array (non-troroidal)
        """
        grid_y, grid_x = self.grid.shape

        if x < 0 or x >= grid_x or \
           y < 0 or y >= grid_y:
            return False

        return True

    def get_neighborhood(self, cell):
        """
        Returns the cell's neighborhood as the 8 surrounding cells and the cell
        in question, inclusively.
        """
        x = 0
        y = 1
        neighbors = [
            (cell[x]-1, cell[y]-1), (cell[x], cell[y]-1), (cell[x]+1, cell[y]-1),
            (cell[x]-1, cell[y]), (cell[x], cell[y]), (cell[x]+1, cell[y]),
            (cell[x]-1, cell[y]+1), (cell[x], cell[y]+1), (cell[x]+1, cell[y]+1)]

        return [cell for cell in neighbors if self.tile_within_bounds(cell[x], cell[y])]

    def rule(self, *args):
        #expects 2d ndarray from numpy for simplicity. 
        grid_y, grid_x = self.grid.shape

        output_map = ndarray(shape=self.grid.shape) 

        for y in range(grid_y):
            for x in range(grid_x):
                neighbors = self.get_neighborhood((x, y))

                #if >= 5 lands exist, it multiplies, otherwise starves (4-5 rule)
                if self.check_neighbors_state(neighbors, 0) >= 5:
                    output_map[y][x] = self.states[0]
                else:
                    output_map[y][x] = self.states[1] #turn to something else. 
                    #TODO: currently default is contrived

        self.grid = output_map

    def check_neighbors_state(self, neighborhood, state):
        return len([n for n in neighborhood if self.grid[n[1]][n[0]] == state])

