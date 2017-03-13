__author__ = 'ccruz'
import numpy as np
import random
from random import uniform
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.path import Path


class CA():
    #Generates and updates, using a rule set 'r', a 1D CA of size n,
    #defined by the input of an initial condition 's'
    def __init__(self,rule,init_states,o):
        def make_ruleset(n):
            #Takes a rule number (n) and transforms it into a rule set
            r = np.zeros(8, dtype = np.int)
            rule_string = bin(n)[2:]
            rev_rule_string = rule_string[::-1]
            for i in range(len(rev_rule_string)):
                r[i] = (int(rev_rule_string[i]))
            return r
        self.ruleset = make_ruleset(rule)
        self.sts = init_states
        self._sts = init_states
        self.gens = 0
        # self.time = t
        self.orientation = o

    def __repr__(self):
        return '%s' % (self.sts)

    def __getitem__(self,i):
        return self.sts[i]

    def __len__(self):
        return len(self.sts)

    def checkNeighboursX(self):
        #check neighbours (end_cells loop around)
        self.neighbourhood = np.ndarray(shape = self.sts.shape, dtype=object)
        for i in range(len(self.sts)):
            for j in range(len(self.sts[i])):
                #First element
                if j < 1:
                    n = [self.sts[i][len(self.sts[i])-1],self.sts[i][j],self.sts[i][j+1]]
                    n_str = ''.join(str(e) for e in n)
                    self.neighbourhood[i,j] = n_str
                #Middle elements
                elif 0 < j < (len(self.sts[i])-1):
                    n = [self.sts[i][j-1],self.sts[i][j],self.sts[i][j+1]]
                    n_str = ''.join(str(e) for e in n)
                    self.neighbourhood[i,j] = n_str
                #Last element
                elif j == (len(self.sts[i])-1):
                    n = [self.sts[i][j-1],self.sts[i][j],self.sts[i][0]]
                    n_str = ''.join(str(e) for e in n)
                    self.neighbourhood[i,j] = n_str
        return self.neighbourhood

    def checkNeighboursY(self):
        #check neighbours (end_cells loop around)
        self.neighbourhood = np.ndarray(shape = self.sts.shape, dtype=object)
        for i in range(len(self.sts)):
            for j in range(len(self.sts[i])):
                #First element
                if i < 1:
                    n = [self.sts[len(self.sts)-1][j],self.sts[i][j],self.sts[i+1][j]]
                    n_str = ''.join(str(e) for e in n)
                    self.neighbourhood[i,j] = n_str
                #Middle elements
                elif 0 < i < (len(self.sts)-1):
                    n = [self.sts[i-1][j],self.sts[i][j],self.sts[i+1][j]]
                    n_str = ''.join(str(e) for e in n)
                    self.neighbourhood[i,j] = n_str
                #Last element
                elif i == (len(self.sts)-1):
                    n = [self.sts[i-1][j],self.sts[i][j],self.sts[0][j]]
                    n_str = ''.join(str(e) for e in n)
                    self.neighbourhood[i,j] = n_str
        return self.neighbourhood

    def nextGen(self, n):
        self.newSts = np.zeros(shape = n.shape, dtype=np.int)
        for i in range(len(n)):
            for j in range(len(n[i])):
                self.newSts[i,j] = self.ruleset[int(n[i,j],2)]
        return self.newSts

    def update(self):
        self.gens+=1
        if self.orientation == 'x':
            self.checkNeighboursX()
            # self.nextGen(self.neighbourhood)
        elif self.orientation == 'y':
            self.checkNeighboursY()
            # self.nextGen(self.neighbourhood)
        self.nextGen(self.neighbourhood)
        self.sts = self.newSts
        return self.sts
    #
    # def run(self):
    #     self.history = []
    #     self.history.append(self.sts)
    #     for i in range(self.time):
    #         u = self.update()
    #         self.history.append(u)
    #     self.hist_record = np.asarray(self.history)
    #     self.sts = self._sts
    #     return self.hist_record


class Tile2D:
    #  locations defined as:
    #  d     2     c
    #  -------------
    #  |           |
    # 3|  center   |1
    #  |           |
    #  -------------
    #  a     0     b
    def __init__(self, xcentre, ycentre, configuration):
        p = 0.02
        self.conf = reversed(configuration)
        self.a = (xcentre-.5,ycentre-.5)
        self.b = (xcentre+.5,ycentre-.5)
        self.c = (xcentre+.5,ycentre+.5)
        self.d = (xcentre-.5,ycentre+.5)
        self.abcd = [self.a,self.b,self.c,self.d]
        # self.r0 = [[self.a[0]-p,self.a[1]-p],[self.b[0]-p,self.b[1]+p],[self.b[0]+p,self.b[1]+p],[self.a[0]-p,self.a[1]+p]]
        # self.r1 = [[self.b[0]-p,self.b[1]-p],[self.b[0]+p,self.b[1]-p],[self.c[0]+p,self.c[1]+p],[self.c[0]-p,self.c[1]+p]]
        # self.r2 = [[self.c[0]+p,self.c[1]+p],[self.d[0]-p,self.d[1]+p],[self.d[0]-p,self.d[1]-p],[self.c[0]+p,self.c[1]-p]]
        # self.r3 = [[self.d[0]-p,self.d[1]+p],[self.a[0]-p,self.a[1]-p],[self.a[0]+p,self.a[1]-p],[self.d[0]+p,self.d[1]+p]]

        # self.r0 = Rectangle((self.a[0]-p,self.a[1]-p),1+(2*p),2*p,angle=0.0,color='k')
        # self.r1 = Rectangle((self.b[0]+p,self.b[1]-p),1+(2*p),2*p,angle=90.0,color= 'k')
        # self.r2 = Rectangle((self.c[0]+p,self.c[1]+p),1+(2*p),2*p,angle=180.0,color= 'k')
        # self.r3 = Rectangle((self.d[0]-p,self.d[1]+p),1+(2*p),2*p,angle=270.0,color= 'k')

        # self.walls = []
        # if configuration[0] == 1:
        #     self.walls.append(self.r0)
        # if configuration[1] == 1:
        #     self.walls.append(self.r1)
        # if configuration[2] == 1:
        #     self.walls.append(self.r2)
        # if configuration[3] == 1:
        #     self.walls.append(self.r3)
        self.verts = []
        self.codes = []



    def return_tile2D(self):
        return 'poto'
        # for wall in range(len(self.walls)):
        #     return self.walls[wall]


class chromosome():
    def __init__(self, size):
        def generate_chr(s):
            chr = []
            for i in range((s[0]*(s[1]+1))+((s[0]+1)*s[1])):
                chr.append(random.randint(0,1))
            return chr
        self.chromosome = generate_chr(size)

    def __repr__(self):
        return '%s' % (self.chromosome)

    def __len__(self):
        return len(self.chromosome)

    def __getitem__(self,i):
        return self.chromosome[i]


### This class defines an individual for a GA population
class Individual(object):
    def __init__(self,size,probability = 0.5,ind = None):
        def chr(s,p):
            c = []
            for i in range(s):
                r = uniform(0,1)
                if r < p:
                    c.append(1)
                else:
                    c.append(0)
            return c
        self.xy = size[0]*size[1]*(size[2]+1)
        self.xz = size[0]*(size[1]+1)*size[2]
        self.yz = (size[0]+1)*size[1]*size[2]
        self.l = int(self.xy+self.xz+self.yz)
        self.p = probability
        self.s = size
#        self.r = radius
        if ind == None:
            self.c = chr(self.l,self.p)
        else:
            self.c = ind
        self.values = {}
        self.dom = []
        self.dom_by = []
        self.hd = None
    ###this function transforms a chromosome into a graph
    def graph(self):
        g = {}
        tot_cells = int(self.s[0]*self.s[1]*self.s[2])
        for cell in range(tot_cells):
            g[cell] = []
        for i in g.keys():
            z = int(i / (self.s[0] * self.s[1]))
            x = int(i%self.s[0])
            y = int((i/self.s[0])-(self.s[1]*z))
            bot = int((y*self.s[0])+x+(z*(self.s[0]*self.s[1])))
            top = int(bot + (self.s[0]*self.s[1]))
            front = int(self.xy + x + (y*(self.s[0]*self.s[2])) + (z*self.s[0]))
            back = int(front + (self.s[0]*self.s[2]))
            left = int(self.xy + self.xz + (x*(self.s[1]*self.s[2])) + y + (z*self.s[1]))
            right = int(left + (self.s[1]*self.s[2]))
#            print 'bot = ',bot,' y = ',y,' z = ',z
            if z > 0 and self.c[bot] == 0:
                g[i].append(i-(self.s[0]*self.s[1]))
            if z < (self.s[2]-1) and self.c[top] == 0:
                g[i].append(i+(self.s[0]*self.s[1]))
            if y > 0 and self.c[front] == 0:
                g[i].append(i-self.s[0])
            if y < (self.s[1]-1) and self.c[back] == 0:
                g[i].append(i+self.s[0])
            if x > 0 and self.c[left] == 0:
                g[i].append(i-1)
            if x < (self.s[0]-1) and self.c[right] == 0:
                g[i].append(i+1)
            g[i] = set(g[i])
        return g
    ###function to get coordinates for every bit in the chromosome
    def getCoord(self):
        pts = []
        for pos,i in enumerate(self.c):
            if pos < self.xy:
                x = (pos%self.s[0])
                y = ((pos//self.s[0])%self.s[1])
                z = (pos//(self.s[0]*self.s[1]))
            elif self.xy-1 < pos < (self.xy+self.xz):
                pos2 = pos - self.xy
                x = (pos2%self.s[0])
                y = (pos2//(self.s[0]*self.s[2]))
                z = ((pos2//self.s[0])%self.s[2])
            elif (self.xy+self.xz)-1 < pos < (self.xy+self.xz+self.yz):
                pos3 = pos - (self.xy+self.xz)
                x = (pos3 // (self.s[1]*self.s[2]))
                y = (pos3 % self.s[1])
                z = ((pos3 // self.s[1]) % self.s[2])
            pts.append((x,y,z))
        return pts
    ###Retreive the normal vector for each bit in the chromosome
    def getNormal(self,position):
        if position < self.xy:
            return (0,0,1)
        elif self.xy-1 < position < (self.xy+self.xz):
            return (0,1,0)
        elif (self.xy+self.xz)-1 < position < (self.xy+self.xz+self.yz):
            return (1,0,0)
#        return norm
    def getShell(self,plane):
        p = None
        shell = []
        coord = self.getCoord()
        if plane == 'xy':
            p = self.xy
            for pos, i in enumerate(self.c):
                if pos < p:
                    if coord[pos][2] == self.s[2]*self.r:
                        shell.append(pos)
        elif plane == 'xz':
            pp = self.xy
            p = self.xy+self.xz
            for pos, i in enumerate(self.c):
                if pp <= pos < p:
                    if coord[pos][1] == 0 or coord[pos][1] == self.s[1]:#*self.r:
                        shell.append(pos)
        elif plane == 'yz':
            pp = self.xy+self.xz
            p = self.xy+self.xz+self.yz
            for pos, i in enumerate(self.c):
                if pp <= pos < p:
                    if coord[pos][0] == 0 or coord[pos][0] == self.s[0]:#*self.r:
                        shell.append(pos)
        else:
            print "plane value has to be 'xy', 'xz' or 'yz'"
            return
        return shell
    ###Compares two individuals to check which one dominates
    def dominates(self, other, problem):
        dom = []
        if problem == 'min':
            for k in self.values.keys():
                if self.values[k] < other.values[k]:
                    dom.append(True)
                else:
                    dom.append(False)
        elif problem == 'max':
            for k in self.values.keys():
                if self.values[k] > other.values[k]:
                    dom.append(True)
                else:
                    dom.append(False)
        return bool(int(sum(dom)/len(self.values)))

    #TODO using self.clear()
    def clear_values(self):
        self.values = {}
        return self

    def __repr__(self):
        return '%s' % (self.c)
    def __iter__(self):
        return iter(self.c)
    def __getitem__(self,item):
        return self.c[item]
    def getLen(self):
        return(len(self.c))


