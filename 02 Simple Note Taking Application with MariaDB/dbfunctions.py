import mariadb

#Function for adding new task
def addNewTask(cur):

    #Input and check for task name
    taskName = input("Input New Task Name: ")
    if len(taskName)==0:
        print("Name cannot be empty")
        return

    #Input and check for task Details
    taskDetails = input("Input Task Details: ")
    if len(taskDetails)==0:
        print("Details cannot be empty")
        return

    #Input and check for task deadline
    taskDate = input("Input Task Deadline (Format: YYYY-MM-DD): ")

    #Try block for adding new task
    try:
        cur.execute(f'INSERT INTO task(task_name, task_details, task_deadline) VALUES ("{taskName}", "{taskDetails}", "{taskDate}");')
    except mariadb.Error as e:
        print(f"Error with adding task: {e}")
        print("Please try again!")
        return

    print("Task successfully added!")

#Function for adding new Task
def editTask(cur):

    #Checks if task id is in database
    taskids =[]
    cur.execute('SELECT task_id from task;')
    for task_id in cur:
        taskids.append(task_id[0])

    if len(taskids)==0:
        print("No tasks in database")
        return

    #Task selector, shows all possible tasks to select
    viewAllTasks(cur)
    try:
        taskToEdit = int(input("Input Task ID of task to edit: "))
    except:
        print("Invalid task number, please try again")
        return    

    if taskToEdit not in taskids:
        print("Task Id not in database! Please try again")
        return

    #Block for editing task name value
    newTaskName = input("Input new task name (Leave empty if not changing): ")
    if len(newTaskName) != 0:
        try:
            cur.execute(f'UPDATE task SET task_name= "{newTaskName}" WHERE task_id= {taskToEdit};')
            print("Successfully Updated Name!")
        except mariadb.Error as e:
            print(f"Error updating: {e}")
            return

    #Block for editing task details value
    newTaskDetails = input("Input new task details (Leave empty if not changing): ")
    if len(newTaskDetails) != 0:
        try:
            cur.execute(f'UPDATE task SET task_details= "{newTaskDetails}" WHERE task_id= {taskToEdit};')
            print("Successfully Updated Details!")
        except mariadb.Error as e:
            print(f"Error updating: {e}")
            return
    
    #Block for editing task deadline value
    newTaskDeadline = input("Input new task deadline (Leave empty if not changing): ")
    if len(newTaskDeadline) != 0:
        try:
            cur.execute(f'UPDATE task SET task_deadline= "{newTaskDeadline}" WHERE task_id= {taskToEdit};')
            print("Successfully Updated Deadline!")
        except mariadb.Error as e:
            print(f"Error updating: {e}")
            return

    #Block for editing task status value
    newTaskStatus =  input("Input new task status (0 = Unfinished 1 = Finished): ")
    if newTaskStatus == "0":
        try:
            cur.execute(f'UPDATE task SET task_status= "Unfinished" WHERE task_id= {taskToEdit};')
            print("Successfully Updated Status!")
        except mariadb.Error as e:
            print(f"Error updating: {e}")
            return
    elif newTaskStatus == "1":
        try:
            cur.execute(f'UPDATE task SET task_status= "Finished" WHERE task_id= {taskToEdit};')
            print("Successfully Updated Status!")
        except mariadb.Error as e:
            print(f"Error updating: {e}")
            return
    else:
        print("Not in choices, status left unchanged")

    #Block for editing category, checks first if there are any categories
    categoryids =[]
    cur.execute('SELECT category_id from category;')
    for category_id in cur:
        categoryids.append(category_id[0])

    if len(categoryids)==0:
        print("Finished Updating!")
        return

    viewCategory(cur)
    newTaskCategory  = input("Input new task category id (Leave empty if not changing, type 'none' if removing category): ")
    if newTaskCategory == 'none':
        cur.execute(f'UPDATE task SET category_id=null WHERE task_id={taskToEdit};')
    elif len(newTaskCategory)!=0:
        try:
            cur.execute(f'UPDATE task SET category_id={int(newTaskCategory)} WHERE task_id={taskToEdit};')
        except mariadb.Error as e:
            print(f"Error updating: {e}")
            return
    

    print("Finished updating!")


#Function for deleting tasks
def deleteTask(cur):
    #Checks if task id exists
    taskids =[]
    cur.execute('SELECT task_id from task;')
    for task_id in cur:
        taskids.append(task_id[0])

    if len(taskids)==0:
        print("No tasks in database")
        return

    #Input for task id
    viewAllTasks(cur)
    try:
        taskToDelete = int(input("Input Task ID of task to delete: "))
    except:
        print("Invalid task number, please try again")
        return

    if taskToDelete not in taskids:
        print("Task Id not in database! Please try again")
        return

    cur.execute(f"DELETE FROM task WHERE task_id= {taskToDelete};")
    print("Task successfully deleted!")

#Code block for viewing all tasks in a table form
def viewAllTasks(cur):
    #List that takes all the tasks
    tasks = []

    #SQL statement for getting all the task values
    cur.execute('SELECT t.task_id, t.task_name, t.task_deadline, t.task_status, coalesce(c.category_name, "None"), t.task_details FROM task t LEFT JOIN category c ON t.category_id = c.category_id;')

    #Loop for putting fetched data into tasks list
    for (task_id, task_name, task_deadline, task_status, category_name, task_details) in cur:
        tasks.append([task_id, task_name, task_deadline, task_status, category_name, task_details])

    #Checks if there are no tasks
    if len(tasks) == 0:
        print("Tasks Empty")
        return

    #Prints tasks table
    print("{:<8} │ {:<15} │ {:<15} │ {:<15} │ {:<10} │ {:<10}".format("Task Id", "Task Name", "Deadline", "Status", "Category", "Details"))
    for row in tasks:
        I, N, DL, S, C, D = row
        print("{:<8} │ {:<15} │ {:<15} │ {:<15} │ {:<10} │ {:<10}".format(I, N, DL.strftime('%m/%d/%Y'), S, C, D))

#Function for finishing a task
def finishTask(cur):

    taskids =[]
    cur.execute('SELECT task_id from task;')
    for task_id in cur:
        taskids.append(task_id[0])
        
    if len(taskids)==0:
        print("No tasks in database")
        return

    #Code block for choosing task to finish
    viewAllTasks(cur)
    try:
        taskToFinish = int(input("Input Task ID of task to finish: "))
    except:
        print("Invalid task number, please try again")
        return    

    if taskToFinish not in taskids:
        print("Task Id not in database! Please try again")
        return

    #Checks if task is already finished
    cur.execute(f'SELECT task_status FROM task WHERE task_id={taskToFinish}')
    if cur.fetchall()[0][0] == "Finished":
        print("Task already finished!")
        return

    #SQL query for changing chosen task to finished
    cur.execute(f'UPDATE task SET task_status= "Finished" WHERE task_id= {taskToFinish};')
    print("Task finished! Congratulations!")


#Function for adding a new Category
def addNewCategory(cur):
    #Block for adding category name
    categoryName = input("Input New Category Name: ")
    if len(categoryName)==0:
        print("Name cannot be empty")
        return
    #Block for adding category description
    categoryDesc = input("Input Category Description: ")
    if len(categoryDesc)==0:
        print("Details cannot be empty")
        return

    #Try block and sql query for creating new category
    try:
        cur.execute(f'INSERT INTO category(category_name, category_desc) VALUES ("{categoryName}", "{categoryDesc}")')
    except mariadb.Error as e:
        print(f"Error with adding task: {e}")
        print("Please try again!")
        return

#Function for editing category details
def editCategory(cur):
    #Category selector, shows all categories to select

    categoryids =[]
    cur.execute('SELECT category_id from category;')
    for category_id in cur:
        categoryids.append(category_id[0])

    if len(categoryids)==0:
        print("No Categories in Database")
        return

    viewCategory(cur)
    try:
        categoryToEdit = int(input("Input Category ID of Category to Edit: "))
    except:
        print("Invalid Category number, please try again")
        return

    if categoryToDelete not in categoryids:
        print("Category Id not in database! Please try again")
        return
    
    #Block for editing name
    newCategoryName = input("Input new category name (Leave empty if not changing): ")
    if len(newCategoryName) != 0:
        try:
            cur.execute(f'UPDATE category SET category_name="{newCategoryName}" WHERE category_id={categoryToEdit};')
            print("Successfully Updated!")
        except mariadb.Error as e:
            print(f"Error updating: {e}")
            return

    #Block for editing Description
    newCategoryDesc = input("Input new category details (Leave empty if not changing): ")
    if len(newCategoryDesc) != 0:
        try:
            cur.execute(f'UPDATE category SET category_desc="{newCategoryDesc}" WHERE category_id={categoryToEdit};')
            print("Successfully Updated!")
        except mariadb.Error as e:
            print(f"Error updating: {e}")
            return

    print("Finished Updating!")

    
#Function for deleting Category
def deleteCategory(cur):
    

    #Checks if category is in database
    categoryids =[]
    cur.execute('SELECT category_id from category;')
    for category_id in cur:
        categoryids.append(category_id[0])

    if len(categoryids)==0:
        print("No Categories in Database")
        return

    #Selector for Category
    viewCategory(cur)
    try:
        categoryToDelete = int(input("Input category ID of task to delete: "))
    except:
        print("Invalid category number, please try again")
        return

    if categoryToDelete not in categoryids:
        print("Category Id not in database! Please try again")
        return

    #SQL Queries, first removes category in all tasks and deletes category
    cur.execute(f"UPDATE task SET category_id=NULL where category_id={categoryToDelete};")
    cur.execute(f"DELETE FROM category WHERE category_id={categoryToDelete};")

    print("Finished Deleting!")

#Views all cateogories
def viewCategory(cur):
    categories = []

    #SQL Query for getting all categories
    cur.execute('SELECT * FROM category')

    #Adds all categories to list
    for (category_id, category_name, category_desc) in cur:
        categories.append([category_id, category_name, category_desc])

    #Checks if categories is empty
    if len(categories) == 0:
        print("Categories Empty")
        return

    #prints categories
    print("{:<8} │ {:<15} │ {:<15} ".format("Id", "Name", "Description"))
    for row in categories:
        I, N, D = row
        print("{:<8} │ {:<15} │ {:<15}".format(I, N, D))

#View tasks by category
def viewCategoryTasks(cur):

    categories = []
    
    cur.execute('SELECT category_id FROM category')

    for (category_id) in cur:
        categories.append(category_id[0])

    if len(categories)==0:
        print("No Categories available")
        return
    
    #Selector for category to view
    viewCategory(cur)
    try:
        categoryToView = int(input("Input Category ID of tasks to view: "))
    except:
        print("Invalid Category number, please try again")
        return

    #Checks if category exists
    if categoryToView not in categories:
        print("Category does not exist")
        return

    #Fetches all tasks with indicated category id
    tasks = []

    cur.execute(f'SELECT task_id, task_name, task_deadline, task_status, task_details FROM task WHERE category_id={categoryToView}')

    for (task_id, task_name, task_deadline, task_status, task_details) in cur:
        tasks.append([task_id, task_name, task_deadline, task_status, task_details])

    if len(tasks) == 0:
        print("No tasks in category")
        return

    #Prints the table
    print("{:<8} │ {:<15} │ {:<15} │ {:<15} │ {:<10}".format("Task Id", "Task Name", "Deadline", "Status", "Details"))
    for row in tasks:
        I, N, DL, S, D = row
        print("{:<8} │ {:<15} │ {:<15} │ {:<15} │ {:<10}".format(I, N, DL.strftime('%m/%d/%Y'), S, D))
    
#Adds task to a category
def addTaskToCategory(cur):

    #Fetches all tasks
    taskids =[]
    cur.execute('SELECT task_id from task;')
    for task_id in cur:
        taskids.append(task_id[0])

    #Checks if there no tasks
    if len(taskids) == 0:
        print("No Tasks yet!")
        return

    #Fetches all categories    
    categoryids =[]
    cur.execute('SELECT category_id from category;')
    for category_id in cur:
        categoryids.append(category_id[0])
        
    #Checks if there are no categories
    if len(categoryids)==0:
        print("No categories yet!")
        return

    #Asks for task to add to a category
    viewAllTasks(cur)
    try:
        taskToEdit = int(input("Input Task ID of task to add to category: "))
    except:
        print("Invalid task number, please try again")
        return
    

    if taskToEdit not in taskids:
        print("Task Id not in database! Please try again")
        return

    #Asks for category
    viewCategory(cur)
    try:
        categoryToAdd = int(input("Input category ID: "))
    except:
        print("Invalid category number, please try again")
        return
    
    if categoryToAdd not in categoryids:
        print("Category Id not in database! Please try again")
        return

    #Executes SQL Query for adding task to category
    cur.execute(f'UPDATE task SET category_id={categoryToAdd} WHERE task_id={taskToEdit};')

    print("Task added to Category!")
