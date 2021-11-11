import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('wordList')
parser.add_argument('inputDirectoryName')
parser.add_argument('outputDirectoryName')

args = parser.parse_args()

numbers = ["0","1","2","3","4","5","6","7","8","9"]
punctuation = [".","?","!",",",":",";","-","(",")","[","]","{","}","'",'"',"#","@","£","%","^","&","*","_","+","~"]

for file in os.listdir(args.inputDirectoryName):
    inputFile = open(args.inputDirectoryName + "/" + file, 'r')
    inp = inputFile.read()
    inputFile.close()
    #inp = "The tres[12], therefore, must be such old and primitive techniquess that they thought nothing of them, deeming them so inconsequential that even savages like us would knowe of them and not be suspicious. At that, they probably didn't have too much time after they detected us orbiting and intending to land[15]. And if that were true, there cud be only one place where their civilization was hidden[16]."

    caseTrans = 0
    puncRmvs = 0
    nmbrRmvs = 0
    temp = ""

    for i in range(len(inp)):
        if inp[i] in punctuation:
            puncRmvs += 1
            continue
        if inp[i] in numbers:
            nmbrRmvs += 1
            continue
        else:
            temp += inp[i]

    wordFile = open(args.wordList, "r")
    #wordFile = open("EnglishWords.txt", "r")
    correctWords = wordFile.read().split()
    wordFile.close()

    wordCount = 0
    correctWordCount = 0

    words = temp.split()
    for word in words:
        wordCount += 1
        if word.lower() in correctWords:
            correctWordCount += 1
        # else:
        #     print(word)
        for i in range(len(word)):
            if word[i] == word[i].upper():
                caseTrans += 1

    outputFile = open(args.outputDirectoryName + "/" + file[0:-4] + "_j56995jg.txt", 'w')
    outputFile.write("j56995jg")
    outputFile.write("\nFormatting ###################")
    outputFile.write("\nNumber of upper case words transformed: " + str(caseTrans))
    outputFile.write("\nNumber of punctuations removed: " + str(puncRmvs))
    outputFile.write("\nNumber of numbers removed: " + str(nmbrRmvs))
    outputFile.write("\nSpellchecking ###################")
    outputFile.write("\nNumber of words: " + str(wordCount))
    outputFile.write("\nNumber of correct words: " +  str(correctWordCount))
    outputFile.write("\nNumber of incorrect words: " + str(wordCount - correctWordCount))
    inputFile.close()