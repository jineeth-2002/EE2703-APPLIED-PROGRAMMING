'''
------------------------------------
Assignment 6 - EE2703 
Name: Jineeth N (EE20B051)
Date: 25/03/2022
------------------------------------
'''
# Importing the necessary modules.
from pylab import *
import scipy.signal as sp

# The python code snippet for Q.1
X1 = sp.lti([1, 0.5], polymul([1, 1, 2.5], [1, 0, 2.25]))  #for defining the transfer function
t1, x1 = sp.impulse(X1, None, linspace(0, 50, 500))       #Computes the impulse response of the transfer function
#this is to find the time response of the system.

# The plot x(t) vs t for Q.1
plt.figure(0)
plt.plot(t1, x1)
plt.title("Decay = 0.5",fontsize=12)
plt.xlabel("t",fontsize=10)
plt.ylabel("x(t)")
plt.grid()

# The python code snippet for Q.2
X2 = sp.lti([1, 0.05], polymul([1, 0.1, 2.2525], [1, 0, 2.25]))
t2, x2 = sp.impulse(X2, None, linspace(0, 50, 500))           #to convert to time domain response.

# The plot of x(t) vs t for Q.2
plt.figure(1)
plt.plot(t2, x2)
plt.title("Decay = 0.05",fontsize=12)
plt.xlabel("t",fontsize=10)
plt.ylabel("x(t)",fontsize=10)
plt.grid(True)

# The python code snippet for Q.3
H = sp.lti([1], [1, 0, 2.25])
l = 1.4
r = 1.6
for w in arange(l, r, 0.05):               #4 times the loop will be executed
    t = linspace(0, 80, 500)
    f = np.cos(w * t) * np.exp(-0.05 * t)
    t, x, svec = sp.lsim(H, f, t)

    # The plt.plot of x(t) for various frequencies vs time.
    plt.figure(2)
    plt.plot(t, x, label="w = " + str(w))
    plt.title("x(t) for various frequencies",fontsize=12)
    plt.xlabel("t",fontsize=10)
    plt.ylabel("x(t)",fontsize=10)
    plt.legend()
    plt.grid(True)


# The python code snippet for Q.4
t4 = linspace(0, 20, 500)
X4, Y4 = sp.lti([1, 0, 2], [1, 0, 3, 0]), sp.lti([2], [1, 0, 3, 0])     #to define a rational function.
t4, x4 = sp.impulse(X4, None, t4)
t4, y4 = sp.impulse(Y4, None, t4)

# The plot of x(t) and y(t) vs t for Q.4
plt.figure(3)
plt.plot(t4, x4, label="x(t)")
plt.plot(t4, y4, label="y(t)")
plt.title("x(t) and y(t)",fontsize=12)
plt.xlabel("t",fontsize=10)
plt.ylabel("functions",fontsize=10)
plt.legend()
plt.grid(True)

# The python code snippet for Q.5
temp = poly1d([1e-12, 1e-4, 1])
H5 = sp.lti([1], temp)            #transfer function of the given circuit
w, S, phi = H5.bode()             # S is the magnitude and Phi is the phase of the obtained transfer function.

# The magnitude bode plt.plot for Q.5
plt.figure(4)
plt.semilogx(w, S)
plt.title("Magnitude Bode plot",fontsize=12)
plt.xlabel("w",fontsize=10)
plt.ylabel("20*log|H(j*w)|",fontsize=10)
plt.grid(True)

# The phase bode plt.plot for Q.5
plt.figure(5)
plt.semilogx(w, phi)
plt.title("Phase Bode plot",fontsize=12)
plt.xlabel("w",fontsize=10)
plt.ylabel("< H(jw)",fontsize=10)
plt.grid(True)

# The python code snippet for Q.6
t6 = arange(0, 25e-3, 1e-7)
vi = cos(1e3 * t6) - cos(1e6 * t6)
t6, vo, svec = sp.lsim(H5, vi, t6)                #To find the output voltage.

# The plot of Vo(t) vs t for large time interval.
plt.figure(6)
plt.plot(t6, vo)
plt.title("The Output Voltage for large time interval",fontsize=12)
plt.xlabel("t",fontsize=10)
plt.ylabel("V_o(t)",fontsize=10)
plt.grid(True)

# The plot of Vo(t) vs t for small time interval.
plt.figure(7)
plt.plot(t6[0:350], vo[0:350])
plt.title("The Output Voltage for small time interval",fontsize=12)
plt.xlabel("t",fontsize=10)
plt.ylabel("V_o(t)",fontsize=10)
plt.grid(True)

show()