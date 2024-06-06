import lexer
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from lexer import lexemes_table
from lexer import all_identifiers
import parser_1
import semantic

root = Tk()
root.title('J2S Lolcode Interpreter')
root.geometry('1250x700')  # whole dimension of the screen


# writes lexeme table to output.txt
def output_to_file(table):
    file_handler = open(r'output.txt', "w")
    for x in table:
        file_handler.write(x[0] + " : " + x[1] + "\n")

# displays executed code to the terminal text box
def display_to_terminal():

    terminal["state"] = "normal" # sets terminal to allow writing

    # converts lolcode escape sequences to python 
    semantic.terminal_str = semantic.terminal_str.replace(":)", "\n")
    semantic.terminal_str = semantic.terminal_str.replace(":>", "\t")
    semantic.terminal_str = semantic.terminal_str.replace(":o", "\g")

    terminal.delete(1.0, END)  # delete initial text for overwriting
    terminal.insert(END, semantic.terminal_str)  # displays code in the terminal
    semantic.terminal_str = "" # clears terminal_str in semantic.py
    terminal["state"] = "disabled" # sets terminal to disable editing

# executes program from imported .lol file
def execute_program(filePath):
    
    # clears lexeme and symbol table
    clear_lexeme_table()
    clear_symbol_table()

    # identifies lexemes from input file
    lines = (filePath).split('\n')
    for line in lines:
        lexer.identify_lexemes(line)

    result = parser_1.parser(lexemes_table) # parses the lexemes from the table
    
    if result != parser_1.CORRECT: # if error occurs in parsing
        # prints out the error in terminal
        print(result) 
        semantic.terminal_str = str(result)
    else:
        semantic.interpreter(lexemes_table) # calls the interpreter if there are no errors in parsing
        display_lexeme_table() # displays lexemes to the GUI
        display_symbol_table() # displays symbol table to the GUI
    
    output_to_file(lexemes_table) # writes identified lexemes to output.txt
    display_to_terminal() # displays output in terminal text box

def clear_lexeme_table():

    global lexemes_table
    lexemes_table.clear() # retrieves lexeme table and clears

    # deletes the contents of the treeview
    for item in lexemes_treeview.get_children():
        lexemes_treeview.delete(item)
    
    root.update() # updates the window

def clear_symbol_table():

    global all_identifiers
    all_identifiers.clear() # retrieves lexeme table and clears

    # deletes the contents of the treeview
    for item in symbol_table_treeview.get_children():
        symbol_table_treeview.delete(item)
    
    root.update() # updates the window

# prints lexeme and classification in a treeview widget
def display_lexeme_table():

    # retrieves elements from lexeme table and appends to the treeview
    for i in range(len(lexemes_table)):
        if(lexemes_table[i][0] == "\\n"): # excludes newline in lexeme table
            continue
        lexemes_treeview.insert(parent='', index='end', iid=i, text='', # inserts lexeme and classification to the treeview
                                values=(lexemes_table[i][0], lexemes_table[i][1]))
    
# prints variable and value in a treeview widget
def display_symbol_table():  
    
    # converts dictionary keys and values to lists for easier accessing
    identifiers = list(all_identifiers.keys())
    values = list(all_identifiers.values())

    for i in range(len(all_identifiers)):
        symbol_table_treeview.insert(parent='', index='end', iid=i, text='', 
                                values=(identifiers[i], values[i])) # inserts variable and value to the treeview

def import_file():

    # clears lexeme and symbol table
    clear_lexeme_table()
    clear_symbol_table()

    # clears terminal text box and terminal output string
    terminal["state"] = "normal"
    terminal.delete(1.0, END)
    terminal["state"] = "disabled"
    semantic.terminal_str = ""

    # displays file dialog
    root.filename = filedialog.askopenfilename(
        initialdir="/sample", title="Select A File", filetypes=(("LOLcode files", "*.lol"), ("All files", "*.*")))
    code_editor.delete('1.0', END)  # clears code editor text box
    
    try: # checks if file is imported
        text_file = open(root.filename, 'r')
        code = text_file.read()
        code_editor.insert(END, code)  # displays the code in the code editor text box
        text_file.close()
    except:
        print("No file has been selected.") # catches if ever cancel has been selected in the file dialog

# GUI WIDGETS AND ELEMENTS

open_button = Button(root, text="Open File", command=import_file).place(
    x=10, y=10)  

code_editor = Text(root, font=("Helvetica", 8))
code_editor.place(x=10, y=50)

execute_button = Button(root, text="Execute", command=lambda: execute_program(
    code_editor.get('1.0', END))).place(x=10, y=400)

lexemes_treeview = ttk.Treeview(root)
lexemes_treeview.place(x=500, y=50)

lexemes_treeview['columns'] = ('lexemes', 'classification')
lexemes_treeview.column("#0", width=0,  stretch=NO)
lexemes_treeview.column("lexemes", anchor=CENTER, width=175)
lexemes_treeview.column("classification", anchor=CENTER, width=175)

lexemes_treeview.heading("#0", text="", anchor=CENTER)
lexemes_treeview.heading("lexemes", text="Lexemes", anchor=CENTER)
lexemes_treeview.heading(
    "classification", text="Classification", anchor=CENTER)

symbol_table_treeview = ttk.Treeview(root)
symbol_table_treeview.place(x=860, y=50)

symbol_table_treeview['columns'] = ('identifier', 'value')
symbol_table_treeview.column("#0", width=0,  stretch=NO)
symbol_table_treeview.column("identifier", anchor=CENTER, width=175)
symbol_table_treeview.column("value", anchor=CENTER, width=175)

symbol_table_treeview.heading("#0", text="", anchor=CENTER)
symbol_table_treeview.heading("identifier", text="Identifier", anchor=CENTER)
symbol_table_treeview.heading(
    "value", text="Value", anchor=CENTER)

terminal = Text(root, font=("Helvetica", 8), state="disabled")
terminal.place(x=10, y=440, height = 200, width = 1000)

root.mainloop()