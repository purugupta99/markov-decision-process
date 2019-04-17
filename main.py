from copy import deepcopy


def check_if_possible(i,j):
	if i < 0 or j < 0 or i >= n or j >= m:
		return False

	for wall in walls:
		if wall[0] == i and wall[1] == j:
			return False

	return True

def next_state(i,j):
	max_value = -1000
	
	value = "- "
	if check_if_possible(i+1,j):
		previous_best = max_value

		val = p_right*previous_util[i+1][j]

		if check_if_possible(i,j-1):
			val += p_left*previous_util[i][j-1]
		else:
			val += p_left*previous_util[i][j]

		if check_if_possible(i,j+1):
			val += p_left*previous_util[i][j+1]
		else:
			val += p_left*previous_util[i][j]

		val += step_reward
		max_value = max(max_value,val)
		if previous_best != max_value:
			value = "S"
	
	# print(max_value)


	if check_if_possible(i,j+1):
		previous_best = max_value

		val = p_right*previous_util[i][j+1]

		if check_if_possible(i+1,j):
			val += p_left*previous_util[i+1][j]
		else:
			val += p_left*previous_util[i][j]

		if check_if_possible(i-1,j):
			val += p_left*previous_util[i-1][j]
		else:
			val += p_left*previous_util[i][j]

		val += step_reward

		max_value = max(max_value,val)
		if previous_best != max_value:
			value = "E"

	# print(max_value)


	if check_if_possible(i-1,j):
		previous_best = max_value

		val = p_right*previous_util[i-1][j]

		if check_if_possible(i,j+1):
			val += p_left*previous_util[i][j+1]
		else:
			val += p_left*previous_util[i][j]

		if check_if_possible(i,j-1):
			val += p_left*previous_util[i][j-1]
		else:
			val += p_left*previous_util[i][j]

		val += step_reward

		max_value = max(max_value,val)
		if previous_best != max_value:
			value = "N"
	# print(max_value)


	if check_if_possible(i,j-1):
		previous_best = max_value
		
		val = p_right*previous_util[i][j-1]

		if check_if_possible(i+1,j):
			val += p_left*previous_util[i+1][j]
		else:
			val += p_left*previous_util[i][j]

		if check_if_possible(i-1,j):
			val += p_left*previous_util[i-1][j]
		else:
			val += p_left*previous_util[i][j]

		val += step_reward

		max_value = max(max_value,val)
		if previous_best != max_value:
			value = "W"

	
	Policy[i][j] = value

	return max_value


X = 40
tolerance = 0.01
discount_factor = 0.99
p_right = 0.8
p_left = 0.1
previous_best = -1


n,m = raw_input().split()
n = int(n)
m = int(m)


# m = raw_input()

reward = [raw_input().split() for y in range(n)]

reward = [[float(reward[y][x]) for x in range(m)] for y in range(n)]

utils = [[0 for x in range(m)] for y in range(n)]



# print(utils)
# print(reward)

# print(reward)

e,w = raw_input().split()
e = int(e)
w = int(w)

end_states = [raw_input().split() for x in range(e)]
end_states = [[int(end_states[y][x]) for x in range(2)] for y in range(e)]

for end in end_states:
	utils[end[0]][end[1]] = reward[end[0]][end[1]]

# print(reward)

walls = [raw_input().split() for x in range(w)]
walls = [[float(walls[y][x]) for x in range(2)] for y in range(w)]


start_x , start_y = raw_input().split()
start_x = float(start_x)
start_y = float(start_y)

step_reward = raw_input().split()
# print(step_reward[0])
step_reward = float(step_reward[0])

delta = float('Inf')

epoch = 0
previous_util = deepcopy(utils)
iter_i = -1
iter_j = -1

Policy = [["-" for x in range(m)] for y in range(n)]
while delta > tolerance*abs(previous_util[iter_i][iter_j]):
	previous_util = deepcopy(utils)
	# print(previous_util)

	delta = -100
	iter_i = -1
	iter_j = -1

	for i in range(n):
		for j in range(m):

			is_blocked = False

			for end in end_states:
				# print(end)
				if end[0] == i and end[1] == j:
					is_blocked = True
					break
			if is_blocked == True:
				continue
			
			for wall in walls:
				if wall[0] == i and wall[1] == j:
					is_blocked = True
					break
				
			if is_blocked == True:
				continue
			
			# print(is_blocked,i,j)
			value = next_state(i,j)
			# print(value)
			utils[i][j] = reward[i][j] + discount_factor*value

			# print("Updating: "+str(i)+","+str(j)+" "+str(utils[i][j]))

			delta = max(delta,abs(utils[i][j]-previous_util[i][j]))

			if delta == abs(utils[i][j]-previous_util[i][j]):
				iter_i = i
				iter_j = j
		
	if previous_util[iter_i][iter_j] != 0.0:
		print("Max_Error "+str(delta/abs(previous_util[iter_i][iter_j])))
	else:
		print("Max_Error: Infinity")

	# policy()

	for items in utils:
		for inner in items:
			print(round(inner,3)),
		print("")
	
	for items in Policy:
		print(items)
	
	print("")


	epoch += 1
	print("Iteration: " + str(epoch))
	print("x---x---x---x")
	print("")