
'''
------------------------------------
Assignment 3 - EE2703 
Name: Jineeth N (EE20B051)
Date: 18/02/2022
------------------------------------
'''

import matplotlib.pyplot as plt
from numpy import *
import scipy.special as sp


# Actual function.
def g(t, A, B):
    return A * sp.jn(2, t) + B * t


A_p = 1.05
B_p = -0.105
k_c = 9

# Reading the  data from "fitting.dat"
data = loadtxt("fitting.dat")

# storing X coordinates .
t = data[:, 0]

# computing the actual functional values.
y0 = g(t, A_p, B_p)
stdev = logspace(-1, -3, k_c)
n, m = data.shape  #It returns the dimensions of the array

# Plotting given noisy data along with the actual function.
def plot_figure0():
    plt.figure(0)
    for i in range(1, 10):
        plt.plot(t, data[:, i], label="σ=%.3f" % stdev[i - 1])
    plt.plot(t, y0, label="True Value", color="black", linewidth=3)
    plt.title("Dataset plots", size=20)
    plt.grid(True)
    plt.legend()
    plt.xlabel(r"$t$", size=20)
    plt.ylabel(r"$f(t)+n$", size=20)


# Plotting data in the first column with error bars.
def plot_figure1():
    plt.figure(1)
    plt.plot(t, y0, label="True Value", color="black", linewidth=3)
    plt.errorbar(t[::5], data[:, 1][::5], stdev[0], fmt="ro", label="Noise")
    plt.grid(True)
    plt.legend()
    plt.title("Data with Error Bars", size=20)
    plt.xlabel(r"$t", size=20)
    plt.ylabel(r"$f(t)+n", size=20)

#plotting contour of RMS errors.
def plot_figure2():
    plt.figure(2)
    Contour = plt.contour(X, Y, E, 25)
    plt.clabel(Contour, Contour.levels[:5], inline=1)
    plt.grid(True)
    plt.plot(A_p,B_p,'ro')
    plt.text(A_p,B_p,"exact location")
    plt.title("Contour Plot", size=20)
    plt.xlabel(r"$A", size=20)
    plt.ylabel(r"$B", size=20)


# plotting the error in estimataion of A and B w.r.t standard deviation.
def plot_figure3():
    plt.figure(3)
    plt.plot(stdev, Ea, label="Aerr", marker="o", linestyle="dashed")
    plt.plot(stdev, Eb, label="Berr", marker="o", linestyle="dashed")
    plt.title("Variation of Error with Noise", size=20)
    plt.grid(True)
    plt.legend()
    plt.xlabel("Noise standard deviation", size=20)
    plt.ylabel("MS error", size=20)


# plotting the error in estimataion of A and B w.r.t standard deviation in log scale.
def plot_figure4():
    plt.figure(4)
    plt.loglog(stdev, Ea, "ro", label="Aerr" )
   # plt.errorbar(stdev, Ea, std(Ea), fmt="ro")
    #plt.errorbar(stdev , Ea , std(Ea) , fmt='ro')
    plt.loglog(stdev, Eb, "go", label="Berr")
    #plt.errorbar(stdev, Eb, std(Eb), fmt="go")
    #plt.errorbar(stdev , Eb , std(Eb) ,fmt='go')
    plt.title("Variation of Error with Noise", size=20)
    plt.grid(True)
    plt.legend()
    plt.xlabel("Noise standard deviation", size=20)
    plt.ylabel("MS error", size=20)





# Calculating the M matrix asked in Q.6.
M = zeros((n, 2))
for i in range(n):
    M[i] = (sp.jn(2, t[i]), t[i])

A0 = array([A_p, B_p])
y = dot(M, A0)

if array_equal(y, g(t, A_p, B_p)):
    print("Both solutions for Q.6 are equal.")
else:
    print("Both solutions for Q.6 are not equal.")

#  To calculate the mean squared error for different values of A and B.
dx = 0.1
A = array([dx * i for i in range(0, 21)])
dx = 0.01
B = array([-0.2 + dx * i for i in range(0, 21)])
E = zeros((21, 21))

for i in range(21):
    for j in range(21):
        for k in range(n):
            E[i][j] += ((g(t[k], A[i], B[j]) - data[:, 1][k]) ** 2) / n


# Generating meshgrid.
X, Y = meshgrid(A, B)


# Fitting curve and calculating  A and B coefficients.
Ea = zeros((k_c, 1))
Eb = zeros((k_c, 1))

for j in range(k_c):
    AB = linalg.lstsq(M, data[:, j + 1], rcond=None)
    Ea[j], Eb[j] = abs(AB[0][0] - A0[0]), abs(AB[0][1] - A0[1])

plot_figure0()
plot_figure1()
plot_figure2()
plot_figure3()
plot_figure4()


# This command will display all the graphs defined above.
plt.show()