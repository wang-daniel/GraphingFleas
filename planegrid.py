from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, NullFormatter
import math

class State(Enum):
	"""
	The State enum represents possible states (colors) of the grid vertices.
	The values of the enums are the pyplot shortcuts for the corresponding
	colors, found here: https://matplotlib.org/2.0.2/api/colors_api.html.
	"""
	RED = "r"
	BLUE = "b"
	GREEN = "g"

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
	def __init__(self, initialPosition, initialDirection, mute = False):
		self.position = initialPosition
		self.direction = initialDirection
		self.mute = mute

	def __str__(self):
		return self.position.__str__() + ", Direction: " + str(self.direction.name)

	def step(self):
		"""
		Take one "step" in the direction that the flea is facing.
		"""
		if (self.direction == Direction.UP):
			self.position.y += 1
			if not self.mute: print("UP")
		if (self.direction == Direction.LEFT):
			self.position.x -= 1
			if not self.mute: print("LEFT")
		if (self.direction == Direction.DOWN):
			self.position.y -= 1
			if not self.mute: print("DOWN")
		if (self.direction == Direction.RIGHT):
			self.position.x += 1
			if not self.mute: print("RIGHT")

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
	that have already been visited by the flea.
	"""
	def __init__(self, flea, rule, defaultState, initialStates = np.empty([0]), initialStatesInterpreter = None):
		self.flea = flea
		self.rule = rule
		self.defaultState = defaultState
		self.initiated = {}
		self.visited = set([])
		# self.initiated is a hashmap whose keys are the positions whose states
		# have been changed at least once; and the values are the current states
		# of those positions.

		# Using the inputted initial states array to initiate some positions
		if initialStates.shape != (0,):
			r = initialStates.shape[0]
			c = initialStates.shape[1]
			if r % 2 == 0 or c % 2 == 0:
				raise ValueError("The width and length of the initial states board must be both odd.")
			if initialStatesInterpreter == None:
				raise ValueError("An initial state board was provided without an interpreter. ")
			for y in range(0, r):
				for x in range(0, c):
					if initialStates[y, x] != 0:
						self.initiated[Coordinate(x - c//2, r//2 - y)] = initialStatesInterpreter(initialStates[y, x])

		self._radius_ = 0
		self._coverage_ = 0
	def step(self):
		"""
		In a "grid step", the flea takes a step, and then we use the
		state (color) of its position in order to determine which direction
		that the flea turns and the new state of that position, using the
		rule dictionary.
		"""
		self.flea.step()
		if self.flea.position in self.initiated:
			newState, turnDirection = rule[self.initiated[self.flea.position]]
		else:
			newState, turnDirection = rule[self.defaultState]
		if not self.flea.position in self.visited:
			self._radius_ = max((self.flea.position.x**2 + self.flea.position.y**2)**0.5, self._radius_)
			self._coverage_ += 1
			self.visited.add(self.flea.position)
		self.initiated[Coordinate(self.flea.position.x, self.flea.position.y)] = newState
		self.flea.turn(turnDirection)

	def get_state(self, position):
		"""
		Returns the state of the grid at position
		"""
		if position in self.initiated.keys():
			return self.initiated[position]
		return self.defaultState

	def on_keyboard(self, event, lines):
		"""
		steps the grid when the right arrow key is pressed
		"""
		if event.key == 'right':
			self.fleaPoint.remove()
			self.step()
			self.draw(lines)
			plt.draw()

	def draw(self, lines):
		x = self.flea.position.x
		y = self.flea.position.y
		self.fleaLoc = Coordinate(x-self.x0, y-self.y0)
		if hasattr(self, 'fleaLoc') and lines:
			plt.plot([self.fleaLoc.x, x], [self.fleaLoc.y, y], 'k-', zorder=0)
		color = self.initiated[self.flea.position].value if flea.position in self.initiated else self.defaultState.value
		plt.scatter(x-self.x0, y-self.y0, c=color, s=25, zorder=3)
		self.fleaPoint = plt.scatter(x-self.x0, y-self.y0, c=color, s=25, zorder=3, edgecolors="k", linewidths=2)

	def visualize(self, size = 5, lines = True):
		"""
		blah blah plotting code that I copied pasted off stack overflow
		"""
		self.x0 = self.flea.position.x
		self.y0 = self.flea.position.y
		print([self.x0, self.y0])
		plt.xlim(-1 * size, size)
		plt.ylim(-1 * size, size)
		plt.gca().set_aspect('equal', adjustable='box')
		x = np.arange(-1 * size, size + 1, 1)
		y = np.arange(-1 * size, size + 1, 1)
		xx, yy = np.meshgrid(x, y)
		plt.scatter(xx, yy, c=self.defaultState.value, s=25, zorder=3)
		for i in x:
			for j in y:
				position = Coordinate(i+self.x0,j+self.y0)
				color = self.initiated[position].value if position in self.initiated else self.defaultState.value
				if color != self.defaultState.value:
					plt.scatter(i, j, c = color, s=25, zorder=3)

		plt.axis('on')
		ax = plt.gca()
		ax.xaxis.set_major_locator(MultipleLocator(1))
		ax.xaxis.set_major_formatter(NullFormatter())
		ax.yaxis.set_major_locator(MultipleLocator(1))
		ax.yaxis.set_major_formatter(NullFormatter())
		ax.tick_params(axis='both', length=0)
		plt.grid(True, ls=':')
		plt.gcf().canvas.mpl_connect('key_press_event', lambda x: self.on_keyboard(x, lines))
		self.draw(lines)
		plt.show()

	def radius(self):
		"""
		Computes the "radius" of the path.
		"""
		return self._radius_
	def coverage(self):
		"""
		Computes the number of points ever visited
		"""
		return self._coverage_

if __name__ == "__main__":
	flea = Flea(Coordinate(0, 0), Direction.RIGHT, mute = True)

	# Here I create the initial states grid. 0 denotes the red state, and 1 denotes the blue state
	# The row and column marked with "###" is the origin
															###
	initialStates = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  ###
							  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
	initialStatesInterpreter = lambda x: State.BLUE if x == 1 else State.RED

	rule = {
		State.RED: (State.BLUE, Direction.LEFT),
		State.BLUE: (State.RED, Direction.RIGHT),
		State.GREEN: (State.RED, Direction.LEFT)}
	grid = Grid(flea, rule, State.RED)
	#grid = Grid(flea, rule, State.RED, initialStates = initialStates, initialStatesInterpreter = initialStatesInterpreter)
	#grid.visualize(10, lines = True)

	# Un-comment the following code to run the system 15000 times before visualizing!

	radii = []
	percent_coverages = []

	for step in range(15000):
		#print("{}: ".format(step), end = "")
		grid.step()
		r = grid.radius()
		radii.append(grid.radius())
		percent_coverages.append(grid.coverage() / (math.pi * (r**2)))
	fig, ax1 = plt.subplots()

	color = 'tab:red'
	ax1.set_xlabel('Time')
	ax1.set_ylabel('Radius', color=color)
	ax1.plot(radii, color=color)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

	color = 'tab:blue'
	ax2.set_ylabel('Percent Coverage', color=color)  # we already handled the x-label with ax1
	ax2.plot(percent_coverages, color=color)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.show()
	grid.visualize(size = 30, lines = False)
