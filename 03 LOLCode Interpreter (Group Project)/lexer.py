import re  # imports regex

multiline = False
multiline_valid = False
error_detected = False

lexemes_table = []
all_identifiers = {}
variable_identifiers = []
function_identifiers = []
loop_identifiers = []
not_binary = ["concatenation", "infinite_and", "infinite_or_operator", "unary_negation"]

all_regexes = {
    "IS NOW A": "type_casting",
    "YA RLY": "if_statement",
    "O RLY\?": "if_then_statement",
    "NO WAI": "else_statement",
    "BOTH SAEM": "equal_operator",
    "EITHER OF": "or_operator",
    "PRODUKT OF": "multiplication_operator",
    "QUOSHUNT OF": "division_operator",
    "DIFF OF": "subtraction_operator",
    "BIGGR OF": "greater_than_operator",
    "SMALLR OF": "less_than_operator",
    "BOTH OF": "and_operator",
    "SUM OF": "addition_operator",
    "MOD OF": "modulo_operator",
    "WON OF": "xor_operator",
    "ANY OF": "infinite_or_operator",
    "ALL OF": "infinite_and",
    "R MAEK": "r_maek_literal",
    "KTHXBYE": "end",
    "DIFFRINT": "not_equal_operator",
    "VISIBLE": "print_statement",
    "OMGWTF": "default_case",
    "GIMMEH": "input_statement",
    "SMOOSH": "concatenation",
    "UPPIN": "increment",
    "NERFIN": "decrement",
    "MEBBE": "else_if_statement",
    "WILE": "continue_while_true",
    "MAEK": "type_casting",
    "HAI": "start",
    "TIL": "continue_while_false",
    "ITZ": "variable_declarator_ITZ",
    "NOT": "unary_negation",
    "OIC": "end_of_if_else_statement",
    "WTF\?*": "switch",
    "OMG": "comparison_block",
    "GTFO": "break_statement",

    "HOW IZ I (([A-Za-z])\w*)": "function_declarator",
    "IM IN YR [a-zA-Z]+[a-zA-Z0-9_]*": "loop_declarator",
    "IM OUTTA YR [a-zA-Z][a-zA-Z0-9_]*": "loop_end",
    "I HAS A [A-Za-z]+[0-9A-Za-z_]*": "variable_declarator",

    '\"[^"]*\"': "yarn_literal",
    "-?[0-9]*\.[0-9]+": "numbar_literal",
    "-?[0-9]+": "numbr_literal",
    "(WIN|FAIL)": "troof_literal",
    "(NUMBR|NUMBAR|YARN|TROOF)": "type_literal",

    "AN": "argument_separator",  # <opr> <exp> AN <exp>
    "YR": "YR_separator",  # IM IN YR <opr> YR <var>
    "A": "A_separator",  # MAEK [A]
    "R": "casting_assignment",  # R MAEK
    ",": "comma",

    "[a-zA-Z][a-zA-Z0-9_]*": "identifier",
}

def identify_lexemes(line):
    
    emptyCheck = False
    global multiline, multiline_valid, error_detected
    line = line.strip() # removes whitespace

    # substitution important for checking multiline comment syntax
    line = re.sub("OBTW .* (?!TLDR)", "", line)

    # checks if line is empty
    if line.isspace() or line=="":
        emptyCheck = True

    # checks for multiline comments
    OBTWCheck = re.search("OBTW", line)
    TLDRCheck = re.search("TLDR", line)
    newlineCheck = re.search("\n", line)

    # updates flagger when multiline comment is found

    if not multiline: # disregards comments by removing
        line = re.sub("BTW .*", "", line)
        if line.isspace() or line == "":
            return
    if OBTWCheck != None: # if start of multiline comment is detected
        multiline = True
        print("Multiline comment detected!")
        return
    if multiline and newlineCheck != None: # checks if TLDR is found in a separate line
        multiline_valid = True
        return
    if TLDRCheck != None: # if end of multiline comment is detected
        multiline = False
        if not multiline_valid: # if OBTW and TLDR are in the same line
            print("Error: incorrect multiline comment syntax")
            error_detected = True
        line = line.replace("TLDR", " ", 1) # removes TLDR

    regexes = all_regexes.keys()  # retrieves regexes from the dictionary

    # iterates until end of line is reached
    while not (line.isspace() or line == "") and not multiline and not error_detected:

        # removes whitespaces from line
        line = line.strip()

        # goes through all regexes
        for regex in regexes:

            # finds first match to the current regex
            result = re.match(regex, line)

            # if a match is found
            if result != None:

                # checks if match is a string
                if regex == '\"[^"]*\"':

                    # separates delimiters from literal
                    lexemes_table.append(['"', "string_delimeter"])
                    lexemes_table.append(
                        [result.group()[1:-1], "string_literal"])
                    lexemes_table.append(['"', "string_delimeter"])

                    # replaces match with space to exclude from next iteration
                    line = line.replace(result.group(), " ", 1)
                    break

                # checks for identifiers
                if regex == "[a-zA-Z][a-zA-Z0-9_]*":

                    # classifies which type of identifier
                    if result.group() in variable_identifiers:
                        lexemes_table.append(
                            [result.group(), "variable_identifier"])
                    elif result.group() in loop_identifiers:
                        lexemes_table.append(
                            [result.group(), "loop_identifier"])
                    elif result.group() in function_identifiers:
                        lexemes_table.append(
                            [result.group(), "function_identifier"])
                    else:
                        lexemes_table.append([result.group(), "identifier"])

                    # replaces match with space to exclude from next iteration
                    line = line.replace(result.group(), " ", 1)
                    break

                # checks if function declaration
                if regex == "HOW IZ I (([A-Za-z])\w*)":

                    function_identifiers.append(
                        result.group().replace("HOW IZ I", "").strip())
                    lexemes_table.append(["HOW IZ I", "function_declarator"])
                    lexemes_table.append([result.group().replace(
                        "HOW IZ I", "").strip(), "function_identifier"])

                    # replaces match with space to exclude from next iteration
                    line = line.replace(result.group(), " ", 1)
                    break

                # checks if loop declaration
                elif regex == "IM IN YR [a-zA-Z]+[a-zA-Z0-9_]*":

                    loop_identifiers.append(
                        result.group().replace("IM IN YR", "").strip())
                    lexemes_table.append(["IM IN YR", "loop_declarator"])
                    lexemes_table.append([result.group().replace(
                        "IM IN YR", "").strip(), "loop_identifier"])

                    # replaces match with space to exclude from next iteration
                    line = line.replace(result.group(), " ", 1)
                    break

                # checks if variable declaration
                elif regex == "I HAS A [A-Za-z]+[0-9A-Za-z_]*":

                    all_identifiers[result.group().replace("I HAS A", "").strip()] = None
                    variable_identifiers.append(
                        result.group().replace("I HAS A", "").strip())
                    lexemes_table.append(["I HAS A", "variable_declarator"])
                    lexemes_table.append([result.group().replace(
                        "I HAS A", "").strip(), "variable_identifier"])

                    # replaces match with space to exclude from next iteration
                    line = line.replace(result.group(), " ", 1)
                    break

                # if not declaration, no extraction will be done and regex will be paired with result
                lexemes_table.append([result.group(), all_regexes[regex]])
                
                # replaces match with space to exclude from next iteration
                line = line.replace(result.group(), " ", 1)
                break
    
    # separates lines in the lexeme table
    if (not emptyCheck and not multiline) and TLDRCheck == None:
        lexemes_table.append(["\\n", "new_line"])