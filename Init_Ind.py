from random import uniform

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
       # self.r = radius
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
        #TODO If there are 2 ture and 1 false, what do we want from this?
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