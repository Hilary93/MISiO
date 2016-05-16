import random
import time
from action import Action

def find_max(self):
	hist_max = .0
	hist_x = .0
	hist_y = .0
	for y in range(self.height):
		for x in range(self.width):
			if self.hist[y][x] >= hist_max:
				hist_max = self.hist[y][x]
				hist_x = x
				hist_y = y
	return hist_y, hist_x

class Agent:
	def __init__(self, p, pj, pn, height, width, areaMap):
		self.p = p
		self.pj = pj
		self.pn = pn
		self.height = height
		self.width = width
		self.map = areaMap

		# create smooth histogram
		self.hist = [[0 for x in range(self.width)] for y in range(self.height)]
		smooth = 1.0 / (height * width)
		for y in range(self.height):
			for x in range(self.width):
				self.hist[y][x] = smooth

		self.exit_y = 0
		self.exit_x = 0
		# find exit
		for y in range(self.height):
			for x in range(self.width):
				if self.map[y][x] == 'W':
					self.exit_y = y
					self.exit_x = x

	def sense(self,sensor):
		self.hist[self.exit_y][self.exit_x] = .0
		sum_hist = .0
		# try to predict the position
		for y in range(self.height):
			for x in range(self.width):
				if sensor == True:
					if self.map[y][x] == 'J':
						self.hist[y][x] *= self.pj
					else:
						self.hist[y][x] *= self.pn
				else:
					if self.map[y][x] == 'J':
						self.hist[y][x] *= 1 - self.pj
					else:
						self.hist[y][x] *= 1 - self.pn
				sum_hist += self.hist[y][x]
		# normalization
		for y in range(self.height):
			for x in range(self.width):
				self.hist[y][x] /= sum_hist

	def move(self):
		y_coord, x_coord = find_max(self)

		action = Action.DOWN

		yBey = y_coord > self.exit_y
		xBex = x_coord > self.exit_x
		yND = abs(y_coord - self.exit_y) > self.height / 2
		xND = abs(x_coord - self.exit_x) > self.width / 2
		disY = .0
		disX = .0
		if yBey:
			disY = y_coord - self.exit_y
		else:
			disY = self.exit_y - y_coord

		if xBex:
			disX = x_coord - self.exit_x
		else:
			disX = self.exit_x - x_coord

		# make move
		if disY >= disX:
			if yBey and yND:
				action = Action.DOWN
			elif yBey != yND:
				action = Action.UP
			else:
				action = Action.DOWN
		else:
			if xBex and xND:
				action = Action.RIGHT
			elif xBex != xND:
				action = Action.LEFT
			else:
				action = Action.RIGHT

		tmp_hist = [[0 for x in range(self.width)] for y in range(self.height)]

		# shift histogram
		for y in range(self.height):
			for x in range(self.width):
				prop_opt = (self.p) * self.hist[y][x]
				prop_pes = ((1-self.p)/4) * self.hist[y][x]

				tmp_hist[y][x] += prop_pes

				if action == Action.DOWN:
					tmp_hist[(y+1) % self.height][x                 ] += prop_opt
					tmp_hist[(y+2) % self.height][x                 ] += prop_pes
					tmp_hist[(y+1) % self.height][(x+1) % self.width] += prop_pes
					tmp_hist[(y+1) % self.height][x-1               ] += prop_pes
				elif action == Action.UP:
					tmp_hist[y-1                ][x                 ] += prop_opt
					tmp_hist[y-2                ][x                 ] += prop_pes
					tmp_hist[y-1                ][x-1               ] += prop_pes
					tmp_hist[y-1                ][(x+1) % self.width] += prop_pes
				elif action == Action.LEFT:
					tmp_hist[y                  ][x-1               ] += prop_opt
					tmp_hist[y                  ][x-2               ] += prop_pes
					tmp_hist[y-1                ][x-1               ] += prop_pes
					tmp_hist[(y+1) % self.height][x-2               ] += prop_pes
				else:
					tmp_hist[y                  ][(x+1) % self.width] += prop_opt
					tmp_hist[y                  ][(x+2) % self.width] += prop_pes
					tmp_hist[(y+1) % self.height][(x+1) % self.width] += prop_pes
					tmp_hist[y-1                ][(x+1) % self.width] += prop_pes
		self.hist = tmp_hist
		return action

	def histogram(self):
		return self.hist
