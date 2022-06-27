'''
------------------------------------
Assignment 5 - EE2703 
Name: Jineeth N (EE20B051)
Date: 06/03/2022
------------------------------------
'''

# Importing the required modules.
import sys
from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3

# Initializing the required parameters with their default values.
Niter = 1500
Ny = 25
Nx = 25


# The above parameters can also be given through the commmand line.
if len(sys.argv) > 1:
    Nx = sys.argv[1]
    Ny = sys.argv[2]
    Niter = sys.argv[3] 

n = arange(Niter)

# Creating the respective matrices and initializing them also.
phi = np.zeros((Ny, Nx))

rng = 0.5\
x = np.linspace(-rng, rng, Nx)
y = np.linspace(-rng, rng, Ny)
X, Y = meshgrid(x, -y)

#print(Y)
ii = where(((X * X) + (Y * Y)) <= (0.35 * 0.35))
phi[ii] = 1.0

# Plotting of the initial potential contour.
xp = x[ii[0]]
yp = y[ii[1]]
figure(1, figsize=(6, 6))
plot(xp, yp, "ro", label="V = 1")
xlim(-0.5, 0.5)
ylim(-0.5, 0.5)
xlabel(r"X")
ylabel(r"Y")
title("Initial Potential Contour")
grid()
legend()

# The below piece of code is to perform the iteration and to calculate the error in the potential.
errors = np.zeros((Niter, 1))
for k in range(Niter):
    oldphi = phi.copy()
    phi[1:-1, 1:-1] = (1/4) * (phi[1:-1, 0:-2] + phi[1:-1, 2:] + phi[0:-2, 1:-1] + phi[2:, 1:-1])

    # These lines will set the proper boundary conditions.
    phi[1:-1, 0] = phi[1:-1, 1]
    phi[1:-1, -1] = phi[1:-1, -2]
    phi[0, 1:-1] = phi[1, 1:-1]
    phi[ii] = 1.0
 #Maximum error between old and new potential values in the matrix  
    errors[k] = (abs(phi - oldphi)).max()

# Plotting of error vs iteration in semilog.
figure(2, figsize=(6, 6))
semilogy(n, errors)
xlabel(r"Iteration", fontsize=15)
ylabel(r"Error", fontsize=15)
title("Error vs iteration")
grid()

# Plotting of error vs iteration in loglog.
figure(3, figsize=(6, 6))
loglog(n, errors)
xlabel(r"Iteration", fontsize=15)
ylabel(r"Error", fontsize=15)
title("Error vs iteration in a loglog plot")
grid()

# Plotting of error vs iteration above 500 in semilog .
figure(4, figsize=(6, 6))
semilogy(n[500:], errors[500:])
xlabel(r"Iteration", fontsize=15)
ylabel(r"Error", fontsize=15)
title("Error vs iteration above 500")
grid()

# The exponent part of the error values can be got using the below piece of code.
y1 = log(errors)
yfit = lstsq(c_[np.ones(Niter - 0), arange(Niter - 0)], y1, rcond=None)[0]
#fitting a straight line in log scale and calculating actual values in normal scale
a, b = exp(yfit[0]), yfit[1]     #returns the values of log A and B
y2 = log(errors[500:])
yfit = lstsq(c_[np.ones(Niter - 500), arange(500, Niter)], y2, rcond=None)[0]
a_500, b_500 = exp(yfit[0]), yfit[1]


# Plotting of actual and expected error (above 500 iterations) in semilog.
figure(5, figsize=(6, 6))
semilogy(n[500:], errors[500:], label="Actual")
semilogy(n[500:], a_500 * exp(b_500 * n[500:]), label="Fit1")
xlabel(r"Iteration", fontsize=15)
ylabel(r"Error", fontsize=15)
title("Expected vs actual error (>500 iterations)")
grid()
legend()

# Plotting of the actual and expected error in semilog.
figure(6, figsize=(6, 6))
semilogy(n, errors, label="Actual")
semilogy(n, a * exp(b * n), label="Fit2")
xlabel(r"Iteration", fontsize=15)
ylabel(r"Error", fontsize=15)
title("Expected vs actual error ")
grid()
legend()



# Plotting of the contour of phi (potential).
figure(7, figsize=(6, 6))
contourf(X, Y, phi)
plot(xp, yp, "ro", label="V = 1")
xlabel(r"X")
ylabel(r"Y")
title("Contour plot of potential")
grid()
legend()

# Plotting the surface plots of phi (potential).
fig1=figure(8, figsize=(6, 6))
ax = p3.Axes3D(fig1)
xlabel(r"X")
ylabel(r"Y")
title("The 3-D surface plot of the potential")
surf = ax.plot_surface(X, Y, phi, rstride=1, cstride=1, cmap=cm.jet)

# The current density vectors can be calulated as shown.
Jx = np.zeros((Ny, Nx))
Jy = np.zeros((Ny, Nx))
Jx = 0.5 * (phi[1:-1, 0:-2] - phi[1:-1, 2:])
Jy = 0.5 * (phi[2:, 1:-1] - phi[0:-2, 1:-1])

# plotting of the current vector plot along with the potential.
figure(9, figsize=(6, 6))
quiver(X[1:-1, 1:-1], Y[1:-1, 1:-1], Jx, Jy)  
plot(xp, yp, "ro")
xlabel(r"X")
ylabel(r"Y")
title("The vector plot of the current flow")

show()
