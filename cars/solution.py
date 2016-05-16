import numpy as np
import math
import sys
def p(delta, n):
	result = delta ** n / math.factorial(n)
	result *= math.e ** ( -delta )
	return result
def mine(cars, min_action, max_action, gamma, reps):
	Psn = np.zeros((5, cars + 1))
	for q in range(2, 5):
		for r in range(cars + 1):
			Psn[q][r] = p(np.float64(q), np.float64(r))
		Psn[q][cars] += (1 - Psn[q].sum())
	P = np.zeros((cars + 1, cars + 1, max_action - min_action + 1, cars + 1, cars + 1))
	mP = np.zeros((2, max_action - min_action + 1, cars + 1, cars + 1))
	R = np.zeros((cars + 1, cars + 1, max_action - min_action + 1, cars + 1, cars + 1))
	mR = np.zeros((2, max_action - min_action + 1, cars + 1, cars + 1))
	for action in range(min_action, max_action + 1):
		for pt in range(cars + 1):
			for w in range(cars + 1):
				for z in range(cars + 1):
					if pt >= action:
						n1 = min(cars, max(0, pt-w-action) + z)		
						n2 = min(cars, max(0, pt-w-action) + z)
						wyp = min(pt - action, w)
						mP[0][action][pt][n1] += Psn[3][w] * Psn[3][z]
						mP[1][-action][pt][n2] += Psn[4][w] * Psn[2][z]
						mR[0][action][pt][n1] += (-20.0 * abs(action) + 100.0 * wyp) * Psn[3][w] * Psn[3][z]
						mR[1][-action][pt][n2] += 100.0 * wyp * Psn[4][w] * Psn[2][z]						
	mR[mP != 0] /= mP[mP != 0]
	for y0 in range(cars + 1):
		for x0 in range(cars + 1):
			for action in range(min_action, max_action + 1):
				for y1 in range(cars + 1):
					for x1 in range(cars + 1):
						P[y0][x0][action][y1][x1] += mP[0][action][y0][y1] * mP[1][action][x0][x1]
						R[y0][x0][action][y1][x1] += mR[0][action][y0][y1] + mR[1][action][x0][x1]
	Q = np.zeros((cars + 1, cars + 1, max_action - min_action + 1))
	times = 0
	result = np.zeros((cars + 1, cars + 1))
	prev_result = np.zeros((cars + 1, cars + 1))
	while True:
		Q1 = np.zeros((cars + 1, cars + 1, max_action - min_action + 1))
		for y0 in range(cars + 1):
			for x0 in range(cars + 1):
				for action in range(min_action, max_action + 1):				
					for y1 in range(cars + 1):
						for x1 in range(cars + 1):
							Q1[y0][x0][action] += P[y0][x0][action][y1][x1] * (R[y0][x0][action][y1][x1] + gamma * Q[y1, x1].max())
		Q = Q1
		result = np.argmax(Q, axis=2)
		if (result == prev_result).all():
			times += 1
		else:
			times = 0		
		if times == reps:
			break		
		prev_result = result
	for y in range(len(result)):
		for x in range(len(result[y])):
			if result[y][x] > 5:
				sys.stdout.write(str(result[y][x] - max_action + min_action - 1))
			else:
				sys.stdout.write(str(result[y][x]))
			sys.stdout.write(" ")
		sys.stdout.write("\n")
mine(20, -5, 5, 0.9, 10)
