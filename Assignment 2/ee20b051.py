""" **************

            Assignment 2
Name: Jineeth N (EE20B051)
Date: 26-01-2022

Description: This code can solve AC as well as DC circuits
             Components: Resistor, Capacitor, Inductor, Voltage Source, Current Source, Voltage controlled current source
             voltage controlled voltage source.
Output: All node voltages and current through voltage sources

**************"""


# Importing the necessary modules.
from re import A
from numpy import *
from math import radians, sin, cos
from sys import argv, exit

# Classes are declared for each circuit component.
class Resistor:
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value


class Capacitor:
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value


class Inductor:
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value


class VoltageSource:
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value


class CurrentSource:
    def __init__(self, name, node1, node2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.value = value


class VCCS:
    def __init__(self, name, node1, node2, nc1, nc2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.nc1 = nc1
        self.nc2 = nc2
        self.value = value

class VCVS:
    def __init__(self, name, node1, node2, nc1, nc2, value):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.nc1 = nc1
        self.nc2 = nc2
        self.value = value


def printResult(V, n, k):
    for i in range(n - 1):
        print("V", i + 1, "=", V[i], "\n")
    for j in range(k):
        print("I", j + 1, "=", V[j + n - 1], "\n")


# This is to check the number of commnad line arguements.
if len(argv) != 2:
    print("Please provide the correct 2 arguments in the commandline.")
    exit()

# Assigning constants variables to .circuit , .end and .ac
CIRCUIT = ".circuit"
END = ".end"
AC = ".ac"

try:

    # Opening the file mentioned in the commandline.
    with open(argv[1]) as f:
        lines = f.readlines()

        # To check whether the given input file is correct.
        start, start_check = -1, -1
        end, end_check = -2, -1
        ac, ac_check = -1, -1

        # The program will traverse through the file and take out only the required part.
        for line in lines:
            if CIRCUIT == line[: len(CIRCUIT)]:
                start = lines.index(line)
                start_check = 0

            elif END == line[: len(END)]:
                end = lines.index(line)
                end_check = 0
            # To check whether the circuit has AC or DC source.
            elif AC == line[: len(AC)]:
                ac = lines.index(line)
                ac_check = 1

        # to check whether the given is correct.
        if start >= end or start_check == -1 or end_check == -1:
            print("Invalid circuit definition.")
            exit()

        #  A list to store all the necessary information required.
        l = []
        k = 0
        # In case of an AC circuit, the required information is collected.
        try:
            if ac_check == 1:
                _, ac_name, w = lines[ac].split("#")[0].split()
                w = 2 * 3.1415926 * float(w)

            for line in lines[start + 1 : end]:
                name, node1, node2, *value = line.split("#")[0].split()

                if name[0] == "R":
                    object = Resistor(name, node1, node2, value)

                elif name[0] == "C":
                    object = Capacitor(name, node1, node2, value)

                elif name[0] == "L":
                    object = Inductor(name, node1, node2, value)

                elif name[0] == "V":
                    object = VoltageSource(name, node1, node2, value)
                    k = k + 1

                elif name[0] == "I":
                    object = CurrentSource(name, node1, node2, value)

                elif name[0] == "G":
                    nc1 = value[0]
                    nc2 = value[1]
                    object = VCCS(name, node1, node2, nc1, nc2, float(value[2]))
                    l.append(object)
                    continue
                
                elif name[0] == "E":
                    nc1 = value[0]
                    nc2 = value[1]
                    object = VCCS(name, node1, node2, nc1, nc2, float(value[2]))
                    k += 1
                    l.append(object)
                    continue

                if len(object.value) == 1:
                    object.value = float(object.value[0])
                elif len(object.value) == 2:
                    object.value = float(object.value[1])
                # In case of an AC source, the voltage and phase are assigned properly.
                else:
                    object.value = (float(object.value[1]) / 2) * complex(
                        cos(radians(float(object.value[2]))), sin(radians(float(object.value[2])))
                    )

                l.append(object)

        # To show the error if the input is improper.
        except IndexError:
            print("Please make sure the netlist is written properly.")
            exit()

    # Creating a node dictionary.
    node = {}
    count = 1
    for object in l:
        if object.node1 not in node:
            if object.node1 == "GND":
                node["GND"] = 0

            else:
                name = object.node1
                node[name] = count
                count += 1

        if object.node2 not in node:
            if object.node2 == "GND":
                node["GND"] = 0

            else:
                name = object.node2
                node[name] = count
                count += 1

        if object.name[0] == "G" or object.name[0] == "E":
            if object.nc1 not in node:
                if object.nc1 == "GND":
                    node["GND"] = 0

                else:
                    name = object.nc1
                    node[name] = count
                    count += 1

            if object.nc2 not in node:
                if object.nc2 == "GND":
                    node["GND"] = 0

                else:
                    name = object.nc2
                    node[name] = count
                    count += 1

    node["GND"] = 0
    n = len(node)

    # creating M and b for for solving the question.
    M = zeros(((n + k - 1), (n + k - 1)), dtype="complex_")
    b = zeros(((n + k - 1), 1), dtype="complex_")
    p = 0

    #This part will the Matrices M and b in different situation.
    for object in l:

        # RESISTOR
        if object.name[0] == "R":
            if object.node2 == "GND":
                index1 = node[object.node1] - 1
                M[index1][index1] += 1 / object.value

            elif object.node1 == "GND":
                index2 = node[object.node2] - 1
                M[index2][index2] += 1 / object.value

            else:
                index1 = node[object.node1] - 1
                index2 = node[object.node2] - 1
                M[index1][index1] += 1 / object.value
                M[index2][index2] += 1 / object.value
                M[index1][index2] += -1 / object.value
                M[index2][index1] += -1 / object.value

        # CAPACITOR
        elif object.name[0] == "C":
            if ac_check == 1:
                Xc = -1 / (float(object.value) * w)
                object.value = complex(0, Xc)

            if object.node2 == "GND":
                index1 = node[object.node1] - 1
                M[index1][index1] += 1 / object.value
            elif object.node1 == "GND":
                index2 = node[object.node2] - 1
                M[index2][index2] += 1 / object.value

            else:
                index1 = node[object.node1] - 1
                index2 = node[object.node2] - 1
                M[index1][index1] += 1 / object.value
                M[index2][index2] += 1 / object.value
                M[index1][index2] += -1 / object.value
                M[index2][index1] += -1 / object.value

        # INDUCTOR
        elif object.name[0] == "L":
            if ac_check == 1:
                Xl = float(object.value) * w
                object.value = complex(0, Xl)

            if object.node2 == "GND":
                index1 = node[object.node1] - 1
                M[index1][index1] += 1 / object.value
            elif object.node1 == "GND":
                index2 = node[object.node2] - 1
                M[index2][index2] += 1 / object.value

            else:
                index1 = node[object.node1] - 1
                index2 = node[object.node2] - 1
                M[index1][index1] += 1 / object.value
                M[index2][index2] += 1 / object.value
                M[index1][index2] += -1 / object.value
                M[index2][index1] += -1 / object.value

        #CURRENT SOURCE
        elif object.name[0] == "I":
            print(object.value)
            if object.node2 == "GND":
                index1 = node[object.node1] - 1
                b[index1][0] += object.value

            elif object.node1 == "GND":
                index2 = node[object.node2] - 1
                b[index2][0] += -object.value

            else:
                index1 = node[object.node1] - 1
                index2 = node[object.node2] - 1
                b[index1][0] += object.value
                b[index2][0] += -object.value

        # VOLTAGE SOURCE
        elif object.name[0] == "V":

            if object.node2 == "GND":
                index1 = node[object.node1] - 1
                M[index1][n - 1 + p] += 1
                M[n - 1 + p][index1] += 1
                b[n - 1 + p] += object.value
                p = p + 1
            elif object.node1 == "GND":
                index2 = node[object.node2] - 1
                M[index2][n - 1 + p] += -1
                M[n - 1 + p][index2] += -1
                b[n - 1 + p] += object.value
                p = p + 1
            else:
                index1 = node[object.node1] - 1
                index2 = node[object.node2] - 1
                M[index1][n - 1 + p] += 1
                M[index2][n - 1 + p] += -1
                M[n - 1 + p][index1] += 1
                M[n - 1 + p][index2] += -1
                b[n - 1 + p] += object.value
                p = p + 1

        elif object.name[0] == "G":
            i1 = node[object.node1] - 1
            i2 = node[object.node2] - 1
            j1 = node[object.nc1] - 1
            j2 = node[object.nc2] - 1

            if i1 != -1 and j1 != -1:
                M[i1][j1] += object.value
            if i1 != -1 and i2 != -1:
                M[i1][i2] -= object.value
            if j1 != -1 and i2 != -1:
                M[i2][j1] -= object.value
            if i2 != -1 and j2 != -1:
                M[i2][j2] += object.value
        
        elif object.name[0] == "E":
            i1 = node[object.node1] - 1 
            i2 = node[object.node2] - 1
            j1 = node[object.nc1] - 1
            j2 = node[object.nc2] - 1
            kl = n - 1 + p 

            if i1 != -1:
                M[i1][kl] += 1
                M[kl][i1] += 1
            if i2 != -1:
                M[i2][kl] -= 1  
                M[kl][i2] -= 1

            if j1 != -1:
                M[kl][j1] -= object.value

            if j2 != -1:
                M[kl][j2] += object.value
            
            p = p + 1

    #  linalg.solve() function is used to solve the circuit equations.
    V = linalg.solve(M, b)
    print(M)
    print(b)
    printResult(V, n, k)
except FileNotFoundError:
    print("Invalid File.")
    exit()