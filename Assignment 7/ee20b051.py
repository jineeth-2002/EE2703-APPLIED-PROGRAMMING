import matplotlib.pyplot as plt
from sympy import *
import pylab as p
import scipy.signal as sp

s = symbols("s")

# Lowpass filter.
def lowpass(R1, R2, C1, C2, G, Vi):
    s = symbols("s")
    # Creating the matrices and solving them to get the output voltage.
    A = Matrix(
        [
            [0, 0, 1, -1 / G],
            [-1 / (1 + s * R2 * C2), 1, 0, 0],
            [0, -G, G, 1],
            [-1 / R1 - 1 / R2 - s * C1, 1 / R2, 0, s * C1],
        ]
    )
    b = Matrix([0, 0, 0, -Vi / R1])
    V = A.inv() * b
    return A, b, V


# Highpass filter.
def highpass(R1, R3, C1, C2, G, Vi):
    s = symbols("s")
    # Creating the matrices and solving them to get the output voltage.
    A = Matrix(
        [
            [0, -1, 0, 1 / G],
            [s * C2 * R3 / (s * C2 * R3 + 1), 0, -1, 0],
            [0, G, -G, 1],
            [-s * C2 - 1 / R1 - s * C1, 0, s * C2, 1 / R1],
        ]
    )
    b = Matrix([0, 0, 0, -Vi * s * C1])
    V = A.inv() * b
    return A, b, V


# Convert a sympy function into a version that is understood by sp.signal
def sympyToCoeff(Y):
    # The following lines will give the proper form for numerator and denomerator.
    n, d = fraction(Y)                            #splitting the numnerator and denominator
    n, d = Poly(n, s), Poly(d, s)                 #it will replace the variable with s
    num = n.all_coeffs()                          #coefficients of the numerator are extracted                  
    den = d.all_coeffs()
    num, den = [float(f) for f in num], [float(f) for f in den]
    # This will calculate the function that is understood by sp.signal
    H = sp.lti(num, den)
    return H                                       


# Reassigning the value of PI.
PI = p.pi                           

# The below piece of code will calculate the transfer function for the lowpass filter.
A, b, V = lowpass(10000, 10000, 1e-9, 1e-9, 1.586, 1)
Vo = V[3]                              #because the given input is 1
H = sympyToCoeff(Vo)
ww = p.logspace(0, 8, 801)      #between 1 to 10^8 801 values are equally spaced in log scale.
ss = 1j * ww
hf = lambdify(s, Vo, "numpy")     #converting the expression into a numpy function.
v = hf(ss)

# Magnitude of transfer function of a lowpass filter.
plt.figure(0)
plt.loglog(ww, abs(v), lw=2)
plt.title(r"$|H(j\omega)|$ for lowpass filter", fontsize=12)
plt.xlabel(r"$\omega$", fontsize=10)
plt.ylabel(r"$|H(j\omega)|$", fontsize=10)
plt.grid(True)

# These lines of code will calculate the step response for the lowpass filter.
A1, b1, V1 = lowpass(10000, 10000, 1e-9, 1e-9, 1.586, 1 / s)
Vo1 = V1[3]
H1 = sympyToCoeff(Vo1)
t, y1 = sp.impulse(H1, None, p.linspace(0, 5e-3, 10000))

# The plot for step response of a lowpass filter.
plt.figure(1)
plt.plot(t, y1)
plt.title(r"Step Response for low pass filter", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)

# The response is also calculated for sum of sinusoids.
a = 2e3
b = 2e6
vi = p.sin(a * PI * t) + p.cos(b * PI * t)
t, y2, svec = sp.lsim(H, vi, t)               #to get the time response output

# The plot for output response for sum of sinusoids of a lowpass filter.
plt.figure(2)
plt.plot(t, y2)
plt.title(r"Output voltage for sum of sinusoids", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)


# The below piece of code will calculate the transfer function for the highpass filter.
A3, b3, V3 = highpass(10000, 10000, 1e-9, 1e-9, 1.586, 1)
Vo3 = V3[3]
H3 = sympyToCoeff(Vo3)
hf3 = lambdify(s, Vo3, "numpy")
v3 = hf3(ss)

# The plot for Magnitude of transfer function of a highpass filter.
plt.figure(3)
plt.loglog(ww, abs(v3), lw=2)
plt.title(r"$|H(j\omega)|$ for highpass filter", fontsize=12)
plt.xlabel(r"$\omega$", fontsize=10)
plt.ylabel(r"$|H(j\omega)|$", fontsize=10)
plt.grid(True)

# The output response is calculated when the input is a damped sinusoid for both high and low frequency.
# High frequency.
d_f = -500
f = 2e6
t = p.linspace(0, 1e-2, int(1e5))
vi4_1 = p.exp(d_f * t) * p.cos(f * PI * t)
t, y4_1, svec = sp.lsim(H3, vi4_1, t)

# The plot for high frequency damped sinusoids.
plt.figure(4)
plt.plot(t, vi4_1)
plt.title(r"High frequency damped sinusoid ", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)

# Low frequency.
f = 2e3
t = p.linspace(0, 1e-2, int(1e5))
vi4_2 = p.exp(d_f * t) * p.cos(f * PI * t)
t, y4_2, svec = sp.lsim(H3, vi4_2, t)

# The plot for low frequency damped sinusoids.
plt.figure(5)
plt.plot(t, vi4_2)
plt.title(r"Low frequency damped sinusoid", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)

# The plot for high frequency damped sinusoid response from highpass filter.
plt.figure(6)
plt.plot(t, y4_1)
plt.title(r"High frequency damped sinusoid response from High Pass filter", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)

# The plot for low frequency damped sinusoid response from highpass filter.
plt.figure(7)
plt.plot(t, y4_2)
plt.title(r"Low frequency damped sinusoid response from High Pass filter", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)


A4, b4, V4 = lowpass(10000, 10000, 1e-9, 1e-9, 1.586, 1)
Vo4 = V4[3]
H4 = sympyToCoeff(Vo4)
hf3 = lambdify(s, Vo4, "numpy")
v3 = hf3(ss)

# The output response is calculated when the input is a damped sinusoid for both high and low frequency.
# High frequency.
d_f = -500
f = 2e6
t = p.linspace(0, 1e-2, int(1e5))
vi4_1 = p.exp(d_f * t) * p.cos(f * PI * t)
t, y4_1, svec = sp.lsim(H4, vi4_1, t)

# Low frequency.
f = 2e3
t = p.linspace(0, 1e-2, int(1e5))
vi4_2 = p.exp(d_f * t) * p.cos(f * PI * t)
t, y4_2, svec = sp.lsim(H4, vi4_2, t)

# The plot for high frequency damped sinusoid response from lowpass filter.
plt.figure(9)
plt.plot(t, y4_1)
plt.title(r"High frequency damped sinusoid response from Low Pass filter", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)

# The plot for low frequency damped sinusoid response from lowpass filter.
plt.figure(10)
plt.plot(t, y4_2)
plt.title(r"Low frequency damped sinusoid response from Low Pass filter", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)

# The step response is calculated for a highpass filter.
A5, b5, V5 = highpass(10000, 10000, 1e-9, 1e-9, 1.586, 1 / s)
Vo5 = V5[3]
H5 = sympyToCoeff(Vo5)
t, y5 = sp.impulse(H5, None, p.linspace(0, 5e-3, 10000))

# The plot for step response of a highpass filter.
plt.figure(11)
plt.plot(t, y5)
plt.title(r"Step Response for high pass filter", fontsize=12)
plt.xlabel(r"$t$", fontsize=10)
plt.ylabel(r"$V_o(t)$", fontsize=10)
plt.grid(True)

plt.show()