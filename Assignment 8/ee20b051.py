"""
            EE2703 Applied Programming Lab - 2022
            Assignment 8: The Digital Fourier Transform(DFT)
            NAME: JINEETH N
            ROLLL NO.: EE20B051
            DATE: 07-05-22
"""

# Importing the required modulues
from sympy import *
import numpy as np
from numpy.fft import fftshift,fft
import matplotlib.pyplot as plt

pi = np.pi

#######
# 1.) Calculating the DFT(Digital Fourier Transform) of sin(5t)
x = np.linspace(0, 2*pi, 129); x = x[:-1]
y = np.sin(5*x)
Y0 = fftshift(fft(y))/128.0
w0 = np.linspace(-64, 63, 128)

plt.figure(0)

# Magnitude Plot
plt.subplot(2, 1, 1) # To plot magnitude and phase plot above and below at same pop up graph 
plt.plot(w0, abs(Y0), lw = 2) # Magnitude plot
plt.xlim([-10, 10]) # x(i.e., w{omega}) - axis limit 
plt.ylabel("|Y|", size = 16)
plt.title("Spectrum of sin(5t)")
plt.grid(True)

# Phase plot
plt.subplot(2, 1, 2)
plt.plot(w0, np.angle(Y0), 'ro', lw = 2) # Phase plot for all w 
ii = np.where(abs(Y0) > 1e-3)
plt.plot(w0[ii], np.angle(Y0[ii]), 'go', lw = 2) # Phase plot for such 'w' for which |Y| > 0.001
plt.xlim([-10, 10])
plt.ylabel("Phase of Y", size = 16)
plt.xlabel("k", size = 16)
plt.grid(True)


####### 
# 2.) Calculating the DFT of (1 + 0.1cos(t))cos(10t)
t1 = np.linspace(-4*pi, 4*pi, 513); t1 = t1[:-1] 
y1 = (1 + 0.1*np.cos(t1))*np.cos(10*t1) 
Y1 = fftshift(fft(y1))/512.0  
w1 = np.linspace(-64,64,513); w1 = w1[:-1]

plt.figure(1)


# Magnitude Plot
plt.subplot(2, 1, 1)
plt.plot(w1, abs(Y1), lw = 2)
plt.xlim([-15, 15])
plt.ylabel("|Y|", size = 16)
plt.title("Spectrum of (1 + 0.1cos(t))cos(10t)")
plt.grid(True)

# Phase plot 
plt.subplot(2, 1, 2)
plt.plot(w1, np.angle(Y1), 'ro', lw = 2)
plt.xlim([-15, 15])
plt.ylabel("Phase of Y", size = 16)
plt.xlabel("ω", size = 16)
plt.grid(True)


######
# 3.) Calculating the DFT of cos^3(t)
t2 = np.linspace(-4*pi, 4*pi, 513); t2 = t2[:-1]
y2 = (np.cos(t2))**3
Y2 = fftshift(fft(y2))/512.0
w2 = np.linspace(-64, 64, 513); w2 = w2[:-1]


# Magnitude plot
plt.figure(2)
plt.subplot(2, 1, 1)
plt.plot(w2, abs(Y2), lw = 2)
plt.xlim([-15, 15])
plt.ylabel("|Y|", size = 16)
plt.title("Spectrum of cos\u00B3(t)")
plt.grid(True)

# Phase plot
plt.subplot(2, 1, 2)
plt.plot(w2, np.angle(Y2), 'ro', lw = 2)
plt.xlim([-15, 15])
plt.ylabel("Phase of Y", size = 16)
plt.xlabel("ω",size = 16)
plt.grid(True)


######
# 4.) Calculating the DFT of sin^3(t)
t3 = np.linspace(-4*pi, 4*pi, 513); t3 = t3[:-1]
y3 = (np.sin(t3))**3
Y3 = fftshift(fft(y3))/512.0
w3 = np.linspace(-64, 64, 513); w3 = w3[:-1]

plt.figure(3)

# Magnitude Plot
plt.subplot(2, 1, 1)
plt.plot(w3, abs(Y3), lw = 2)
plt.xlim([-15, 15])
plt.ylabel("|Y|", size = 16)
plt.title("Spectrum of sin\u00B3(t)")
plt.grid(True)

# Phase Plot
plt.subplot(2, 1, 2)
plt.plot(w3, np.angle(Y3), 'ro', lw = 2)
plt.xlim([-15, 15])
plt.ylabel("Phase of Y", size = 16)
plt.xlabel("ω", size = 16)
plt.grid(True)


######
# 5.) Calculating the DFT of cos(20t + 5cos(t)) where magnitude is greater than 1e-3.
t4 = np.linspace(-4*pi, 4*pi, 513); t4 = t4[:-1]
y4 = np.cos(20*t4 + 5*np.cos(t4))
Y4 = fftshift(fft(y4))/512.0
w4 = np.linspace(-64, 64, 513); w4 = w4[:-1]

plt.figure(1)

# Magnitude Plot
plt.subplot(2, 1, 1)
plt.plot(w4, abs(Y4), lw = 2)
plt.xlim([-30, 30])
plt.ylabel("|Y|", size = 16)
plt.title("Spectrum of cos(20t + 5cos(t))")
plt.grid(True)

# Phase Plot
plt.subplot(2, 1, 2)
ii = np.where(abs(Y4) > 1e-3)
plt.plot(w4[ii], np.angle(Y4[ii]), 'go', lw = 2)
plt.xlim([-30, 30])
plt.ylabel("Phase of Y", size = 16)
plt.xlabel("ω", size = 16)
plt.grid(True)


# Defining the required functions
def gaussFn(x):
    return np.exp(-0.5*x**2)

def ExpectedGauss(w):
    return 1/np.sqrt(2*pi) * np.exp(-w**2/2)

def estdft(tolerance = 1e-6, samples = 128, func = gaussFn, expectedfn = ExpectedGauss, wlim = 5):
    T = 8*pi
    N = samples
    Yold = 0
    error = tolerance + 1
    iter = 0
    # Iterative loop to find window size
    while error > tolerance:  
        x = np.linspace(-T/2, T/2, N + 1)[:-1]
        w = np.linspace(-N*pi/T, N*pi/T, N + 1)[:-1]
        y = gaussFn(x)
        Y = fftshift(fft(fftshift(y)))*T/(2*pi*N)
        error = sum(abs(Y[::2] - Yold))
        Yold = Y
        iter += 1
        T *= 2
        N *= 2
        

    # Calculating error
    true_error = sum(abs(Y - expectedfn(w))) # Absolute error
    print("True error: ", true_error)
    print("Samples = " + str(N))
    print("Time period = " + str(T))

    mag = abs(Y)
    phi = np.angle(Y)
    phi[np.where(mag < tolerance)] = 0
    
    ######
    # 6.) Plotting estimated output
    plt.figure()
    
    # Magnitude Plot
    plt.subplot(2, 1, 1)
    plt.plot(w, abs(Y), lw = 2)
    plt.xlim([-wlim, wlim])
    plt.ylabel('Magnitude', size = 16)
    plt.title("Estimated FFT of Gaussian")
    plt.grid(True)

    # Phase Plot
    plt.subplot(2, 1, 2)
    plt.plot(w, np.angle(Y), 'ro', lw = 2)
    ii = np.where(abs(Y) > 1e-3)
    plt.plot(w[ii], np.angle(Y[ii]), 'go', lw = 2)
    plt.xlim([-wlim, wlim])
    plt.ylabel("Phase", size = 16)
    plt.xlabel("ω", size = 16)
    plt.grid(True)
    

    #######
    # 7.) Plotting expected output    
    Y_out = expectedfn(w)
    
    mag = abs(Y_out)
    phi = np.angle(Y_out)
    phi[np.where(mag < tolerance)] = 0
    
    plt.figure()
    
    # Magnitude Plot
    plt.subplot(2, 1, 1)
    plt.plot(w, abs(Y), lw = 2)
    plt.xlim([-wlim, wlim])
    plt.ylabel('Magnitude', size = 16)
    plt.title("True FFT of Gaussian")
    plt.grid(True)

    # Phase Plot
    plt.subplot(2, 1, 2)
    plt.plot(w, np.angle(Y), 'ro', lw = 2)
    ii = np.where(abs(Y) > 1e-3)
    plt.plot(w[ii], np.angle(Y[ii]), 'go', lw = 2)
    plt.xlim([-wlim, wlim])
    plt.ylabel("Phase", size = 16)
    plt.xlabel("ω",size = 16)
    plt.grid(True)
   

    return


estdft()

plt.show()