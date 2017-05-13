from random import randint, random, sample
import sys
import pickle
from Init_Ind import Individual

def walkability(ind):
    g = ind.graph()

    w = []
    for i in g.keys():
        z = i // (ind.s[0] * ind.s[1])
        x = i % ind.s[0]
        y = (i // ind.s[0]) - (ind.s[1] * z)
        pot = 4
        deg = 0
        if x == 0 or x == ind.s[0] - 1:
            pot -= 1
        if y == 0 or y == ind.s[1] - 1:
            pot -= 1
        if ind[i] == 1:
            if i + 1 in g[i] and ind[i + 1] == 1:
                deg += 1
            if i - 1 in g[i] and ind[i - 1] == 1:
                deg += 1
            if i + ind.s[0] in g[i] and ind[i + ind.s[0]] == 1:
                deg += 1
            if i - ind.s[0] in g[i] and ind[i - ind.s[0]] == 1:
                deg += 1
        w.append(float(deg) / pot)
    ar = sum(w) / len(g.keys())  #accessibility ratio (how much of the potential accessibility is reached)
    ind.values['walk'] = "%.3f" % ar
    return ind.values['walk']

def structure(ind):
    cols = []
    for i in range(int((ind.s[0] + 1) * (ind.s[1] + 1))):
        cols.append(0)
    for i, col in enumerate(cols):
        x = int(i % (ind.s[0] + 1))
        y = int(i // (ind.s[0] + 1))
        neigh = []  # right, front, left, back
        if x < ind.s[0]:  # right
            neigh.append(int(x + ind.xy + (y * (ind.s[0] * ind.s[2]))))
        if y < ind.s[1]:
            neigh.append(int(y + ind.xy + ind.xz + (x * (ind.s[1] * ind.s[2]))))
        if x > 0:
            neigh.append(int(x - 1 + ind.xy + (y * (ind.s[0] * ind.s[2]))))
        if y > 0:
            neigh.append(int(y - 1 + ind.xy + ind.xz + (x * (ind.s[1] * ind.s[2]))))
        z = 0
        while z < int(ind.s[2]):
            n = []
            for j in neigh:
                if j < (ind.xy + ind.xz):
                    n.append(ind[j + (z * int(ind.s[0]))])
                else:
                    n.append(ind[j + (z * int(ind.s[1]))])
            if sum(n) > 0:
                cols[i] += 1
            z += 1
    for i in range(len(cols)):
        if cols[i] == ind.s[2]:
            cols[i] = 1
        else:
            cols[i] = 0
    ind.values['structure'] = "%.3f" % (sum(cols) / float(len(cols)))
    return ind.values['structure']
# def structure(ind):
#     cols = []
#     for i in range(int((ind.s[0] + 1) * (ind.s[1] + 1))):
#         cols.append(0)
#     for i, col in enumerate(cols):
#         x = int(i % (ind.s[0] + 1))
#         y = int(i // (ind.s[0] + 1))
#         neigh = []  # right, front, left, back
#         if x < ind.s[0]:  # right
#             neigh.append(int(x + ind.xy + (y * (ind.s[0] * ind.s[2]))))
#         if y < ind.s[1]:
#             neigh.append(int(y + ind.xy + ind.xz + (x * (ind.s[1] * ind.s[2]))))
#         if x > 0:
#             neigh.append(int(x - 1 + ind.xy + (y * (ind.s[0] * ind.s[2]))))
#         if y > 0:
#             neigh.append(int(y - 1 + ind.xy + ind.xz + (x * (ind.s[1] * ind.s[2]))))
#         z = 0
#         while z < int(ind.s[2]):
#             n = []
#             for j in neigh:
#                 if j < (ind.xy + ind.xz):
#                     n.append(ind[j + (z * int(ind.s[0]))])
#                 else:
#                     n.append(ind[j + (z * int(ind.s[1]))])
#             if sum(n) > 0:
#                 cols[i] += 1
#             z += 1
#     for i in range(len(cols)):
#         if cols[i] == ind.s[2]:
#             cols[i] = 1
#         else:
#             cols[i] = 0
#
#     ind.values['structure'] = "%.3f" % (sum(cols) / float(len(cols)))
#     return ind.values['structure']

def hamming_dist(pop):
    for i, ind in enumerate(pop):
        hd = []
        for j, other in enumerate(pop):
            if i != j:
                dist = 0
                for b in range(int(ind.getLen())):
                    if ind[b] != other[b]:
                        dist += 1
                hd.append(float(dist) / ind.getLen())
        ind.hd = sum(hd) / (len(pop) - 1)
    return pop

def sort_pop_st(pop, problem):
    # new_pop is a list of pointers to the individuals in pop
    pop_ind = [i for i in range(len(pop))]  ###List of pointers to individuals in pop
    # fronts is the output list
    fronts = []
    dom = []
    dom_by = []
    for i, ind in enumerate(pop_ind):
        dom.append([])
        dom_by.append([])

        for j, other in enumerate(pop_ind):
            if ind != other:
                if pop[ind].dominates(pop[other], problem):
                    dom[i].append(other)
                if pop[other].dominates(pop[ind], problem):
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
        # in python3, the key has to be declared with sorted() function
        fronts[-1] = [i for (r, i) in sorted(zip(rank, fronts[-1]), reverse=True)]
        pop_ind = [i for i in pop_ind if i not in rem]
        for i in range(len(dom)):
            dom[i] = [j for j in dom[i] if j not in rem]
            dom_by[i] = [k for k in dom_by[i] if k not in rem]

    # fronts_ind = [pop[ind] for row in fronts for ind in row]
    ff = [[pop[i] for i in f] for f in fronts]
    return ff

def tournament(pop, p_len, problem):
    _pop = pop
    new_pop = []
    while len(new_pop) < p_len:
        r1 = randint(0, len(_pop) - 1)
        r2 = randint(0, len(_pop) - 1)
        ind = _pop[r1]
        other = _pop[r2]
        if not any([ind.dominates(other, problem), other.dominates(ind, problem)]):
            if ind.hd > other.hd:
                new_pop.append(ind)
                _pop.remove(ind)
            else:
                new_pop.append(other)
                _pop.remove(other)
        elif ind.dominates(other, problem):
            new_pop.append(ind)
            _pop.remove(ind)
        else:
            new_pop.append(other)
            _pop.remove(other)
    return new_pop


def mate(pop):
    new_pop = []
    ### This step makes the length of the population even
    if len(pop) % 2 == 1:
        new_pop.append(pop[0])
        del pop[0]
    ### Make a new list with the indices of the members of the population
    pop_i = [i for i in range(len(pop))]
    xy = pop[0].xy
    xz = xy + pop[0].xz
    while len(pop_i) > 0:
        parent1, parent2 = sample(pop_i,2)
        p0 = randint(0, xy)
        p1 = randint(xy, xz)
        p2 = randint(xy, xz)
        p3 = randint(xz, pop[parent1].getLen())
        p = sorted([p0, p1, p2, p3])
        ni1 = pop[parent1][:p[0]] + pop[parent2][p[0]:p[1]] + pop[parent1][p[1]:p[2]] + pop[parent2][p[2]:p[3]] + pop[parent1][p[3]:]
        ni2 = pop[parent2][:p[0]] + pop[parent1][p[0]:p[1]] + pop[parent2][p[1]:p[2]] + pop[parent1][p[2]:p[3]] + pop[parent2][p[3]:]
        new_ind1 = Individual(pop[0].s, pop[0].p, ni1)
        new_ind2 = Individual(pop[0].s, pop[0].p, ni2)
        new_pop.append(new_ind1)
        new_pop.append(new_ind2)
        pop_i.remove(parent1), pop_i.remove(parent2)
    return new_pop

def mutate(pop, prob):
    for ind in pop:
        for i,bit in enumerate(ind):
            r = random()
            if r < prob:
                ind.c[i] = abs(bit - 1)
    return pop

def get_json(pop):
    output = []
    for each in pop:
        ind_dict = {"graph": [], "values": {}}
        ind_dict["graph"] = list(each)
        ind_dict["values"] = each.values
        output.append(ind_dict)
    return output

def evolve(pop_size, ind_size, gens, problem, pop=[]):
    try:
        # print "the length of population is -> ", len(pop)
        gens = int(gens)
        pop_size = int(pop_size)
        # ind_size = eval(ind_size)
        print "the length of population is ", len(pop)
        while len(pop) < pop_size:
            pop.append(Individual(ind_size))

        print pop[1].l

        new_pop = pop
        for i in new_pop:
            walkability(i)
            structure(i)
        hamming_dist(new_pop)

        while gens > 0:
            ### sort population
            fronts = sort_pop_st(new_pop, problem)
            sorted_pop = [ind for front in fronts for ind in front]

            ### elite population
            elite_pop = []
            for ind in sorted_pop:
                if ind not in elite_pop and len(elite_pop) < int(len(new_pop) / 4):
                    elite_pop.append(ind)
            ### mating pool
            m_pool = tournament(sorted_pop, len(new_pop) - len(elite_pop), problem)

            ### operate on mating pool
            off_1 = mate(m_pool)
            offspring = mutate(off_1, 0.05)

            ### recompose population
            new_pop = elite_pop + offspring
            for ind in new_pop:
                ind.clear_values()
            ### re_evaluate new_pop
            for i in new_pop:
                walkability(i)
                structure(i)
            hamming_dist(new_pop)
            fronts2 = sort_pop_st(new_pop, problem)
            new_pop = [ind for front in fronts2 for ind in front]

            # print threading.current_thread().getName() +  "  Number %dth loop is done"%(gens)
            print "  Number %dth loop is done"%(gens)

            gens -= 1

        # output = pickle.dumps(new_pop[:10])
        output = pickle.dumps(new_pop)
        # print type(new_pop)
        return output
    except Exception as ex:
        print "evolve -> " , ex
        print "evolve -> " + str(sys.exc_traceback.tb_lineno)



if __name__ == '__main__':
    s = (2, 3, 4)
    evolve(50, s, 5, 'max')


