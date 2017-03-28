import rhinoscriptsyntax as rs

### These are the outlines of the overall shape
outlnX = [rs.AddLine(pts[0],pts[1]),rs.AddLine(pts[2],pts[3]),rs.AddLine(pts[4],pts[5]),rs.AddLine(pts[6],pts[7])]
outlnY = [rs.AddLine(pts[0],pts[2]),rs.AddLine(pts[1],pts[3]),rs.AddLine(pts[4],pts[6]),rs.AddLine(pts[5],pts[7])]
outlnZ = [rs.AddLine(pts[0],pts[4]),rs.AddLine(pts[1],pts[5]),rs.AddLine(pts[2],pts[6]),rs.AddLine(pts[3],pts[7])]

### Visualise outlines of shape
lines = outlnX+outlnY+outlnZ

###Global variables calculating the size of each plane (number of faces)
plane_xy = sub_x * sub_y * (sub_z + 1)
plane_xz = sub_x * (sub_y + 1) * sub_z
plane_yz = (sub_x * 1) + sub_y * sub_z

### subdivide vertical outlines by the number sub_z 
ptsZ = []
for i in outlnZ:
    ptsZ.append(rs.DivideCurve(i,sub_z))

### generate all the lines in y axis from sub_z
linesY = []
for i in range(len(ptsZ[0])):
    linesY.append(rs.AddLine(ptsZ[0][i],ptsZ[2][i]))
    linesY.append(rs.AddLine(ptsZ[1][i],ptsZ[3][i]))

### Subdivide all lines on y axis by subdivisions in y
ptsY = []
for i in linesY:
    ptsY.append(rs.DivideCurve(i,sub_y))

### generate all lines in x axis from sub_y
linesX = []
for i in range(0,len(ptsY)-1,2):
    for j in range(len(ptsY[i])):
        linesX.append(rs.AddLine(ptsY[i][j],ptsY[i+1][j]))

### subdivide lines on x axis by sub_X
ptsX = []
for i in linesX:
    ptsX.append(rs.DivideCurve(i,sub_x))

### Generate the 3D grid of points
pts3D = [ptsX[i:i+(sub_y+1)] for i in range(0,len(ptsX),(sub_y+1))]

### Flip matrix (these steps are mysterious)
pts3D = zip(*pts3D)

for i,row in enumerate(pts3D):
    pts3D[i] = zip(*row)

pts3D = zip(*pts3D)

### get the coordinates for the points on each face
### this is done using pointers rather than reorganising objects
### the pointers are used to search points within the pts3D list.
facesXY = []
for i in range(sub_z+1):
    for j in range(sub_y):
        for k in range(sub_x):
            f = [(k,j,i),(k+1,j,i),(k+1,j+1,i),(k,j+1,i)]
            facesXY.append(f)

facesXZ = []
for i in range(sub_z):
    for j in range(sub_y+1):
        for k in range(sub_x):
            f = [(k,j,i),(k+1,j,i),(k+1,j,i+1),(k,j,i+1)]
            facesXZ.append(f)

facesYZ = []
for i in range(sub_z):
    for j in range(sub_y):
        for k in range(sub_x+1):
            f = [(k,j,i),(k,j+1,i),(k,j+1,i+1),(k,j,i+1)]
            facesYZ.append(f)

###Testing
test = [1,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,
        0,0,0,0,0,0,
        0,0,0,0,0,0,
        0,0,0,0,0,0,
        0,0,0,0,0,1]

### Output of the test
b = []
for i,v in enumerate(test):
    if v == 1:
        if i < plane_xy:
            p = []
            for coord in facesXY[i]:
                p.append(pts3D[coord[0]][coord[1]][coord[2]])
            b.append(rs.AddSrfPt(p))
        elif i < (plane_xy+plane_xz):
            p = []
            for coord in facesXZ[i-plane_xy]:
                p.append(pts3D[coord[0]][coord[1]][coord[2]])
            b.append(rs.AddSrfPt(p))
        else:
            p = []
            for coord in facesYZ[i-(plane_xy+plane_xz)]:
                p.append(pts3D[coord[0]][coord[1]][coord[2]])
            b.append(rs.AddSrfPt(p))