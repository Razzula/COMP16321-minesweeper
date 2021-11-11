import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputDirectoryName')
parser.add_argument('outputDirectoryName')

args = parser.parse_args()

morseDict = {
    ".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E","..-.":"F","--.":"G","....":"H","..":"I",".---":"J","-.-":"K",".-..":"L","--":"M","-.":"N","---":"O",".--.":"P","--.-":"Q",".-.":"R","...":"S","-":"T","..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z","/":" ","-----":"0",".----":"1","..---":"2","...--":"3","....-":"4",".....":"5","-....":"6","--...":"7","---..":"8","----.":"9",".-.-.-":".","--..--":",","..--..":"?","..--.":"!","---...":":",".-..-.":'"',".----.":"'","-...-":"=","-..-.":"/",".--.-.":"@",
}

for file in os.listdir(args.inputDirectoryName):
    inputFile = open(args.inputDirectoryName + "/" + file, 'r')
    inp = inputFile.read()
    inputFile.close()

    cipher = ""
    cipherText = ""
    flag = True
    for i in range(len(inp)):
        if flag:
            if inp[i] == ":":
                flag = False
                continue
            cipher += inp[i]
        else:
            cipherText += inp[i]

    plainText = ""
    if cipher.lower() == "caesar cipher(+3)":
        
        plainTextPos = 0
        while (plainTextPos < len(cipherText)):
            plaintextChar = cipherText[plainTextPos]
            if plaintextChar == " ":
                plainText += " "
            else:
                ASCIIValue = ord(plaintextChar)
                ASCIIValue -= 3
                plainText += chr(ASCIIValue)
            plainTextPos += 1

    elif cipher.lower() == "hex":
        
        cipherArray = cipherText.split()
        for character in cipherArray:
            ASCIIValue = int(character, 16)
            temp = chr(ASCIIValue)
            plainText += temp

    elif cipher.lower() == "morse code":
        
        cipherArray = cipherText.split()
        for character in cipherArray:
            temp = morseDict[character]
            plainText += temp
    
    outputFile = open(args.outputDirectoryName + "/" + file[0:-4] + "_j56995jg.txt", 'w')
    outputFile.write(plainText.lower())
    inputFile.close()