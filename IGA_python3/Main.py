import Individual
from random import randint, random
from operator import itemgetter, attrgetter


def getEvolution(pop_size, ind_size, generation, problem, pop=[]):
    _gens = generation
    for i in range(pop_size):
        pop.append(Individual.Individual(ind_size))
    print ('the population is ', len(pop), 'individuals')

    ### evaluate population
    new_pop = pop
    for i in new_pop:
        getWalkability(i)
        structure(i)
    hamming_dist(new_pop)

    ### Pareto front for each generation will be stored in this list
    pareto_fronts_out = []
    ### Values for individuals in pareto front for each gen will be stored in this list
    values_out = []
    ### Full pop will be stored here
    full_pop_out = []

    ### Evolution starts here
    while generation > 0:
        ### sort population
        fronts = sort_pop(new_pop, problem)
        sorted_pop = [ind for front in fronts for ind in front]

        ### elite population
        e_pop = []
        for ind in sorted_pop:
            if ind not in e_pop and len(e_pop) < int(len(new_pop) / 4):
                e_pop.append(ind)

        ### mating pool
        m_pool = tournament(sorted_pop, len(new_pop) - len(e_pop), problem)

        ### operate on mating pool
        off_1 = mate(m_pool)
        offspring = mutate(off_1, 0.05)

        ### recompose population
        new_pop = e_pop + offspring
        for ind in new_pop:
            ind.clear_values()

        ### re_evaluate new_pop
        for i in new_pop:
            getWalkability(i)
            structure(i)
        hamming_dist(new_pop)
        fronts2 = sort_pop(new_pop, problem)
        pFront = fronts[0]
        pFront2 = []
        for ndf in pFront:
            if ndf not in pFront2:
                pFront2.append(ndf)
        pareto_fronts_out.append(pFront2)
        values_out.append([i.values for i in pFront2])
        srtd_pop = [ind for front in fronts2 for ind in front]
        full_pop_out.append(srtd_pop)
        generation -= 1
    print ('there are ', len(full_pop_out), 'in the pareto front')
    print (pareto_fronts_out)
    print (values_out)
    print (full_pop_out)
    prompt1 = input('Terminate? (Y/N): ')
    if prompt1 == 'Y':
        exit()
        # print 'there are ', len(full_pop_out), 'in the pareto front'
        # return pareto_fronts_out, values_out, full_pop_out
    elif prompt1 == 'N':
        # _pop_size = pop_size
        # _ind_size = ind_size
        # _gens = gens
        # _problem = problem
        #TODO using try/except statement
        prompt2 = input('seed population (enter list of indice up to %s): '
                            % (len(full_pop_out[0]) - 1))
        seed_pop = [
            full_pop_out[-1][seeded_ind]
            for seeded_ind in [int(ii) for ii in prompt2.split(',')]
        ]
        print ('you have selected', len(seed_pop), 'individuals to seed next gen')
        return getEvolution(pop_size, ind_size, _gens, problem, seed_pop)
    else:
        return 'You have failed!'
#
# if __name__ == "__main__":
#     evolve(100, (2,3,4), 10, 'max')

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

def sort_pop(pop, problem):
    new_pop = pop
    fronts = []
    while len(new_pop) > 0:
        fronts.append([])
        dom = []
        dom_by = []
        #Evaluate dominance
        for i, ind in enumerate(new_pop):
            dom.append([])
            dom_by.append([])
            for j, other in enumerate(new_pop):
                if i != j:
                    if ind.getDominates(other, problem):
                        dom[i].append(j)
                    if other.getDominates(ind, problem):
                        dom_by[i].append(j)
            ind.dom = dom[i]
            ind.dom_by = dom_by[i]
        rem = []
        for j, ind in enumerate(new_pop):
            if len(ind.dom_by) == 0:
                fronts[-1].append(ind)
                rem.append(j)
        rank = []
        for i in fronts[-1]:
            rank.append(len(i.dom))
        fronts[-1] = [i for (r, i) in sorted(zip(rank, fronts[-1]), key = itemgetter(0),reverse=True)]
        new_pop = [i for j, i in enumerate(new_pop) if j not in rem]
    return fronts


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

def hamming_dist(pop):
    for i, ind in enumerate(pop):
        hd = []
        for j, other in enumerate(pop):
            if i != j:
                dist = 0
                for b in range(int(ind.getLen())):
                    if ind[b] != other[b]:
                        dist += 1
                hd.append(dist / ind.getLen())
        ind.hd = sum(hd) / (len(pop) - 1)
    return pop

def tournament(pop, p_len, problem):
    _pop = pop
    new_pop = []
    while len(new_pop) < p_len:
        r1 = randint(0, len(_pop) - 1)
        r2 = randint(0, len(_pop) - 1)
        ind = _pop[r1]
        other = _pop[r2]
        if ind.getDominates(other,
                         problem) and other.getDominates(ind, problem) is False:
            if ind.hd > other.hd:
                new_pop.append(ind)
                _pop.remove(ind)
            else:
                new_pop.append(other)
                _pop.remove(other)
        elif ind.getDominates(other, problem):
            new_pop.append(ind)
            _pop.remove(ind)
        else:
            new_pop.append(other)
            _pop.remove(other)
    return new_pop


### Mating
def mate(pop):
    selected = []
    new_pop = []
    ni1 = None
    ni2 = None
    while len(new_pop) < len(pop):
        if len(pop) % 2 == 1:
            new_pop.append(pop[0])
            selected.append(0)
            del pop[0]
        else:
            r1 = randint(0, len(pop) - 1)
            r2 = randint(0, len(pop) - 1)
            if r1 in selected:
                r1 = randint(0, len(pop) - 1)
            elif r1 not in selected:
                selected.append(r1)
            if r2 in selected:
                r2 = randint(0, len(pop) - 1)
            elif r2 not in selected:
                selected.append(r2)
            p1 = randint(0, pop[r1].getLen() - 1)
            p2 = randint(0, pop[r1].getLen() - 1)
            p = sorted([p1, p2])
            ni1 = pop[r1][:p[0]] + pop[r2][p[0]:p[1]] + pop[r1][p[1]:]
            ni2 = pop[r2][:p[0]] + pop[r1][p[0]:p[1]] + pop[r2][p[1]:]
        new_ind1 = Individual.Individual(pop[0].size, pop[0].prob, ni1)
        new_ind2 = Individual.Individual(pop[0].size, pop[0].prob, ni2)
        new_pop.append(new_ind1)
        new_pop.append(new_ind2)
    return new_pop


### Mutation
def mutate(pop, prob):
    for ind in pop:
        for bit in ind:
            r = random()
            if r < prob:
                bit = abs(bit - 1)
    return pop

for i in getEvolution(100, (2,3,4), 10, 'max')[1]:
    print (i)
