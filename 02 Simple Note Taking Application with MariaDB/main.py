# Module Imports
import mariadb
import sys
import time
import dbfunctions

# Instantiate Connection
try:
    print("Attempting Connection to Database")
    conn = mariadb.connect(
    host="127.0.0.1",
    port=3306,
    user="pythonapp",
    password="sirperic0")

except mariadb.Error as e:
      print(f"Error connecting to the database: {e}")
      sys.exit(1)

time.sleep(0.5)

print("Successful connection!\n")

#Gets Cursor and changes to application database
cur = conn.cursor()
cur.execute('use taskapp;')

#Main program loop
while(True):
    print("""
   _____          _____  _        _   _       _            
  / ____|   /\   |  __ \| |      | \ | |     | |           
 | |       /  \  | |__) | |      |  \| | ___ | |_ ___  ___ 
 | |      / /\ \ |  _  /| |      | . ` |/ _ \| __/ _ \/ __|
 | |____ / ____ \| | \ \| |____  | |\  | (_) | ||  __/\__ \\
  \_____/_/    \_\_|  \_\______| |_| \_|\___/ \__\___||___/                                                          
""")
    print("==============================================================")
    print("[1] Add New Task")
    print("[2] Edit Task")
    print("[3] Delete Task")
    print("[4] View All Tasks")
    print("[5] Mark Task as Finished")
    print("[6] Add New Category")
    print("[7] Edit Category")
    print("[8] Delete Category")
    print("[9] View Category")
    print("[10] Add a task to a category")
    print("[0] Exit")
    print("=============")

    try:
        choice = int(input("Choice: "))
    except:
        print("Invalid input! Please try again")
        continue

    if(choice==1):
        dbfunctions.addNewTask(cur)
        conn.commit()
    
    elif(choice==2):
        dbfunctions.editTask(cur)
        conn.commit()
    
    elif(choice==3):
        dbfunctions.deleteTask(cur)
        conn.commit()
    
    elif(choice==4):
        dbfunctions.viewAllTasks(cur)
        
    elif(choice==5):
        dbfunctions.finishTask(cur)
        conn.commit()
    
    elif(choice==6):
        dbfunctions.addNewCategory(cur)
        conn.commit()
    
    elif(choice==7):
        dbfunctions.editCategory(cur)
        conn.commit()
    
    elif(choice==8):
        dbfunctions.deleteCategory(cur)
        conn.commit()
    
    elif(choice==9):
        dbfunctions.viewCategoryTasks(cur)
    
    elif(choice==10):
        dbfunctions.addTaskToCategory(cur)
        conn.commit()
    
    elif(choice==0):
        conn.commit()
        conn.close()
        exit()
    
    else:
        print("Invalid input!")
