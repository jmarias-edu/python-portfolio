from lexer import all_identifiers

terminal_str = ""  # will be displayed in the terminal
SEMANTIC_ERROR = False
testCounter = 0

if_else_flag = False
if_else_result = False
if_else_condition = []
if_else_j = 0

prevLine = []
prevJ = 0

switch_flag = False
switch_literal = ""
switch_case_found = False


skipLine = False

binary_op = ["equal_operator",
             "or_operator",
             "multiplication_operator",
             "division_operator",
             "subtraction_operator",
             "greater_than_operator",
             "less_than_operator",
             "and_operator",
             "addition_operator",
             "modulo_operator",
             "xor_operator"]


def addition(line):
    result = float(line[1][0]) + float(line[3][0])  # performs addition
    return str(result)


def subtraction(line):
    result = float(line[1][0]) - float(line[3][0])  # performs subtraction
    return str(result)


def multiplication(line):
    result = float(line[1][0]) * float(line[3][0])  # performs multiplication
    return str(result)


def division(line):
    result = float(line[1][0]) / float(line[3][0])  # performs division
    return str(result)


def less_than(line):
    # returns lesser value
    if (int(line[3][0]) < int(line[1][0])):
        result = float(line[3][0])
    else:
        result = float(line[1][0])
    return str(result)


def greater_than(line):
    # returns greater value
    if (int(line[1][0]) > int(line[3][0])):
        result = float(line[1][0])
    else:
        result = float(line[3][0])
    return str(result)


def modulo(line):
    result = float(line[1][0]) % float(line[3][0])  # performs modulo
    return str(result)


def equal(line):
    # checks of two values are equal
    if line[1][0] == line[3][0]:
        result = "WIN"
    else:
        result = "FAIL"
    return result


def not_equal(line):
    # checks of two values are not equal
    if not line[1][0] == line[3][0]:
        result = "WIN"
    else:
        result = "FAIL"
    return result

# calls corresponding function that performs operation
def binary_operation(line):
    _result = ""
    if line[0][1] == "addition_operator":
        _result = addition(line)
    elif line[0][1] == "subtraction_operator":
        _result = subtraction(line)
    elif line[0][1] == "multiplication_operator":
        _result = multiplication(line)
    elif line[0][1] == "division_operator":
        _result = division(line)
    elif line[0][1] == "modulo_operator":
        _result = modulo(line)
    elif line[0][1] == "greater_than_operator":
        _result = greater_than(line)
    elif line[0][1] == "less_than_operator":
        _result = less_than(line)
    elif line[0][1] == "equal_operator":
        _result = equal(line)
    elif line[0][1] == "not_equal_operator":
        _result = not_equal(line)
    elif line[0][1] == "and_operator":
        _result = and_op(line)
    elif line[0][1] == "xor_operator":
        _result = xor_op(line)
    elif line[0][1] == "or_operator":
        _result = or_op(line)
    print("_result: "+_result)
    return _result


def visible(line):

    global SEMANTIC_ERROR, terminal_str

    # checks value or operation after print statement
    if (line[1][1] in binary_op):  # operation is performed and result is printed
        terminal_str += binary_operation(line[1:])
        terminal_str += "\n"
    elif (line[1][1] == "string_literal"):  # string is printed
        terminal_str += line[1][0]
        terminal_str += "\n"
    elif (line[1][1] == "variable_identifier"): # variavle is assigned then value is printed
        # checks for errors in variable assignment
        if (all_identifiers[line[1][0]] == None): 
            SEMANTIC_ERROR = True
            terminal_str += "Cannot implicitly cast Nil"
        else:
            terminal_str += all_identifiers[line[1][0]]
        terminal_str += "\n"


def and_op(line):
    # uses the and operator on two boolean values
    if line[1][0] == "WIN" and line[3][0] == "WIN":
        result = "WIN"
    else:
        result = "FAIL"
    return result


def or_op(line):
    # uses the or operator on two boolean values
    if line[1][0] == "FAIL" and line[3][0] == "FAIL":
        result = "FAIL"
    else:
        result = "WIN"
    return result


def xor_op(line):
    # uses the xor operator on two boolean values
    if line[1][0] == line[3][0]:
        result = "FAIL"
    else:
        result = "WIN"
    return result


def assignStr(line):
    all_identifiers[line[1][0]] = line[3][0] # assigns the string literal to the variable


def assignNum(line):
    all_identifiers[line[1][0]] = line[3][0] # assigns the numeric value to the variable


def reassignNum(line):  
    all_identifiers[line[1][0]] = all_identifiers[line[3][0]] # overwrites value assigned to variable


def assignNull(line):  
    all_identifiers[line[1][0]] = None # assign nil values for no values


def interpreter(lexemes_table):
    global SEMANTIC_ERROR, terminal_str, if_else_flag, if_else_condition, prevLine, skipLine, switch_flag, switch_literal, switch_case_found

    j = 0 # keeps track on which line is being interpreted
    
    while j != len(lexemes_table):
        line = []

        # implements logic similar to parser where each line is separated by newline
        while lexemes_table[j][1] != "new_line":  
            line.append(lexemes_table[j])
            j += 1
        j += 1

        # if parsing is interrupted or semantic error is found, loop will stop
        if len(line) == 0 or SEMANTIC_ERROR == True:  
            break
        if line[0][1] == "start": # loop will continue upon seeing program start
            continue
        elif line[0][1] == "end": # loop will stop upon seeing program end
            break
        
        # removes delimiters to allow direct access to the string literal
        line = [i for i in line if i[1] != "string_delimeter"]
        
        # locates which condition evaluates to true, then skips lines after
        if if_else_flag:
            if if_else_result and line[0][1] == "else_statement":
                skipLine = True
            elif not if_else_result and line[0][1] == "if_statement":
                skipLine = True
            elif not if_else_result and line[0][1] == "else_statement":
                skipLine = False
                continue
            elif line[0][1] == "end_of_if_else_statement": # resets flags upon reaching the end of statement
                skipLine = False
                if_else_flag = False
                continue
        
        # locates which case evaluates to true, then skips lines after
        if switch_flag:
            if line[0][1] == "comparison_block" and line[1][0] == switch_literal:
                skipLine = False
                switch_case_found = True
                continue
            elif line[0][1] == "break_statement":
                skipLine = True
                continue
            elif line[0][1] == "default_case" and not switch_case_found:
                skipLine = False

        if skipLine: # skips lines for if-else and switch 
            continue

        if line[0][1] == "print_statement":  # executes printing
            visible(line)

        elif line[0][1] in binary_op: # performs binary operation
            binary_operation(line)

        # check if variable declaration
        elif (line[0][1] == "variable_declarator"):

            # checks for various syntax depending on declaration type

            if len(line) == 2:  # I HAS A str
                assignNull(line)

            elif line[3][1] in ("numbr_literal", "numbar_literal"):  # I HAS A num ITZ 3
                assignNum(line)

            elif line[3][1] == "string_literal":  # I HAS var ITZ "some"
                assignStr(line)

            elif line[3][1] == "variable_identifier":  # I HAS var ITZ "some"
                reassignNum(line)

        # initiates if-then statement
        elif line[len(line)-1][1] == "if_then_statement":
            if_else_flag = True
            if_else_condition = prevLine
            if_else_result = binary_operation(prevLine) == "WIN"

        # resets flags upon reaching the end of statement
        elif line[0][1] == "end_of_if_else_statement":
            if_else_flag = False
            switch_flag = False
            switch_case_found = False

        # initiates switch case
        elif line[len(line)-1][1] == "switch":
            skipLine = True
            switch_flag = True
            switch_literal = all_identifiers[line[0][0]]

        # reassigns variable
        if line[0][1] in ("variable_identifier", "identifier"):
            if len(line) != 3:
                continue
            if line[1][1] == "casting_assignment":
                all_identifiers[line[0][0]] = line[2][0]

        prevLine = line
