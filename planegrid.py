from enum import Enum

class State(Enum):
  BLACK = 1
  WHITE = 2

class Direction(Enum):
  UP = 0
  LEFT = 1
  DOWN = 2
  RIGHT = 3

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ")"

  # I defined __hash__ and __eq__ methods because Coordinates are used
  # as keys in the "visited" dictionary of the Grid class
  def __hash__(self):
    return hash((self.x, self.y))

  def __eq__(self, other):
    return (self.x, self.y) == (other.x, other.y)

class Flea:
  def __init__(self, initialPosition, initialDirection):
    self.position = initialPosition
    self.direction = initialDirection

  def __str__(self):
    return self.position.__str__() + ", Direction: " + str(self.direction.name)

  def step(self):
    if (self.direction == Direction.UP):
      self.position.y += 1
    if (self.direction == Direction.LEFT):
      self.position.x -= 1 
    if (self.direction == Direction.DOWN):
      self.position.y -= 1
    if (self.direction == Direction.RIGHT):
      self.position.x += 1

  def turn(self, newDirection):
    self.direction = Direction((self.direction.value + newDirection.value) % 4)

class Grid:
  def __init__(self, flea, rule, initialState):
    self.flea = flea
    self.rule = rule
    self.initialState = initialState
    self.visited = {} 

  def step(self):
    self.flea.step()
    if self.flea.position in self.visited:
      newState, turnDirection = rule[self.visited[self.flea.position]]
    else:
      newState, turnDirection = rule[self.initialState]
    self.visited[Coordinate(self.flea.position.x, self.flea.position.y)] = newState
    self.flea.turn(turnDirection)

def print_grid(grid):
  for k, v in grid.items():
    print(k)
    print(v)

if __name__ == "__main__":
  flea = Flea(Coordinate(0, 0), Direction.UP)
  rule = {State.BLACK: (State.WHITE, Direction.DOWN), State.WHITE: (State.WHITE, Direction.LEFT)}
  grid = Grid(flea, rule, State.BLACK)
  for i in range(500):
    grid.step()
  print_grid(grid.visited)
