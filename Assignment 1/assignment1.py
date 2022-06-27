"""
                      EE2703 Applied Programming Lab
                            Assignment 1
                          Name: JINEETH N
                          Date: 20-01-2022
INPUT: .netlist file
OUTPUT: Identifies errors in SPICE program code, and displays the tokens in reverse order

"""

from sys import argv, exit

def line2tokens(value_list):
    values = value_list

    # R, L, C, Independent Sources
    if len(values) == 4:
        elementName = values[0]
        node1 = values[1]
        node2 = values[2]
        value = values[3]
        return [elementName, node1, node2, value]

    # CCxS
    elif len(values) == 5:
        elementName = values[0]
        node1 = values[1]
        node2 = values[2]
        voltageSource = values[3]
        value = values[4]
        return [elementName, node1, node2, voltageSource, value]

    # VCxS
    elif len(values) == 6:
        elementName = values[0]
        node1 = values[1]
        node2 = values[2]
        voltageSourceNode1 = values[3]
        voltageSourceNode2 = values[4]
        value = values[5]
        return [
            elementName,
            node1,
            node2,
            voltageSourceNode1,
            voltageSourceNode2,
            value,
        ]

    else:
        return []

#The constant variables 'CIRCUIT' and 'END' determines the start and end of the described circuit.

CIRCUIT = ".circuit"
END = ".end"

if len(argv) != 2:
    print("Invalid operation !")
    print(f"Usage: {argv[0]} <inputfile>")
    exit()

try:
    with open(argv[1]) as f:
        lines = f.readlines()
        start = -1    #The 'start' and 'end' variables denote thet starting and ending line of the circuit simulation program.
        end = -2
        for line in lines:     # searching circuit definition start and end lines
            if CIRCUIT == line[0 : len(CIRCUIT)]:
                start = lines.index(line)
            elif END == line[: len(END)]:
                end = lines.index(line)
                break
        if start >= end:  # to ensure that end is present after start
            print("Invalid circuit definition!")
            exit(0)

        linesData = []
        for i in range(start + 1, end):
           line = (lines[i].split("#")[0].split())
           linesData.append(line)

        # linesToken = [line2tokens(line) for line in linesData]
        for line in linesData:
            linesToken = line2tokens(line)
        # print(linesToken)

        output = ""
        for i in reversed(range(start + 1, end)):       # to iterate from next line of start to (end-1)
            line = (lines[i].split("#")[0].split())     # to remove the comments present in checklist and split the words

            line.reverse()                              # to reverse the list
            output = output + (" ".join(line) + "\n")   # this is to join the words after reversing and add "\n" at the end of line

        print(output)

        # for line in reversed(linesData):
        #     for val in reversed(line):
        #         print(val, end=" ")
        #     print()

except IOError:
    print("Invalid file!")
    exit()