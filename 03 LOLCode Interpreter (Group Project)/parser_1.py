from semantic import *

CORRECT = "No errors"

if_else_flag = False
ya_rly_flag = False

switch_flag = False
omg_flag = False


arith_binary_op = [
    "multiplication_operator",
    "division_operator",
    "subtraction_operator",
    "addition_operator",
    "modulo_operator",
    "greater_than_operator",
    "less_than_operator"
]

logic_binary_op = [
    "and_operator",
    "or_operator",
    "xor_operator",
]

comp_binary_op = [
    "equal_operator",
    "not_equal_operator",
]


def check_logic_op(line):

    # checks if syntax follows <OPERATION> <OPERAND> AN <OPERAND>
    if len(line) != 4:
        return "Incorrect number of arguments for logic operation"

    # checks if datatype and separators are correct
    if line[1][1] == "troof_literal" and line[2][1] == "argument_separator" and line[3][1] == "troof_literal":
        return CORRECT
    else:
        return "Improper format for logic operator"


def check_comparison_op(line):

    # checks if syntax follows <OPERATION> <OPERAND> AN <OPERAND>
    if len(line) != 4:
        return "Incorrect number of arguments for comparison operation"

    # checks if datatype and separators are correct
    if line[1][1] in ("troof_literal", "numbr_literal", "numbar_literal", "string_literal") and line[2][1] == "argument_separator" and line[3][1] in ("troof_literal", "numbr_literal", "numbar_literal", "string_literal"):
        return CORRECT
    else:
        return "Improper format for comparison operator"


def check_arithmetic_binary_op(line):

    # checks if syntax follows <OPERATION> <OPERAND> AN <OPERAND>
    if len(line) != 4:
        return "Incorrect number of arguments for binary operation"

    # checks if datatype and separators are correct
    if line[1][1] in ("numbar_literal", "numbr_literal") and line[2][1] == "argument_separator" and line[3][1] in ("numbar_literal", "numbr_literal"):
        return CORRECT
    else:
        result = "Improper syntax for " + str(line[0][0])
        return result


def check_visible(line):

    print(line)

    # checks if value to be printed is not an operation
    if line[1][1] in ("string_literal", "numbar_literal", "variable_identifier", "numbr_literal", "troof_literal", "identifier"):
        return CORRECT

    # if an operation is found, the operation is classified and then executed
    elif line[1][1] in arith_binary_op:
        result = check_arithmetic_binary_op(
            line[1:])  # executes arithmetic operation
        if CORRECT == result:
            return CORRECT
        else:
            return result
    elif line[1][1] in logic_binary_op:
        result = check_logic_op(line[1:])  # executes logic operation
        if CORRECT == result:
            return CORRECT
        else:
            return result
    elif line[1][1] in comp_binary_op:
        result = check_comparison_op(line[1:])  # executes comparison operation
        if CORRECT == result:
            return CORRECT
        else:
            return result

    # if value cannot be printed, and error will be returned
    else:
        return "Improper syntax for visible"


def check_variable(line):

    # checks for the various formats in variable declaration
    if len(line) == 2:
        # checks if declaration follows the correct syntax
        correctSyntax = ["variable_declarator", "variable_identifier"]
        if [line[x][1] for x in range(len(line))] == correctSyntax:
            return CORRECT

    elif len(line) == 4:
        # checks if declaration follows the correct syntax
        correctSyntax = ["variable_declarator",
                         "variable_identifier", "variable_declarator_ITZ"]
        if [line[x][1] for x in range(len(line)-1)] == correctSyntax and line[3][1] in ("numbar_literal", "numbr_literal", "troof_literal", "variable_identifier", "string_literal"):
            return CORRECT

    elif len(line) == 6:
        # checks if declaration follows the correct syntax
        correctSyntax = ["variable_declarator", "variable_identifier", "variable_declarator_ITZ",
                         "string_delimeter", "string_literal", "string_delimeter"]
        if [line[x][1] for x in range(len(line))] == correctSyntax:
            return CORRECT

    # if syntax is incorrect, an error will be returned
    return "Incorrect syntax for variable declaration"

# executes parsing on the lexeme table


def parser(lexemes_table):

    global if_else_flag, ya_rly_flag, switch_flag, omg_flag
    started = False

    j = 0  # keeps track on which line is being parsed
    while j != len(lexemes_table):

        # extracts line from lexeme table
        line = []
        while lexemes_table[j][1] != "new_line": # checks if newline is found, since newline is the line separator in the table
            line.append(lexemes_table[j])
            j += 1
        j += 1
        
        # checks if program has started
        if not started and line[0][1] != "start":
            return "Program does not start with HAI"
        else:
            started = True

        # checks if program has ended
        if line[0][1] == "end" and not if_else_flag and not switch_flag:
            return CORRECT
        elif line[0][1] == "end" and if_else_flag:
            return "Unclosed if else statement"
        elif line[0][1] == "end" and switch_flag:
            return "Unclosed switch statement"

        # removes delimiters to allow direct access to the string literal
        line = [i for i in line if i[1] != "string_delimeter"]

        # checks for if-else condition
        if if_else_flag:
            if line[0][1] == "if_statement": # if an if condition (ya rly) is found
                ya_rly_flag = True
            if line[0][1] == "end_of_if_else_statement" and not ya_rly_flag: # checks if there is an else statement, or if initial if condition is found
                return "No if statement in if else declaration"
            if line[0][1] == "end_of_if_else_statement" and ya_rly_flag: # checks if there is an else statement, or if initial if condition is found
                if_else_flag = False
            

        if switch_flag:
            if line[0][1] == "comparison_block":
                omg_flag = True
            if line[0][1] == "end_of_if_else_statement" and not omg_flag: # checks if there is an else statement, or if initial if condition is found
                return "No case in switch declaration"
            if line[0][1] == "end_of_if_else_statement" and omg_flag: # checks if there is an else statement, or if initial if condition is found
                switch_flag = False

        # checks for print statement
        if line[0][1] == "print_statement":
            result = check_visible(line) # checks for correct syntax and executes print
            if result != CORRECT:
                return result 

        # checks for arithmetic binary operation
        if line[0][1] in arith_binary_op:
            result = check_arithmetic_binary_op(line) # checks for correct syntax and executes operation
            if result != CORRECT:
                return result 

        # checks for variable declaration
        if line[0][1] == "variable_declarator":
            result = check_variable(line) # checks for correct syntax and saves value
            if result != CORRECT:
                return result

        # checks for logic binary operation
        if line[0][1] in logic_binary_op:
            result = check_logic_op(line) # checks for correct syntax and executes operation
            if result != CORRECT:
                return result 

        # checks for comparison binary operation
        if line[0][1] in comp_binary_op:
            result = check_comparison_op(line) # checks for correct syntax and executes operation
            if result != CORRECT:
                return result

        # checks for if-then statement
        if line[0][1] == "if_then_statement":
            if_else_flag = True

        if line[len(line)-1][1] == "switch":
            switch_flag = True

        # checks for variable identifier
        if line[0][1] in ("variable_identifier", "identifier"):
            if line[1][1] == "casting_assignment":
                if len(line) != 3: # checks for syntax
                    return "Improper syntax for typecasting"
                elif line[0][0] not in all_identifiers.keys(): # checks if variable has already been defined
                    return "Variable has not yet been declared"
