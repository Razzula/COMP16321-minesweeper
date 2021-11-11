import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputDirectoryName')
parser.add_argument('outputDirectoryName')

args = parser.parse_args()

for file in os.listdir(args.inputDirectoryName):
    inputFile = open(args.inputDirectoryName + "/" + file, 'r')
    inp = inputFile.read()
    #fileName = inputFile.name
    inputFile.close()

    scores = []
    for i in range(0, len(inp), 3):
        scores.append(inp[i:i+3])

    T1 = 0
    T2 = 0

    for score in scores:
        if score[2] == 't':
            increment = 5
        elif score[2] == 'c':
            increment = 2
        elif score[2] == 'p':
            increment = 3
        elif score[2] == 'd':
            increment = 3
        else:
            increment = 0

        if score[0:2] == 'T1':
            T1 += increment
        elif score[0:2] == 'T2':
            T2 += increment

    outputFile = open(args.outputDirectoryName + "/" + file[0:-4] + "_j56995jg.txt", 'w')
    outputFile.write(str(T1) + ":" + str(T2))
    inputFile.close()