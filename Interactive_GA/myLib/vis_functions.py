__author__ = 'ccruz'
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from os import path
import functions
from matplotlib import colors

def plot_array_colours(array, label):
    #takes a 2D array and plots it as a mosaic of colours
    #using the values of the items
    cmap = plt.cm.get_cmap('gray',np.amax(array)*2)
    fig = plt.imshow(array, cmap = cmap, interpolation='none')
    # fig.set_cmap('Set1')
    plt.axis('tight')
    plt.title(label)
    # plt.axvline(x=(0),linewidth=1, color='w')
    ticks = np.arange(np.amax(array)+1)
    plt.colorbar(orientation='vertical', ticks = ticks)
    # plt.savefig(label+".png")
    plt.show()

def plot_array(arr, imsize,txt_on):
    ### Takes a 2D array and displays it as black lines on white background
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            flipped_arr = np.flipud(arr)
            name = flipped_arr[i][j]
            im = Image.open(path.dirname(__file__) + '/states/'+str(name)+'.png', mode="r")
            plt.imshow(im,interpolation="none", aspect='equal', extent=np.array([j, j+1, i, i+1])*(imsize))
            if txt_on == 'y':
                tx = Image.open(path.dirname(__file__) + '/states/txt'+str(name)+'.png', mode="r")
                plt.imshow(tx,interpolation="none", aspect='equal', extent=np.array([j, j+1, i, i+1])*(imsize))

def plot_graph(arr, imsize):
    ### Takes a 2D array and displays it as black lines on white background
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            flipped_arr = np.flipud(arr)
            names = []
            if flipped_arr[i][j]['links'][0] == '0':
                names.append('left')
            if flipped_arr[i][j]['links'][1] == '0':
                names.append('top')
            if flipped_arr[i][j]['links'][2] == '0':
                names.append('right')
            if flipped_arr[i][j]['links'][3] == '0':
                names.append('bottom')
            if len(names) == 0:
                names.append('none')
            for name in names:
                im = Image.open(path.dirname(__file__) + '/links/'+name+'.png', mode="r")
                plt.imshow(im,interpolation="none", aspect='equal', extent=np.array([j, j+1, i, i+1])*(imsize))
            # if txt_on == 'y':
            #     tx = Image.open(path.dirname(__file__) + '/states/txt'+str(name)+'.png', mode="r")
            #     plt.imshow(tx,interpolation="none", aspect='equal', extent=np.array([j, j+1, i, i+1])*(imsize))

### This function plots a graph differentiating its clusters
### by colour
def plot_graph_2(g,l_weight):
    clstrs = functions.clusters(g)
    clrs = colors.cnames.keys()
    col_pick = -1
    for c in clstrs:
        col_pick+=1
        if col_pick < len(clrs):
            clr = clrs[col_pick]
        else:
            clr = clrs[col_pick-len(clrs)]
        for sp in c:
            for ep in c[sp]:
                plt.plot([sp[1],ep[1]],[sp[0],ep[0]], lw = l_weight, color = clr, marker = 'o')

def plot_graph_3(g,l_weight,s):
    s2 = (s[0]+2,s[1]+2)
    clstrs = functions.clusters(g)
    clrs = colors.cnames.keys()
    col_pick = -1
    for c in clstrs:
        col_pick+=1
        if col_pick < len(clrs):
            clr = clrs[col_pick]
        else:
            clr = clrs[col_pick-len(clrs)]
        for a in c.keys():
            sp = (a%s2[0],a/s2[0])
            for b in c[a]:
                ep = (b%s2[0],b/s2[0])
                plt.plot([sp[0],ep[0]],[sp[1],ep[1]], lw = l_weight, color = clr, marker = 'o')


def plot_graph_4(g,l_weight,s):
    clstrs = functions.clusters(g)
    clrs = colors.cnames.keys()
    col_pick = -1
    for c in clstrs:
        col_pick+=1
        if col_pick < len(clrs):
            clr = clrs[col_pick]
        else:
            clr = clrs[col_pick-len(clrs)]
        for a in c.keys():
            sp = (a%s[0],a/s[0])
            for b in c[a]:
                ep = (b%s[0],b/s[0])
                plt.plot([sp[0],ep[0]],[sp[1],ep[1]], lw = l_weight, color = clr, marker = 'o')

def plot_walls(arr,l_weight,colour):
    dif = 0.5
    walls = functions.draw_walls(arr)
    for tile in walls:
        for wall in walls[tile]:
            sp = (tile[0]-dif+wall[0][0],tile[1]-dif+wall[0][1])
            ep = (tile[0]-dif+wall[1][0],tile[1]-dif+wall[1][1])
            plt.plot([sp[1],ep[1]],[sp[0],ep[0]],lw = 3, color = colour)

# Graphic representation of a chromosome as graph using its list of connected elements (con)
def plot_chromosome(con,s):
    s2 = (s[0]+2,s[1]+2)
    for pt in con:
        sp = pt[0]
        ep = pt[1]
        plt.plot([sp%s2[0],ep %s2[0]],[sp/s2[0],ep/s2[0]], lw = 1.5, color = 'k', marker = 'o')
    plt.xlim(-1,s2[0])
    plt.ylim(s2[1],-1)

# Graphic representation of a chromosome (ch) as a set of walls
def plot_chr_walls(ch,s):
    s2 = (s[0]+2,s[1]+2)
    for i in range(len(ch)):
        dif = 0.5
        sp = (0,0)
        ep = (0,0)
        if i < s[0]*(s[1]+1):
            sp = (i%s[0]+dif,i/s[0]+dif)
            ep = (sp[0]+1,sp[1])
        else:
            j = i-(s[0]*(s[1]+1))
            sp = (j/s[1]+dif,j%s[1]+dif)
            ep = (sp[0],sp[1]+1)
        if ch[i] == 1:
            plt.plot([sp[0],ep[0]],[sp[1],ep[1]], lw = 5, color = 'grey')
        plt.xlim(-.2,s2[0]-.8)
        plt.ylim(s2[1]-.8,-.2)

def plot_chr_walls2(ch,s,l=1.0):
    for i in range(len(ch)):
        dif = l/2
        sp = (0,0)
        ep = (0,0)
        if i < s[0]*(s[1]+1):
            x = i%s[0]
            y = i/s[0]
            sp = (x-dif,y-dif)
            ep = (x+dif,y-dif)
        else:
            j = i-(s[0]*(s[1]+1))
            x = j/s[1]
            y = j%s[1]
            sp = (x-dif,y-dif)
            ep = (x-dif,y+dif)
        if ch[i] == 1:
            plt.plot([sp[0],ep[0]],[sp[1],ep[1]], lw = 5, color = 'grey')
        plt.xlim((-1*l),s[0])
        plt.ylim(s[1],(-1*l))

### 3D printing starts here
def plot_graph3D(g,lw,s):
    fig = plt.figure(figsize=(s[0]*2,s[1]*2))
    ax = fig.add_subplot(111, projection = '3d')
    clust = functions.clusters(g)
    clrs = colors.cnames.keys()
    col_pick = -1
    for c in clust:
        col_pick+=1
        for a in c.keys():
            if col_pick < len(clrs):
                clr = clrs[col_pick]
            else:
                clr = clrs[col_pick-len(clrs)]
            z = a / (s[0] * s[1])
            x = a % s[0]
            y = (a / s[0]) - (s[1] * z)
            sp = (x,y,z)
            for b in c[a]:
                z = b / (s[0] * s[1])
                x = b % s[0]
                y = (b / s[0]) - (s[1] * z)
                ep = (x,y,z)
                ax.plot([sp[0],ep[0]],[sp[1],ep[1]],[sp[2],ep[2]],lw=lw, color = clr, marker='o')
            ax.grid(b=None)
            ax.patch.set_facecolor('grey')
            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')