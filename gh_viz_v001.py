import rhinoscriptsyntax as rs

outlnX = [rs.AddLine(pts[0],pts[1]),rs.AddLine(pts[2],pts[3]),rs.AddLine(pts[4],pts[5]),rs.AddLine(pts[6],pts[7])]
outlnY = [rs.AddLine(pts[0],pts[3]),rs.AddLine(pts[1],pts[2]),rs.AddLine(pts[4],pts[6]),rs.AddLine(pts[5],pts[7])]
outlnZ = [rs.AddLine(pts[0],pts[4]),rs.AddLine(pts[1],pts[5]),rs.AddLine(pts[2],pts[6]),rs.AddLine(pts[3],pts[7])]

plane_xy = sub_x + sub_y + (sub_z + 1)
plane_xz = sub_x + (sub_y + 1) + sub_z
plane_yz = (sub_x + 1) + sub_y + sub_z

ptsZ = []
#subdivX = rs.DivideCurve(outlnX[0],x)
for i in outlnZ:
    ptsZ.append(rs.DivideCurve(i,sub_z))

linesY = []

for i in range(len(ptsZ[0])):
    linesY.append(rs.AddLine(ptsZ[0][i],ptsZ[2][i]))
    linesY.append(rs.AddLine(ptsZ[1][i],ptsZ[3][i]))



ptsY = []
for i in linesY:
    ptsY.append(rs.DivideCurve(i,sub_y))




linesX = []

for i in range(0,len(ptsY)-1,2):
    for j in range(len(ptsY[i])):
        linesX.append(rs.AddLine(ptsY[i][j],ptsY[i+1][j]))



ptsX = []
for i in linesX:
    ptsX.append(rs.DivideCurve(i,sub_x))

a = [i for j in ptsX for i in j]

index_x = 0
index_y = 1
index_z = 2


pts3D = [ptsX[i:i+(sub_y+1)] for i in range(0,len(ptsX),(sub_y+1))]

print ptsX[index_y][index_x]

print pts3D[index_z][index_y][index_x]

pts3D = zip(*pts3D)

for i,row in enumerate(pts3D):
    pts3D[i] = zip(*row)

pts3D = zip(*pts3D)

print pts3D[index_x][index_y][index_z]

facesXY = []
for i in range(sub_z):
    for j in range(sub_y+1):
        for k in range(sub_x+1):
            f = [(k,j,i),(k+1,j,i),(k+1,j+1,i),(k,j+1,i)]
#            f = [(k,j,i),(k+1,j,i),(k+1,j+1,i),(k,j+1,i)]
            facesXY.append(f)
#    for j in range(len(ptsY[i])-1):
#        for k in range(len(ptsZ)):
##            f = [ptsY[i][j],ptsY[i+1][j],ptsY[i+1][j+1],ptsY[i][j+1]]
#            f = [(i,j,k),(i+1,j,k),(i+1,j+1,k),(i,j+1,k)]

print facesXY,len(facesXY)
#print facesXY
print test
#test = [1,1,1,1,0,0,0,0,0,0,0,0]
#print facesXY[1]
b = []
for i,v in enumerate(test):
    if v == 1:
        p = []
        for coord in facesXY[i]:
            print coord[0], coord[1],coord[2]
            p.append(pts3D[coord[0]][coord[1]][coord[2]])
        print p
        b.append(rs.AddSrfPt(p))

#print b
#b = rs.AddSrfPt([a[n],a[n+(sub_y+1)],a[n+(sub_x+1)],a[n+1]])