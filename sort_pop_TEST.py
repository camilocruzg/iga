from IGA_Python3.Individual import Individual as ind
from operator import itemgetter, attrgetter
import time


test_pop = [ind((10,9,8)) for i in range(500)]

### This is the new sorting algorithm
def sort_pop(pop, problem):
    # new_pop is a list of pointers to the individuals in pop
    pop_ind = [i for i in range(len(pop))] ###List of pointers to individuals in pop
    # fronts is the output list
    fronts = []
    while len(pop_ind) > 0:
        fronts.append([])
        dom = []
        dom_by = []
        #Evaluate dominance
        # start_dom = time.time()
        for i,ind in enumerate(pop_ind):
            dom.append([])
            dom_by.append([])
            for j,other in enumerate(pop_ind):
                if ind != other:
                    if pop[ind].getDominates(pop[other], problem):
                        dom[i].append(other)
                    if pop[other].getDominates(pop[ind], problem):
                        dom_by[i].append(other)
            pop[ind].dom = dom[i]
            pop[ind].dom_by = dom_by[i]
        rem = []
        for i in pop_ind:
            if len(pop[i].dom_by) == 0:
                fronts[-1].append(i)
                rem.append(i)
        rank = []
        for i in fronts[-1]:
            rank.append(len(pop[i].dom))
        #in python3, the key has to be declared with sorted() function
        fronts[-1] = [i for (r, i) in sorted(zip(rank, fronts[-1]), key = itemgetter(0),reverse=True)]
        # new_pop = [i for j, i in enumerate(new_pop) if j not in rem]
        pop_ind = [i for i in pop_ind if i not in rem]
        # print(fronts, sorted(rank, reverse=True), rem, pop_ind )
    return fronts

### This is the original sorting algorithm
# def sort_pop_b(pop, problem):
#     new_pop = pop
#     fronts = []
#     while len(new_pop) > 0:
#         fronts.append([])
#         dom = []
#         dom_by = []
#         #Evaluate dominance
#         for i, ind in enumerate(new_pop):
#             dom.append([])
#             dom_by.append([])
#             for j, other in enumerate(new_pop):
#                 if i != j:
#                     if ind.getDominates(other, problem):
#                         dom[i].append(j)
#                     if other.getDominates(ind, problem):
#                         dom_by[i].append(j)
#             ind.dom = dom[i]
#             ind.dom_by = dom_by[i]
#         rem = []
#         for j, ind in enumerate(new_pop):
#             if len(ind.dom_by) == 0:
#                 fronts[-1].append(ind)
#                 rem.append(j)
#         rank = []
#         for i in fronts[-1]:
#             rank.append(len(i.dom))
#         #in python3, the key has to be declared with sorted() function
#         fronts[-1] = [i for (r, i) in sorted(zip(rank, fronts[-1]), key = itemgetter(0),reverse=True)]
#         new_pop = [i for j, i in enumerate(new_pop) if j not in rem]
#     return fronts

### This is the latest static approach, where the output is a list of pointers towards the individuals in the population
### I still have to understand how to use this approach in the evolutionary function
def sort_pop_st(pop, problem):
    # new_pop is a list of pointers to the individuals in pop
    pop_ind = [i for i in range(len(pop))] ###List of pointers to individuals in pop
    # fronts is the output list
    fronts = []
    dom = []
    dom_by = []
    for i, ind in enumerate(pop_ind):
        dom.append([])
        dom_by.append([])
        for j, other in enumerate(pop_ind):
            if ind != other:
                if pop[ind].getDominates(pop[other], problem):
                    dom[i].append(other)
                if pop[other].getDominates(pop[ind], problem):
                    dom_by[i].append(other)
        pop[ind].dom = dom[i]
        pop[ind].dom_by = dom_by[i]
    while len(pop_ind) > 0:
        fronts.append([])
        rem = []
        for i in range(len(pop_ind)):
            if len(dom_by[pop_ind[i]]) == 0:
                fronts[-1].append(pop_ind[i])
                rem.append(pop_ind[i])
        rank = []
        for i in fronts[-1]:
            rank.append(len(dom[i]))
        #in python3, the key has to be declared with sorted() function
        fronts[-1] = [i for (r, i) in sorted(zip(rank, fronts[-1]), key = itemgetter(0),reverse=True)]
    #     # new_pop = [i for j, i in enumerate(new_pop) if j not in rem]
        pop_ind = [i for i in pop_ind if i not in rem]
        for i in range(len(dom)):
            dom[i] = [j for j in dom[i] if j not in rem]
            dom_by[i] = [k for k in dom_by[i] if k not in rem]
    #     # print(fronts, sorted(rank, reverse=True), rem, pop_ind )
    return fronts


### Eval pop
start_eval = time.time()
def getWalkability(ind):
    var_graph = ind.getGraph()
    w = []
    for i in var_graph.keys():
        ###Get the coordinates for each node in the graph
        z = i // (ind.size[0] * ind.size[1])
        x = i % ind.size[0]
        y = (i // ind.size[0]) - (ind.size[1] * z)
        ###Initialise potential connections pot: potential connections
        pot = 4
        ###Initialise counter for degree distribution deg: counter for actual connections
        deg = 0
        ###adjust pot for edges and corners
        if x == 0 or x == ind.size[0] - 1:
            pot -= 1
        if y == 0 or y == ind.size[1] - 1:
            pot -= 1
        ###count deg for each node that has a horizontal panel
        if ind[i] == 1:
            if i + 1 in var_graph[i] and ind[i + 1] == 1:
                deg += 1
            if i - 1 in var_graph[i] and ind[i - 1] == 1:
                deg += 1
            if i + ind.size[0] in var_graph[i] and ind[i + ind.size[0]] == 1:
                deg += 1
            if i - ind.size[0] in var_graph[i] and ind[i - ind.size[0]] == 1:
                deg += 1
        ###
        w.append(float(deg) / pot)
    ar = sum(w) / len(var_graph.keys())  # accessibility ratio (how much of the potential accessibility is reached
    ind.values['walk'] = ar
    return ind.values['walk']

def structure(ind):
    cols = []
    for i in range(int((ind.size[0] + 1) * (ind.size[1] + 1))):
        cols.append(0)
    for i, col in enumerate(cols):
        x = int(i % (ind.size[0] + 1))
        y = int(i // (ind.size[0] + 1))
        neigh = []  #right, front, left, back
        if x < ind.size[0]:  #right
            neigh.append(int(x + ind.xy + (y * (ind.size[0] * ind.size[2]))))
        if y < ind.size[1]:
            neigh.append(int(y + ind.xy + ind.xz + (x * (ind.size[1] * ind.size[2]))))
        if x > 0:
            neigh.append(int(x - 1 + ind.xy + (y * (ind.size[0] * ind.size[2]))))
        if y > 0:
            neigh.append(
                int(y - 1 + ind.xy + ind.xz + (x * (ind.size[1] * ind.size[2]))))
        z = 0
        while z < int(ind.size[2]):
            n = []
            for j in neigh:
                if j < (ind.xy + ind.xz):
                    n.append(ind[j + (z * int(ind.size[0]))])
                else:
                    n.append(ind[j + (z * int(ind.size[1]))])
            if sum(n) > 0:
                cols[i] += 1
            z += 1
    for i in range(len(cols)):
        if cols[i] == ind.size[2]:
            cols[i] = 1
        else:
            cols[i] = 0
    ind.values['structure'] = float(sum(cols) / len(cols))
    return ind.values['structure']

for ind in test_pop:
    getWalkability(ind)
    structure(ind)
finish_eval = time.time()

print('Eval:',finish_eval-start_eval)
### Tests

start = time.time()
test02 = sort_pop(test_pop,'max')
check = time.time()
print('Old approach takes',check-start, 'seconds')
test03 = sort_pop_st(test_pop,'max')

end = time.time()
print('New approach takes',end-check,'seconds')

# for i in test02:
#     print(i)
# for i in test03:
#     print(i)

