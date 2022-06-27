"""
                       EE2703 Applied Programming Lab 
                             Assignment-01
                            Name: Jineeth N
                           Date: 20-01-2022

INPUT: .netlist file
OUTPUT: Displays the tokens in reverse order and identifies errors in SPICE program code                           

"""

from sys import argv, exit

#The constant variables 'CIRCUIT' and 'END' determines the start and end of the described circuit.  

CIRCUIT = ".circuit"       
END = ".end"

 #To check only if required inputs are given and whether the given file is correct and the file exists
if len(argv) != 2:                     
    print("Invalid operation !")
    print(f"Usage: {argv[0]} <inputfile>'")
    exit()


try:
    with open(argv[1]) as f:
        lines = f.readlines()
        start = -1
        end = -2
        for line in lines:             
            if CIRCUIT == line[0 : len(CIRCUIT)]:
                start = lines.index(line)
            elif END == line[: len(END)]:
                end = lines.index(line)
                break
        if start >= end:                #to ensure .ciruit and .end are present and .circuit comes before .end
            print("Invalid circuit definition!")
            exit(0)

        output = ""
        for i in reversed(range(start + 1, end)):       # loop starting from next line of circuit till (end-1) line.
            line = (lines[i].split("#")[0].split())     # 

            line.reverse()                              # reverse the list
            output = output + (" ".join(line) + "\n")   # join words after reversing and add "\n" at the end of line

        print(output)

except IOError:
    print("Invalid file!")
    exit()