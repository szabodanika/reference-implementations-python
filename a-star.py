class Connection:
	def __init__(self, parent, child, distance):
		self.parent = parent
		self.child = child
		self.distance = distance

class Node:
	def __init__(self, name, heuristic):
		# basic node attributes
		self.name = name
		self.connections = []

		# additional attributes for A* algorithm
		self.parent = None
		self.g = 0  # distance from start
		self.h = heuristic  # distance to goal

	def connect(self, node, dist):
		self.connections.append(Connection(self, node, dist))

	def dist(self, node):
		for conn in self.connections:
			if conn.child == node:
				# print("Distance between {0} - {1} : {2}".format(self, node, conn.distance))
				return conn.distance
		raise Exception("Can't return distance: {0} is not connected to {1}".format(self, node))

	def get_successors(self):
		return [conn.child for conn in self.connections]

	def is_goal(self):
		goal = "G" in self.name
		# print(self.name + " is goal: " + str(goal))
		return goal

	def backtrack(self, totalCost = 0):
		if self.parent:
			return "{0} -{1}-> {2}".format(self.parent.backtrack(totalCost + self.parent.dist(self)), self.parent.dist(self),  self.name)
		else:
			return "total cost: {0}\n{1}".format(totalCost, self.name)

	def __str__(self):
		return "{0}".format(self.name)
		# return "[{0}] {1}:{2}:{3}".format(self.name, self.g, self.h, self.f)

# creating nodes
a = Node("A", 4)
b = Node("B", 5)
c = Node("C", 6)
d = Node("D", 4)
e = Node("E", 6)
f = Node("F", 2)
g1 = Node("G1", 0)
g2 = Node("G2", 0)
h = Node("H", 3)
s = Node("S", 6)
nodes = [a, b, c, d, e, f, g1, g2, h, s]

# connecting nodes
a.connect(g1, 9)
a.connect(b, 5)
b.connect(a, 5)
b.connect(c, 3)
c.connect(s, 4)
c.connect(f, 5)
c.connect(h, 9)
d.connect(c, 5)
d.connect(e, 3)
e.connect(g2, 4)
e.connect(s, 10)
f.connect(b, 8)
f.connect(g1, 8)
h.connect(d, 10)
h.connect(g2, 6)
s.connect(d, 6)
s.connect(b, 4)
s.connect(a, 8)

# defining heuristics
print("Search space prepared")

# initializaiton
open = [s]
closed = []
ITERATION_LIMIT = 20
iteration_counter = 0
# print(*a.getSuccessors())

while len(open) != 0:
	# setting hard iteration limit
	iteration_counter += 1
	print("\n### Iteration {0} ###".format(iteration_counter))
	if iteration_counter == ITERATION_LIMIT:
		break
		raise Exception("Reached iteration limit {0}".format(ITERATION_LIMIT))

	print("Open list:")
	print(*open)
	print("Closed list:")
	print(*closed)

	# find lowest total cost node from open list
	current = open[0]

	# checking total costs of open nodes
	print("checking open nodes")
	for node in open:
		print("{0}.f = {1}".format(node, node.g + node.h))
		if current.g + current.h > node.g + node.h:
			current = node
	print("picked {0} as current node because its {1}.f is {2}".format(current, current, current.g + current.h))

	print("moving current node {0} from open to closed".format(current))
	closed.append(current)
	open.remove(current)

	# check if we reached a goal
	if current.is_goal():
		print("!!! reached goal node {0}".format(current))
	# if we only had one goal state then we could end the search here

	print("{0}'s successors:".format(current))
	print(*current.get_successors())
	for successor in current.get_successors():

		# check child is already in closed list
		if successor in closed:
			break

		# child is not in closed list
		# calculate f, g and h
		successor.g = current.g + current.dist(successor)

		# check child is already in open list
		if successor in open and successor.g > current.g:
			break

		# child is not in open list
		print("moving current node {0} to open".format(successor))
		open.append(successor)
		successor.parent = current

	print("Open list:")
	print(*open)
	print("Closed list:")
	print(*closed)

print("\n### Search loop exited after {0} iterations ###".format(iteration_counter))
print("\nOptimal path  to goal state 1: ")
print(g1.backtrack())
print("\nOptimal path to goal state 2: ")
print(g2.backtrack())