import random

###############################
# function


def func_variation(li, var_rate):
    if random.random() < var_rate:
        li[random.randint(0, 9)] = random.randint(0, 9)
    else:
        return li
    return func_variation(li, var_rate)

# setting
children_num = 500
next_num = 50
length = 10
generation = 300

cross_rate = 0.5
variation_rate = 0.5

range_children_num = range(children_num)
###############################
# random create first generation children
print("Create first generation children")
children_next = []
child = []
for i in range_children_num:
    for j in range(length):
        child.append(random.randint(0, 9))
    children_next.append(child)
    child = []

print(children_next)
print("Create END")
generation_num = 0
while generation_num < generation:

    ###############################
    # cross - variation - fit
    children = children_next[:]

    # mating
    children_next = []
    while len(children_next) < children_num:
        for i in range(next_num):
            # cross
            if random.random() < cross_rate:
                point = random.randint(1, length-2)
                rud_num = random.randint(0, next_num-1)
                children[i][point:], children[rud_num][point:] = children[rud_num][point:], children[i][point:]
            # variation
            children[i] = func_variation(children[i], variation_rate)
            # add
            children_next.append(children[i])

            if len(children_next) == children_num:
                break

    children = children_next[:]
    '''
    # cross
    for i in range_children_num:
        # exchange
        if random.random() < cross_rate:
            point = random.randint(1, 8)
            children[i][point:], children[i + random.randint(-i, children_num - i - 1)][point:] = children[i + random.randint(-i, children_num - i - 1)][point:], children[i][point:]
    # variation
    for i in range_children_num:
        children[i] = func_variation(children[i], variation_rate)
    '''
    # fit?
    sum_fit = 0
    sum_children = []
    # compute fit of creature
    for i in range_children_num:
        sum_children.append(sum(children[i]))

    #########################################
    # another fit method (by sort)
    sum_children_sort = sum_children[:]
    sum_children_sort.sort()

    children_next = []
    for i in range(next_num):
        for j in range_children_num:
            if sum_children[j] == sum_children_sort[-i-1]:
                children_next.append(children[i])
                break
    #########################################
    '''
    # fit method (by roulette)
    fit = []
    # fit[i][0] = fit; fit[i][1] = fit_rate; fit[i][2] = sum_fit_rate
    for i in range_children_num:
        fit.append([])

    sum_fit = 0
    for i in range_children_num:
        fit[i].append(sum(children[i]))
        sum_fit += fit[i][0]

    sum_fit = float(sum_fit)

    sum_rate = 0
    for i in range_children_num:
        fit[i].append(float(fit[i][0])/sum_fit)
        sum_rate += fit[i][1]
        fit[i].append(sum_rate)

    # roulette
    children_next = []
    while len(children_next) < next_num:
        rnd = random.random()
        for i in range_children_num:
            if fit[i][2] >= rnd:
                children_next.append(children[i])
                break
    ###############################
    '''
    generation_num += 1

print("END generation:")
print(children_next)
