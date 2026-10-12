import numpy as np
import matplotlib.pyplot as plt


def calcEfield(xrng: list, yrng: list, npts, Q: list):
    x1, x2 = xrng
    y1, y2 = yrng
    xpts = npts
    ypts = npts
    dx = (x2 - x1) / xpts
    dy = (y2 - y1) / ypts
    x, y = np.linspace(x1, x2, xpts), np.linspace(y1, y2, ypts)
    x, y = np.meshgrid(x, y)
    Ex = np.zeros((xpts, ypts))
    Ey = np.zeros((xpts, ypts))

    k = 9 * 10 ** 9
    for i in range(xpts):
        for j in range(ypts):
            xp, yp = x[i][j], y[i][j]
            for q in Q:
                deltaX = xp - q[0]
                deltaY = yp - q[1]

                distance = (deltaX ** 2 + deltaY ** 2) ** 0.5

                E = (k * q[2]) / (distance ** 2)
                Ex[i][j] += E * (deltaX / distance)
                Ey[i][j] += E * (deltaY / distance)
    return x, y, Ex, Ey


Q = []
numpts = 100
for qy in range(-5,5,1):
    Q.append((0, qy, 1))
xrange = [-5, 5]
yrange = [-5, 5]
x, y, Ex, Ey = calcEfield(xrange, yrange, numpts, Q)
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.scatter([q[0] for q in Q], [q[1] for q in Q], c='red', s=[abs(q[2]) * 50 for q in Q], zorder=1)
for q in Q: ax.text(q[0] + 0.1, q[1] - 0.3, '{} unit'.format(q[2]), color='black', zorder=2)
ax.streamplot(x, y, Ex, Ey, linewidth=1, density=1.5, zorder=0)

plt.title('Electrostatic Field Simulation')
plt.show()

# Confirm with Gauss's Law
#  we are going to integrate ("add up") around the edges of a box. Might as well use the entire box
#
# # contour 1 starts at 5,5, with -5<x<5 and y=5
# checkval1 = 0
# for a in range(1, len(Ey)):
#     tempval = ((Ey[-1][a] + Ey[-1][a - 1]) / 2) * dx
#     #tempval = ((abs(Ey[a][-1]) + abs(Ey[a - 1][-1])) / 2) * dx
#     #tempval = Ey[-1][a]
#     checkval1 = checkval1 + tempval
#
# # x=-5 and 5 < y < -5
# checkval2 = 0
# for b in range(1,len(Ex)):
#     tempval = ((Ex[b][0] + Ex[b - 1][0]) / 2) * dy
#     #tempval = ((abs(Ex[0][b]) + abs(Ex[0][b - 1])) / 2) * dy
#     #tempval = Ex[b][0]
#     checkval2 = checkval2 + tempval
# checkval2 = -checkval2  # negative because normal vector points in -xhat direction
#
# # (-5,5)  -5<x<5, y=-5
# checkval3 = 0
# for c in range(1, len(Ey)):
#     tempval = ((Ey[0][c] + Ey[0][c - 1]) / 2) * dx
#     #tempval = ((abs(Ey[c][0]) + abs(Ey[c - 1][0])) / 2) * dx
#     #tempval = Ey[0][c]
#     checkval3 = checkval3 + tempval
# checkval3 = -checkval3  # negative because normal vector points in -yhat direction
#
# # (5,-5) x=5, -5<y<5
# checkval4 = 0
# for d in range(1, len(Ex)):
#     tempval = ((Ex[d][-1] + Ex[d - 1][-1]) / 2) * dy
#     #tempval = ((abs(Ex[-1][d]) + abs(Ex[-1][d - 1])) / 2) * dy
#     #tempval = Ex[d][-1]
#     checkval4 = checkval4 + abs(tempval)
#
# intval = (8.854 * 10 ** (-12)) * (checkval1 + checkval2 + checkval3 + checkval4) /(2*np.pi)
# #intval =  (checkval1 + checkval2 + checkval3 + checkval4) /(1)
#
# print(intval)


# dipole
# create a line charge
# create another shape
