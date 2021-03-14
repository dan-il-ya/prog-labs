from fenics import *
import time

T = 1.5            # final time
num_steps = 150     # number of time steps
dt = T / num_steps # time step size

# Create mesh and define function space
nx = ny = 30
mesh = RectangleMesh(Point(-2, -2), Point(2, 2), nx, ny)
V = FunctionSpace(mesh, 'P', 1)

# Define boundary condition
def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, interpolate(Expression('(x[1]+2)',
                 degree=2),V), boundary)

# Define initial value
u_0 = interpolate(Expression('0',
                 degree=2),V)
u_n = interpolate(u_0, V)

# Define variational problem
u = TrialFunction(V)
v = TestFunction(V)

f = Constant(0)

chi = interpolate(
    Expression('0.1 + D*c*(abs(x[0] + 1/D)-abs(x[0]-1/D)+2/D)',
                 degree=2,c=10,D=10), V)

F = 1/chi*u*v*dx + dt*dot(grad(u), grad(v))*dx - (1/chi*u_n + dt*f)*v*dx
a, L = lhs(F), rhs(F)

# Create VTK file for saving solution
vtkfile = File('heat_gaussian/solution.pvd')

# Time-stepping
u = Function(V)
t = 0

for n in range(num_steps):

    # Update current time
    t += dt

    # Compute solution
    solve(a == L, u, bc)

    # Save to file and plot solution
    vtkfile << (u, t)
    plot(u)

    # Update previous solution
    u_n.assign(u)