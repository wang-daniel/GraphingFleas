from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, NullFormatter

class State(Enum):
	RED = "r"
	BLUE = "b"

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
		self.xs = np.array([flea.position.x])
		self.ys = np.array([flea.position.y])
		self.colors = np.array([initialState.value])

	def step(self):
		self.flea.step()
		self.xs = np.append(self.xs, self.flea.position.x)
		self.ys = np.append(self.ys, self.flea.position.y)
		if self.flea.position in self.visited:
			newState, turnDirection = rule[self.visited[self.flea.position]]
		else:
			newState, turnDirection = rule[self.initialState]
		self.colors = np.append(self.colors, newState.value)
		self.visited[Coordinate(self.flea.position.x, self.flea.position.y)] = newState
		self.flea.turn(turnDirection)

	def visualize(self, size=5):
		plt.xlim(-1 * size, size)
		plt.ylim(-1 * size, size)
		plt.gca().set_aspect('equal', adjustable='box')
		x = np.arange(-1 * size, size + 1, 1)
		y = np.arange(-1 * size, size + 1, 1)
		xx, yy = np.meshgrid(x, y)
		plt.scatter(xx, yy, c=self.initialState.value, s=25, zorder=3) 
		plt.axis('on')
		ax = plt.gca()
		ax.xaxis.set_major_locator(MultipleLocator(1))
		ax.xaxis.set_major_formatter(NullFormatter())
		ax.yaxis.set_major_locator(MultipleLocator(1))
		ax.yaxis.set_major_formatter(NullFormatter())
		ax.tick_params(axis='both', length=0)
		plt.grid(True, ls=':')
		plt.gcf().canvas.mpl_connect('key_press_event', self.on_keyboard)
		self.draw()
		plt.show()

	def on_keyboard(self, event):
		if event.key == 'right':
			self.lastVisited.remove()
			self.step()
			self.draw()
			plt.draw()

	def draw(self):
		plt.plot(self.xs, self.ys, 'k-', zorder=0)
		plt.scatter(self.xs, self.ys, c=self.colors, s=25, zorder=3) 
		self.lastVisited = plt.scatter(self.xs[-1], self.ys[-1], c=self.colors[-1], s=25, zorder=3, edgecolors="k", linewidths=2)

if __name__ == "__main__":
	flea = Flea(Coordinate(0, 0), Direction.UP)
	rule = {
		State.RED: (State.BLUE, Direction.DOWN), 
		State.BLUE: (State.BLUE, Direction.LEFT)}
	grid = Grid(flea, rule, State.RED)
	grid.visualize()