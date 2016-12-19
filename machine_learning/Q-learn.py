import numpy as np
import random

####################################
# function


def init_zero(x, y):
    return 0*(x+y)


def init_zero3(x, y ,z):
    return 0*(x+y+z)


def select_action(state):
    qmax = max(state)
    max_num = 0
    max_list = []
    for i in range(4):
        if state[i] == qmax:
            max_num = max_num + 1
            max_list.append(i)
    return max_list[random.randint(0, max_num-1)]

####################################
# init for zero
maze_reward = np.fromfunction(init_zero, (10, 9))

# wall = -1
for i in (0, 9):
    for j in range(9):
        maze_reward[i][j] = -1

for i in (0, 8):
    for j in range(9):
        maze_reward[j][i] = -1

templist = [[2, 2], [2, 6], [2, 7], [3, 2], [3, 6], [6, 3], [6, 7], [7, 3], [8, 3]]
for i, j in templist:
    maze_reward[i][j] = -1

# target=10
maze_reward[8][6] = 10

print("the maze is:")
print(maze_reward)


#########################################
# state init
state_reward = np.fromfunction(init_zero3, (10, 9, 4))
# Active = 4, Row = 10, Column = 9

state_init = [1, 1]
state = state_init[:]

active = 0
active_list = [[0, 1], [0, -1], [1, 1], [1, -1]]
active_back = {"0": 1, "1": 0, "2": 3, "3": 2}
# active_list = [x-plus, x-minus, y-plus, y-minus]

alpha = 0.5
gamma = 0.9
random_prob = 0.2

trail_max = 1000
step_max = 100

#########################################
print("Q-learing start")

i = 0
while i < trail_max:
    print("turn", i+1)
    state_next = state[:]
    active_pre = random.randint(0, 2)
    j = 0
    while j < step_max:
        # active select
        while True:
            # random_prob% random OR select Q-max active
            if random.random() < random_prob:
                active = random.randint(0, 3)
            else:
                active = select_action(state_reward[state[0]][state[1]])

            # don't back
            if active != active_back[str(active_pre)]:
                break

        # move
        state_next[(active_list[active][0])] += active_list[active][1]
        active_pre = active

        reward = maze_reward[state_next[0]][state_next[1]]
        Q_max = max(state_reward[state[0]][state[1]])
        state_reward[state[0]][state[1]][active] = (1-alpha)*state_reward[state[0]][state[1]][active] + alpha*(reward + gamma*Q_max)

        if reward > 0:
            print("form", state, "to", state_next)
            print("target!")
            state = state_init[:]
            break

        elif reward < 0:
            print("form", state, "to", state_next)
            print("crash!")
            state = state_init[:]
            break

        else:
            print("form", state, "to", state_next)
            state = state_next[:]

        j += 1
    i += 1

print("Q-learning END")

print(state_reward)
