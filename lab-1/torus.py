# ------------------------------------------------------------------------------
#
#	Lab 1 part 1
#
#   Torus
#
#	Danilin I.V.
# 
# ------------------------------------------------------------------------------

import gmsh
import sys
from math import *
import vtk

def floor(num,mod):
	return (num // mod) * mod

def mod(num,mod):
	return num%mod

gmsh.initialize()


gmsh.model.add("t1")

lc = 0.5

PI = 3.1415926 

# Geometry of "toroidal polyhedron"
N = 34 
M = 24 

NM = N * M

R = 15
r = 2
d = 1


# generating points of inner torus
circs = [[
	gmsh.model.geo.addPoint((R + r*cos(2*PI*m/M)) * cos(2*PI*n/N), 
                            (R + r*cos(2*PI*m/M)) * sin(2*PI*n/N), 
                            r * sin(2*PI*m/M), lc) 
	for m in range(M)] 
	for n in range(N)]

# Connect given points of circle by lines
def plot_circle(c):
	for i in range(M):
		gmsh.model.geo.addLine(c[i],c[(i + 1) % M])

# Connect two circles 
def merge_circles(c,c_):
	edges = [gmsh.model.geo.addLine(c[i],c_[(i)]) for i in range(M)]
	for i in range(M):
		gmsh.model.geo.addPlaneSurface(
			[gmsh.model.geo.addCurveLoop([c[i],edges[(i+1) % M],-c_[i],-edges[i]])])

# Genereting points of outer torus
circs2 = [[
	gmsh.model.geo.addPoint((R+(r+d)*cos(2*PI*m/M))*cos(2*PI*n/N), 
                            (R+(r+d)*cos(2*PI*m/M))*sin(2*PI*n/N), 
                            (r+d) * sin(2*PI*m/M), 
                            lc) 
	for m in range(M)] 
	for n in range(N)]

for c in circs:
	plot_circle(c)

for c in circs2:
	plot_circle(c)
	
for i in range(N):
	merge_circles(circs[i],circs[(i+1) % N])

for i in range(N):
	merge_circles(circs2[i],circs2[(i+1) % N])

gmsh.model.geo.addVolume([
    gmsh.model.geo.addSurfaceLoop((
        [-(i+1) for i in range(NM)] + [(1+i+NM) for i in range(NM)]))])

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(3)

gmsh.write("tor.msh")

gmsh.fltk.run()

#gmsh.finalize()



