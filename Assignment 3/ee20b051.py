import matplotlib.pyplot as plt
from numpy import *
import scipy.special as sp


# Defining the actual function.
def g(t, A, B):
    return A * sp.jn(2, t) + B * t


A_p = 1.05
B_p = -0.105
k_c = 9

# Loading data from "fitting.dat"
data = loadtxt("fitting.dat")

# Extracting time and the first set of data.
t = data[:, 0]

# Calculating the actual set of functional values.
y0 = g(t, A_p, B_p)
stdev = logspace(-1, -3, k_c)
n, m = data.shape

# This will print the actual plt.plot along with nine other noisy plots.
plt.figure(0)
for i in range(1, 10):
    plt.plot(t, data[:, i], label="σ=%.3f" % stdev[i - 1])
plt.plot(t, y0, label="True Value", color="black", linewidth=3)
plt.title("plt.Figure 0", size=20)
plt.grid(True)
plt.legend()
plt.xlabel(r"$t", size=20)
plt.ylabel(r"$f(t)+n", size=20)

# This will plt.plot the error plt.plot in the first set of data as compared to the actual plt.plot.
plt.figure(1)
plt.plot(t, y0, label="True Value", color="black", linewidth=3)
plt.errorbar(t[::5], data[:, 1][::5], 0.1, fmt="ro", label="Noise")
plt.grid(True)
plt.legend()
plt.title("Data with Error Bars", size=20)
plt.xlabel(r"$t", size=20)
plt.ylabel(r"$f(t)+n", size=20)

# Calculating the M matrix asked in Q.6.
M = zeros((n, 2))
for i in range(n):
    M[i] = (sp.jn(2, t[i]), t[i])

A0 = array([A_p, B_p])
y = dot(M, A0)

if allclose(y, g(t, A_p, B_p)):
    print("Both solutions for Q.6 are equal.")
else:
    print("Both solutions for Q.6 are not equal.")

# The below lines of code is used to calculate the mean squared error for different values of A and B.
dx = 0.1
A = array([dx * i for i in range(0, 21)])
dx = 0.01
B = array([-0.2 + dx * i for i in range(0, 21)])
E = zeros((21, 21))

for i in range(21):
    for j in range(21):
        for k in range(n):
            E[i][j] += ((g(t[k], A[i], B[j]) - data[:, 1][k]) ** 2) / n


# This is used to plt.plot the plt.contour.
X, Y = meshgrid(A, B)

plt.figure(2)
Contour = plt.contour(X, Y, E, 25)
plt.clabel(Contour, Contour.levels[:5], inline=1)
plt.grid(True)
plt.title("Contour Plot", size=20)
plt.xlabel(r"$A", size=20)
plt.ylabel(r"$B", size=20)

# The below part of code is used to calculate the error in the estimate of A and B.
Ea = zeros((k_c, 1))
Eb = zeros((k_c, 1))

for j in range(k_c):
    AB = linalg.lstsq(M, data[:, j + 1], rcond=None)
    Ea[j], Eb[j] = abs(AB[0][0] - A0[0]), abs(AB[0][1] - A0[1])

# This will plt.plot the variation of error in the estimate of A and B with respect to noise.
plt.figure(3)
plt.plot(stdev, Ea, label="Aerr", marker="o", linestyle="dashed")
plt.plot(stdev, Eb, label="Berr", marker="o", linestyle="dashed")
plt.title("Variation of Error with Noise", size=20)
plt.grid(True)
plt.legend()
plt.xlabel("Noise standard deviation", size=20)
plt.ylabel("MS error", size=20)


# This will plt.plot the variation of error in the estimate of A and B with respect to noise in log scale.
plt.figure(4)
plt.loglog(stdev, Ea, "ro", label="Aerr",)
#plt.errorbar(stdev, Ea, std(Ea), fmt="ro")
plt.loglog(stdev, Eb, "go", label="Berr")
# plt.errorbar(stdev, Eb, std(Eb), fmt="go")
plt.title("Variation of Error with Noise", size=20)
plt.grid(True)
plt.legend()
plt.xlabel("Noise standard deviation", size=20)
plt.ylabel("MS error", size=20)


# This command will display all the graphs defined above.
plt.show()