from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, NullFormatter

class State(Enum):
	"""
	The State enum represents possible states (colors) of the grid vertices. 
	The values of the enums are the pyplot shortcuts for the corresponding
	colors, found here: https://matplotlib.org/2.0.2/api/colors_api.html.
	"""
	RED = "r"
	BLUE = "b"

class Direction(Enum):
	"""
	The Direction enum represents possible directions that the flea could be
	facing. On a 2D lattice grid, these are up down left and right. Their values
	are chosen so that turning directions can be achieved just be adding mod 4.
	For example, a right turn followed by a left turn is the same as going up, 
	as 1 + 3 = 0 (mod 4).
	"""
	UP = 0
	LEFT = 1
	DOWN = 2
	RIGHT = 3

class Coordinate:
	"""
	The Coordinate class just holds an x and a y coordinate. The reason I didn't use 
	a Python tuple is because I'm not sure if they're hashable, as I use them 
	as keys to a dictionary. Also, it's more extensible to use a separate class
	in case we look at different coordinate systems later (e.g. hexagonal lattices).
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

	def __hash__(self):
		return hash((self.x, self.y))

	def __eq__(self, other):
		return (self.x, self.y) == (other.x, other.y)

class Flea:
	"""
	The Flea class represents the jumping fleas of our problem. A flea is determined
	by the direction that it is facing, which is a Direction enum, and its position, 
	which is a Coordinate.
	"""
	def __init__(self, initialPosition, initialDirection):
		self.position = initialPosition
		self.direction = initialDirection

	def __str__(self):
		return self.position.__str__() + ", Direction: " + str(self.direction.name)

	def step(self):
		"""
		Take one "step" in the direction that the flea is facing.
		"""
		if (self.direction == Direction.UP):
			self.position.y += 1
		if (self.direction == Direction.LEFT):
			self.position.x -= 1 
		if (self.direction == Direction.DOWN):
			self.position.y -= 1
		if (self.direction == Direction.RIGHT):
			self.position.x += 1
	
	def turn(self, newDirection):
		"""
		Changes flea's direction based on its current direction and a new turn direction
		using the mod 4 addition magic described in the Direction enum.
		"""
		self.direction = Direction((self.direction.value + newDirection.value) % 4)

class Grid:
	"""
	The Grid class represents the grid that the flea is jumping around on. It is determined
	by its initial state, a flea (which has an initial position and direction), and a rule.
	The rule is a map from a state to a (state, turn direction) tuple 
	(see http://www-math.mit.edu/~dav/projectsB.pdf) for more information.

	In addition, the visited dictionary is used to keep track of the states of coordinates
	that have already been visited by the flea, and the xs, ys, and colors arrays are used
	for visualization purposes.
	"""
	def __init__(self, flea, rule, initialState):
		self.flea = flea
		self.rule = rule
		self.initialState = initialState
		self.visited = {} 
		self.xs = np.array([flea.position.x])
		self.ys = np.array([flea.position.y])
		self.colors = np.array([initialState.value])

	def step(self):
		"""
		In a "grid step", the flea takes a step, and then we use the
		state (color) of its position in order to determine which direction
		that the flea turns and the new state of that position, using the 
		rule dictionary.
		"""
		self.flea.step()
		if self.flea.position in self.visited:
			newState, turnDirection = rule[self.visited[self.flea.position]]
		else:
			newState, turnDirection = rule[self.initialState]
		self.visited[Coordinate(self.flea.position.x, self.flea.position.y)] = newState
		self.flea.turn(turnDirection)

		self.xs = np.append(self.xs, self.flea.position.x)
		self.ys = np.append(self.ys, self.flea.position.y)
		self.colors = np.append(self.colors, newState.value)

	def visualize(self, size=5):
		"""
		blah blah plotting code that I copied pasted off stack overflow
		"""
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
		"""
		steps the grid when the right arrow key is pressed
		"""
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
