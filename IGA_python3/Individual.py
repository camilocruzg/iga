from random import uniform

class Individual(object):
    '''Randomly generate the initial individual

    Args:
        size -- The 3-Dimensional data respectively indicating length, width and height. (e.g. (x,y,z))
        prob -- The likelihood of generating 1 or 0. (default 0.5)
        ind -- The input object (default None)

    Return:
        An randomly generated object named Individual, which is a binary bits representation of one architectural form.
        For example,in terms of size [1,2,3], what this class would return is:
            [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1]

    Raise:

    '''
    def __init__(self,size,prob = 0.5,ind = None):
        self.xy = size[0] * size[1] * (size[2] + 1)
        self.xz = size[0] * (size[1] + 1) * size[2]
        self.yz = (size[0] + 1) * size[1] * size[2]
        self.str_length = int(self.xy + self.xz + self.yz)
        self.prob = prob
        self.size = size
        self.values = {}
        self.dom = []
        self.dom_by = []
        self.hd = None
        self.chr = []
        for i in range(self.str_length):
            if uniform(0, 1) < prob:
                self.chr.append(1)
            else:
                self.chr.append(0)

    def getGraph(self):
        var_graph = {}
        tot_cells = int(self.size[0] * self.size[1] * self.size[2])
        for cell in range(tot_cells):
            var_graph[cell] = []
        for i in var_graph.keys():
            z = int(i / (self.size[0] * self.size[1]))
            x = int(i % self.size[0])
            y = int((i / self.size[0]) - (self.size[1] * z))
            bot = int((y * self.size[0]) + x + (z * (self.size[0] * self.size[1])))
            top = int(bot + (self.size[0] * self.size[1]))
            front = int(self.xy + x + (y * (self.size[0] * self.size[2])) + (z * self.size[0]))
            back = int(front + (self.size[0] * self.size[2]))
            left = int(self.xy + self.xz + (x * (self.size[1] * self.size[2])) + y + (z * self.size[1]))
            right = int(left + (self.size[1] * self.size[2]))
            if z > 0 and self.chr[bot] == 0:
                var_graph[i].append(i - (self.size[0] * self.size[1]))
            if z < (self.size[2] - 1) and self.chr[top] == 0:
                var_graph[i].append(i + (self.size[0] * self.size[1]))
            if y > 0 and self.chr[front] == 0:
                var_graph[i].append(i - self.size[0])
            if y < (self.size[1] - 1) and self.chr[back] == 0:
                var_graph[i].append(i + self.size[0])
            if x > 0 and self.chr[left] == 0:
                var_graph[i].append(i - 1)
            if x < (self.size[0] - 1) and self.chr[right] == 0:
                var_graph[i].append(i + 1)
            var_graph[i] = set(var_graph[i])
        return var_graph


    def getCoord(self):
        var_coord = []
        for i in range(len(self.chr)):
            if i < self.xy:
                x = (i % self.size[0])
                y = ((i // self.size[0]) % self.size[1])
                z = (i // (self.size[0] * self.size[1]))
            elif self.xy-1 < i < (self.xy+self.xz):
                i = i - self.xy
                x = (i % self.size[0])
                y = (i // (self.size[0] * self.size[2]))
                z = ((i // self.size[0]) % self.size[2])
            elif (self.xy+self.xz)-1 < i < (self.xy+self.xz+self.yz):
                i = i - (self.xy+self.xz)
                x = (i // (self.size[1] * self.size[2]))
                y = (i % self.size[1])
                z = ((i // self.size[1]) % self.size[2])
            var_coord.append((x,y,z))
        return var_coord
# print (Individual((2,3,4)).getCoord())


    def initialState(self,position):
        if position < self.xy:
            return (0,0,1)
        elif self.xy-1 < position < (self.xy+self.xz):
            return (0,1,0)
        elif (self.xy+self.xz)-1 < position < (self.xy+self.xz+self.yz):
            return (1,0,0)

    def getShell(self,plane):
        # p = None
        var_shell = []
        the_coord = self.getCoord()
        try:
            if plane is "xy":
                for i in range(self.xy):
                    #TODO
                    if the_coord[i][2] == self.size[2]:# *self.r
                        var_shell.append(i)
            elif plane is "xz":
                for i in range(self.xy, self.xy + self.xz):
                    if the_coord[i][1] == 0 or the_coord[i][1] == self.size[1]:
                        var_shell.append(i)
            elif plane is "yz":
                for i in range(self.xy + self.xz,self.xy + self.xz + self.yz):
                    if the_coord[i][0] == 0 or the_coord[i][0] == self.size[0]:
                        var_shell.append(i)
            else:
                print("plane value has to be 'xy', 'xz' or 'yz'")
        finally:
            return var_shell
# print (Individual((2,3,4)).getShell("yz"))

    def getDominates(self, other, problem):
        var_dom = []
        if problem is "min":
            for i in self.values.keys():
                if self.values[i] < other.values[i]:
                    var_dom.append(True)
                else:
                    var_dom.append(False)
        elif problem is "max":
            for i in self.values.keys():
                if self.values[i] > other.values[i]:
                    var_dom.append(True)
                else:
                    var_dom.append(False)
        return bool(int(sum(var_dom) / len(self.values)))

    def clear_values(self):
        self.values = {}
        return self

    def __repr__(self):
        return '%s' % (self.chr)

    def __iter__(self):
        return iter(self.chr)

    def __getitem__(self, item):
        return self.chr[item]

    def getLen(self):
        return (len(self.chr))

# print(Individual((2,2,2)).getGraph())
