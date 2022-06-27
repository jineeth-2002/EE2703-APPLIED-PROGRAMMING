'''
------------------------------------
Assignment 4 - EE2703 
Name: Jineeth N (EE20B051)
Date: 26/02/2022
------------------------------------
'''

# from scipy import integrate
from scipy import integrate
from pylab import *

# Declaring all the required functions necessary for the program.
def expo(x):
    return exp(x)


def coscos(x):
    pass
    return cos(cos(x))


def a_exp(x, k):
    pass
    return expo(x) * cos(k * x)


def a_coscos(x, k):
    pass
    return coscos(x) * cos(k * x)


def b_exp(x, k):
    pass
    return expo(x) * sin(k * x)


def b_coscos(x, k):
    pass
    return coscos(x) * sin(k * x)

# Plot actual function and Predicted function(from lstsq) of exp(x)
def plot_fig1():
    figure(1)
    semilogy(x, y_exp, label="True")
    semilogy(xl[::5], yl_exp[::5], "og", label="Predicted")
    title("exp(x)")
    xlabel(r"x", size=15)
    ylabel(r"e^x", size=15)
    grid(True)
    legend()
    pass


# Plot actual function and Predicted function(from lstsq) of cos(cos(x))
def plot_fig2():
    figure(2)
    plot(x, y_coscos, label="True")
    plot(xl[::5], yl_coscos[::5], "og", label="Predicted")
    title("cos(cos(x))")
    xlabel(r"x", size=15)
    ylabel(r"cos(cos(x))", size=15)
    grid(True)
    legend()
    pass

# Plot fourier coefficents from both the methods in semilog scale for exp(x)
def plot_fig3():
    figure(3)
    semilogy(n, abs(c_exp), "or", label="True")
    semilogy(n, abs(cl_exp), "og", label="Predicted")
    title("exp(x) in semilog")
    xlabel(r"n", size=15)
    ylabel(r"coefficients", size=15)
    grid(True)
    legend()
    pass


# Plot fourier coefficents from both the methods in loglog scale for exp(x)
def plot_fig4():
    figure(4)
    loglog(n, abs(c_exp), "or", label="True")
    loglog(n, abs(cl_exp), "og", label="Predicted")
    title("exp(x) in loglog")
    xlabel(r"n", size=15)
    ylabel(r"coefficients", size=15)
    grid(True)
    legend()
    pass


# Plot fourier coefficents from both the methods in semilog scale for cos(cos(x))
def plot_fig5():
    figure(5)
    semilogy(n, abs(c_coscos), "or", label="True")
    semilogy(n, abs(cl_coscos), "og", label="Predicted")
    title("cos(cos(x)) in semilog")
    xlabel(r"n", size=15)
    ylabel(r"coefficients", size=15)
    grid(True)
    legend()
    pass


# Plot fourier coefficents from both the methods in loglog scale for cos(cos(x))
def plot_fig6():
    figure(6)
    loglog(n, abs(c_coscos), "or", label="True")
    loglog(n, abs(cl_coscos), "og", label="Predicted")
    title("cos(cos(x)) in loglog")
    xlabel(r"n", size=15)
    ylabel(r"coefficients", size=15)
    grid(True)
    legend()
    pass


def compute_fourier():
    # Store fourier coefficients
    c_exp = empty((51, 1))
    c_coscos = empty((51, 1))
    p = 0

    # This loop will calculate the first 51 Fourier coefficients of the functions.
    for k in range(26):

        # The corresponding Fourier series and coefficients are calculated and stored.
        if k != 0:
            c_coscos[p] = integrate.quad(a_coscos, 0, 2 * pi, args=(k))[0] / pi
            c_coscos[p + 1] = integrate.quad(b_coscos, 0, 2 * pi, args=(k))[0] / pi
            
            c_exp[p] = integrate.quad(a_exp, 0, 2 * pi, args=(k))[0] / pi
            c_exp[p + 1] = integrate.quad(b_exp, 0, 2 * pi, args=(k))[0] / pi
            p = p + 2

        # Calculate a0
        else:
            c_coscos[p] = (integrate.quad(a_coscos, 0, 2 * pi, args=(k))[0] / pi) / 2
            c_exp[p] = (integrate.quad(a_exp, 0, 2 * pi, args=(k))[0] / pi) / 2
            p = p + 1

    return c_exp, c_coscos

# Main

# Creating a range of x values from -2π to 4π.
x = np.linspace(-2 * pi, 4 * pi, 1200)

# Creating the corresponding function values.
y_exp = expo(x)
y_coscos = coscos(x)

# Generate values form 1 to 51
n = arange(1, 52)

# Calculate fourier coefficents
c_exp, c_coscos = compute_fourier()

# The below set of codes will find the values of the Fourier coefficients using the lstsq() function.
xl = linspace(0, 2 * pi, 401)
xl = xl[:-1]

B_exp = expo(xl)
B_coscos = coscos(xl)

# Least square fitting
A = np.zeros((400, 51))
A[:, 0] = 1
for k in range(1, 26):
    A[:, 2 * k] = sin(k * xl)
    A[:, 2 * k - 1] = cos(k * xl)
    
cl_exp = lstsq(A, B_exp, rcond=None)[0].reshape((-1, 1))
cl_coscos = lstsq(A, B_coscos, rcond=None)[0].reshape((-1, 1))

# The difference and deviation between the actual and predicted values are calculated.
d_exp = abs(cl_exp - c_exp).max()
d_coscos = abs(cl_coscos - c_coscos).max()

print("Max deviation for exp() is ", d_exp)
print("Max deviation for coscos() is ", d_coscos)

# The function values are calculated using the predicted Fourier coefficients.
yl_exp = dot(A, cl_exp)
yl_coscos = dot(A, cl_coscos)

plot_fig1()
plot_fig2()
plot_fig3()
plot_fig4()
plot_fig5()
plot_fig6()


show()