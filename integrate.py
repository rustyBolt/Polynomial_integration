import sys
from Integration import integrateFile, definitiveIntegrationFile

if __name__ == "__main__":
    arguments = sys.argv[1:]

    if len(arguments) < 1:
        print("Options: -i [path to input file] (defines path to input file, default path: 'input.txt'), -I (primitive integral), -D (definite integral)")
        exit()
    if len(arguments) > 3:
        print("Za duzo opcji!")
        exit()

    input = ""
    mode = 0
    for i in range(len(arguments)):
        if arguments[i] == '-i':
            if i + 1 < len(arguments) and arguments[i+1] not in "-i-I-D":
                input = arguments[i+1]
            else:
                print("Input file was not defined!")
                exit()
        elif arguments[i] == '-I':
            if mode == 0:
                mode = 1
            else:
                print("Option was already defined!")
                exit()
        elif arguments[i] == '-D':
            if mode == 0:
                mode = 2
            else:
                print("Option was already defined!")
                exit()
        
    if mode == 1:
        if input == "":
            print(integrateFile(r=True))
        else:
            print(integrateFile(input=input,r=True))
    elif mode == 2:
        if input == "":
            print(definitiveIntegrationFile(r=True))
        else:
            print(definitiveIntegrationFile(input=input,r=True))
