#### error handling --- 5 errors
#   1 : no value given for START keyword
#   2 : opcode mismatch(number of opcodes)
#   3 : value of location counter becomes more than 8 bit : shortage of memory error
#   4 : not a legal opcode


#### literal table ---- assuming the format of literal to be : "=3"
#### comment handling -- assuming comment start with symbol "/"  or "#" or "$" in this syntax and without spaces (use underscore instead)

opcodes = {}
opcodes["CLA"] = "0000"
opcodes["LAC"] = "0001"
opcodes["SAC"] = "0010"
opcodes["ADD"] = "0011"
opcodes["SUB"] = "0100"
opcodes["BRZ"] = "0101"
opcodes["BRN"] = "0110"
opcodes["BRP"] = "0111"
opcodes["INP"] = "1000"
opcodes["DSP"] = "1001"
opcodes["MUL"] = "1010"
opcodes["DIV"] = "1011"
opcodes["STP"] = "1100"


def printlist(File, word):  # function to print the tables
    for line in File:
        obj = ''
        for i in range(word):
            if (line[i] == '0000' or line[i] == '1100'):
                obj += line[i] + '\t\t\t' + "00000000"
            else:
                obj += line[i] + "\t\t\t"

        print(obj)

def printLine(temp):
    for i in range(70):
        print(temp,end="")
    print()
def isComment(tempStr):
    if (tempStr[0] == "#" or tempStr[0] == '$' or tempStr[0] == "/"):
        return True
    return False


def isLiteral(tempStr):
    if (tempStr[0] == '='):
        return True
    return False


def isSymbol(tempStr):
    if (tempStr not in temp_Symbol_table):
        return True
    return False


def isValidOpcode(tempStr):
    if (tempStr in opcodes):
        return True
    return False


def isZero_Operand(tempStr):
    Zero_Operator = ['STP', 'CLA']
    if (tempStr in Zero_Operator):
        return True
    return False


def isBranched(tempStr):
    if (tempStr[0] == ':'):
        return True
    return False


def requiredOperand_SingleOperator(tempStr):
    if (len(tempStr) == 1):
        return True
    if (len(tempStr) > 2 and isComment(tempStr[len(tempStr) - 1])):
        return False
    elif (len(tempStr) == 2 and not isComment(tempStr[len(tempStr) - 1])):
        return False

    return True


def checkMemorySpace(tempNo):
    if (tempNo < 0):
        return False
    return True

def print_list(L):
    # for i in L:
    #     print(i)
    pass

symbol_table = []  # final symbol table
temp_Symbol_table = []  # initial symbol table
temp_Literal_table = []            # initial Literal table
Literal_table = []              # Final Literal table
instruction_table = []                 # instruction table
temp=0  # if  jump <0

def PassOne(File, Program_Checker):
    ###### return opcode table , literal table , symbol table ::::::::

    ### Program_Checker : to generate error

    LC = 0          #location counter
    flag = 1
    check = 0  # condition : becomes 1 once the code starts

    line_no = 0
    for line in File:
        word = line.split()
        line_no += 1

        if ((len(word) == 0 and check == 1) or (len(word) > 0 and word[0] == "END")):  # conditon for end of code
            LC += 1
            for i in temp_Symbol_table:
                lc = bin(LC).replace("0b", "")
                lngth = len(lc)
                jum = 8 - lngth

                if (jum >= 0):
                    temp=1
                    lc = "0" * jum + lc
                    symbol_table.append([i, lc])
                    print_list(symbol_table)
                    LC += 8

                else:
                    temp=0
                    print("Error : Memory shortage for addresses ! in assigning address to variable")
                    Program_Checker = 1
                    break

            for j in temp_Literal_table:
                lc = bin(LC).replace("0b", "")
                lngth = len(lc)
                jum = 8 - lngth
                if (jum >= 0):
                    temp=1
                    LC += 8
                    lc = "0" * jum + lc
                    Literal_table.append([j, lc])
                    print_list(Literal_table)

                else:
                    temp=0
                    print("Error : Memory shortage for addresses ! in assigning to literal ")
                    Program_Checker = 1
                    break

            break
        else:
            check = 1
            if (flag == 1):
                temp=0

                if (word[0] == "START"):

                    if (requiredOperand_SingleOperator(word)):
                        print("Error : NO location value assigned to START ! in line " + str(line_no))
                        Program_Checker = 1

                    else:
                        LC = int(word[1])
                        flag = 0

            if (word[0] != "START"):  ##### to show errror if more than one operand
                temp=0
                lc = bin(LC).replace("0b", "")
                lngth = len(lc)
                jum = 8 - lngth  # address size : 8 bit
                temp=1
                if (not checkMemorySpace(jum)):
                    print("Error : Memory shortage for addresses ! in line " + str(line_no))
                    Program_Checker = 1
                    break

                else:
                    lc = "0" * jum + lc

                if (isValidOpcode(word[0])):

                    if (len(word) == 2):

                        if (isComment(word[1][0])):
                            comm = word[1]
                            word[1] = " "
                            word.append(comm)

                            temp=1
                            print_list(word)

                        else:
                            if (isLiteral(word[1]) and word[1][1:] not in Literal_table):
                                temp_Literal_table.append(word[1][1:])
                                print_list(temp_Literal_table)

                            elif (isSymbol(word[1])):
                                temp_Symbol_table.append(word[1])
                                print_list(temp_Symbol_table)

                            word.append(" ")
                            print_list(word)

                    elif (len(word) == 3):

                        if (isLiteral(word[1]) and word[1][1:] not in Literal_table):
                            temp_Literal_table.append(word[1][1:])

                        elif (isSymbol(word[1])):
                            temp_Symbol_table.append(word[1])
                            print_list(temp_Symbol_table)

                        if (isBranched(word[0])):
                            temp_label.append(word[1])
                            print_list(temp_label)

                    else:
                        word.append(" ")
                        word.append(" ")
                    instruction_table.append(word[:2] + [lc] + [word[2]])
                    print_list(instruction_table)

                elif (word[0][:-1] in temp_Symbol_table):
                    temp=0
                    symbol = [word[0][:-1], lc]
                    temp_Symbol_table.remove(word[0][:-1])
                    symbol_table.append(symbol)
                    print_list(symbol_table)
                    if (len(word) == 2):
                        word.append(" ")
                        word.append(" ")

                    elif (len(word) == 3):
                        if (isComment(word[2])):
                            comm = word[2]
                            word[2] = " "
                            word.append(comm)

                        else:
                            word.append(" ")
                    instruction_table.append(word[1:3] + [lc] + [word[3]])
                    print_list(instruction_table)

                else:
                    temp=0
                    if (True):

                        if (word[0] != "END"):

                            if (word[0][-1] == ":"):
                                print("Error : " + word[0] + " not a legal label ! in line " + str(line_no))
                            else:
                                print("Error : " + word[0] + " not a legal opcode ! in line " + str(line_no))
                            Program_Checker = 1
                LC += 12


    # assigning location counter to variables in binary value in symbol and literal table at the end of file

    for jum in instruction_table:
        if (not isValidOpcode(jum[0])):
            print("Error : " + jum[0] + ' not a legal opcode.')
            Program_Checker = 1

        if (isZero_Operand(jum[0])):
            if (jum[1] != ' '):
                print("Error : " + jum[0] + " has wrong operands. ")
                Program_Checker = 1

            if(isValidOpcode(jum[0])):
                if(not isZero_Operand(jum[0])):
                    if ((',' in jum[1]) or jum[1] == " "):
                        print("Error : " + jum[0] + " has wrong operands. ")
                        Program_Checker = 1

    if (Program_Checker == 0):
        for i in range(3):
            print()
        printLine('-')
        print("              Symbol Table                ")
        printLine('-')
        TAB1 = [["Symbol", "Address"]] + symbol_table
        printlist(TAB1, 2)
        
        for i in range(3):
            print()
        printLine('-')
        print("              Literal Table               ")
        printLine('-')

        TAB3 = [["Literal", "Address"]] + Literal_table
        printlist(TAB3, 2)

        printLine('-')
        print("                            Opcode Table                              ")
        printLine('-')

        TAB2 = [["Opcode", "Operand ", "File C ", " Comment "]] + instruction_table

        printlist(TAB2, 4)

        print_list(symbol_table)

    return symbol_table, instruction_table, Literal_table, Program_Checker


def PassTwo(symbol_table, instruction_table, Literal_table):
    for inst in instruction_table:
        opcode = inst[0]
        
        for i in opcodes:
            if(i!=opcode):
                pass
            else:
                inst[0] = opcodes[i]
                print_list(opcode)
                break

        if (len(inst) > 1):
            operand = inst[1]
            checker = 0
            if(operand!=''):
                
                for j in symbol_table:
                    
                    if(j[0]!=operand):
                        pass
                    else:
                        inst[1] = j[1]
                        checker = 1
                        break

                if (checker == 0):
                    for j in Literal_table:
                        if (j[0] == operand):
                            inst[1] = j[1]
                            checker = 1
                            break
            else:
                inst[2] = ''
                continue


    printLine('-')
    print("                            Object Code                               ")
    printLine('-')

    printlist(instruction_table, 2)
    file2 = open("output.txt", "w")

    for i in instruction_table:
        obj = ''
        
        for j in range(2):
            if (i[j] == '0000' or i[j] == '1100'):
                obj += i[j]+'\t'+"00000000"
                continue
            obj += i[j] + '\t'
        
        obj = obj + '\n'
        file2.write(obj)

    file2.close


# ----------------------------Code Starts Here!!!----------------------------
file1 = open("input.txt")
File = file1.read().split('\n')
Program_Checker = 0  # initially no error !
print("                Pass1                     ")

L1, L2, L3, Program_Checker = PassOne(File, Program_Checker)  # apply pass1() function to this list form ""
for i in range(3):
	print()
if(Program_Checker!=0):
	pass
else:
    print("                Pass2                     ")
    PassTwo(L1, L2, L3)
