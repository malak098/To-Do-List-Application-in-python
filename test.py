
from datetime import datetime
import json
import os

# User input patterns for different actions (e.g., show, create, edit, delete, exit)
User_input_show=["s","show","sh","sho"]
User_input_create=["c","create","cr","cre","crea","creat","new","add","a","ad"]
User_input_edit=["ed","edit","sh","edi","update","updated","up"]
User_input_delete=["dell","delete","d","del","delet"]
User_input_exit=["ex","","exit","exi","fenish","fin","end"]
#List of task statuses
statuses=["pending","ongoing","finished"]
User_input_status_pending=["p","pen","pend","pendi","pendin"]
User_input_status_ongoing=["o","on","ong","ongo","ongoi","ongoin","continue","con"]
User_input_status_finished=["finish","end","f","fi","fin","fini","finis","finishe"]


#Function to prompt the user with a Yes/No question and return their response as a boolean
def Message(message):
   while True:
      response= input(f'Do you want to {message}?[Yes/No] ').lower()
      if response =="yes":
         return True
      elif response =="no":
         return False
      else:
         print("Invalid income,please enter either\" yes\" or \" no \".")
         print("---------------------------------------------------------------------")
         


# Function to display task details (title, description, status, deadline, and priority)
def Task_detail(Task): 
   
   today = datetime.now() # Current time to calculate remaining days for deadlines
   print(f"Title: {Task['title']}")
   print(f"Description: {Task['description']}")
   print(f"Status: {Task['status']}")

   # Check task status and display additional info for deadlines
   if not Task['status']=="finished":
         
      print(f"Deadline: {Task['deadline']}")   
      days_left = (Task['deadline'] - today).days   # Calculate the remaining days until the deadline
      print("The remaining days are: ",days_left)
      # Determine task priority based on how close the deadline is
      if 0 <= days_left <= 7:
         print("The priority of this task is high") #Assume that if I have days less than 8 days,the task will have high priority 
      elif 8 <= days_left <= 15:
         print("The priority of this task is medium")# Assume that if I have days between [8-15] days,the task will have medium priority
      else:
         print("The priority of this task is low")# Assume that if I have days larger than 15 days,the task will have low priority
   print("*****************************************************************")



""" User can edit or delete by entering task number or title"""
# Function to check if a task index is valid (exists in the task list)
def Check_index(index):
   
   if index in range(0,len(Tasks)) :
      return True
   else:
      return False

#Function to check if a task title exists in the task list and return matching indexes
def Check_title(title):
   indexes=[] # To store indexes for tasks with matching titles 
   for index,Task in enumerate(Tasks):
      for key,value in Task.items():
            if key=='title':
              res=value.lower().find(title)
              if res>=0:
                indexes.append(index)
   return indexes

  
#Function to check and set the task status based on user input   
def Check_status():
   while True:
      status=input("Please,enter the task status [pending, ongoing ,finished]: ").lower().strip()
      if status in statuses:
          return status
      elif status in User_input_status_pending: 
         return "pending"
      elif status in User_input_status_ongoing: 
         return "ongoing"
      elif status in User_input_status_finished: 
         return "finished"
      else:
         print("Try again, Invalid  status")

# Function to validate and return a user-provided deadline (in proper format and future date)
def Check_deadline():
   while True:
         user_deadline=input("Please,Enter a deadline (YYYY-MM-DD HH:MM:SS): ")
         try:
            deadline=datetime.strptime(user_deadline,"%Y-%m-%d %H:%M:%S")
            if deadline < datetime.now():
               print("Invalid deadline! Deadline  must be greater than today's date.")
            else:
               break
         except ValueError:
            print("Invalid date format! Please enter the deadline in YYYY-MM-DD HH:MM:SS format.")
   return deadline         

 

# Function to filter and show tasks based on their status (e.g., pending, ongoing, finished)
def Filter_status(status):
   find_status=False # Flag to check if any matching tasks are found
   for task in Tasks:
      if task['status']==status:
         Task_detail(task)
         find_status=True
   if not find_status:
      print(f"There aren\'t any {status} tasks")



# Function to change the status of a task (pending -> ongoing -> finished)
def Change_status(Task):
   
      while True:

         status=Check_status()

         if Task['status']=="finished" and not status=="finished":
            print(f"You can\'t change the status from {Task['status']} to {status}.")
            break

         elif not(Task['status']=="ongoing" and status=="pending"):
            Task['status']=status 
            break 
         else:    
            print(f"You can\'t change the status from {Task['status']} to {status}.")
      
      return Task
       


# Function to update an existing task (change its status, deadline, or other fields)
def Task_update(index):
   
   Task=Tasks[index]
   
   if Message("change only the status of a task (pending → ongoing → finished"):
     Task=Change_status(Task)
   else:
      for key in Task.keys():
         if Message(f"change the {key}"):
            if key=='status':
               Task=Change_status(Task)
            elif key=='deadline':
               Task['deadline']=Check_deadline()
            else:
              Task[key]=input(f"Please,enter the new { key} ?")
   Tasks[index]=Task
   print("The task has been updated successfully.\n")
  

# Function to search for a task by number or title
def Task_Search():
    while True:
         search=input("Please,enter the task number or title: ").strip() #.lower().strip()
         message=''
         # Exit search if input is empty
         if search=='':
            return -1  
         # Check if user input is number
         elif search.isnumeric():
            index=int(search)-1
            if Check_index(index):
              return index
            else:
             message='There is no index match the input'
        # Check user input
         else:
            index_tasks=Check_title(search) 
            index_tasks_len=len(index_tasks)
            #There is no index match
            if index_tasks_len==0:
               message='There is no title match the input'
            #There is one match
            elif index_tasks_len==1:
               return index_tasks[0]
            # We have more than one Task
            else:
               print("There are many tasks close to your input:")
               for index in index_tasks:
                  print(f'The task number {index+1} :')
                  task=Tasks[index]
                  Task_detail(task)
               while True:
                  try:
                        index=int(input("Please choose one form the list, enter Task number :"))-1
                        if index in index_tasks:
                           return index
                        else:
                           message='Try_Again,please choose from the list.'
                  except:
                     message='Try_Again,you didn\'t enter a number.'
               
         if  message!='':
           print(message)
           if not Message("try again"):
              return -1
   
# Function to sort tasks based on their deadline and priority (high, medium, low)
def Task_Sort():
   
   # Priority lists
   High_priority = []
   Medium_priority = []
   Low_priority = []
   today=datetime.now()
   # Categorize tasks based on deadline proximity
   for index,Task in enumerate(Tasks):
      for key,value in Task.items():

         if key=="status" and value=="finished":
          break
   
         if key=="deadline":
      
            # Calculate days left for the deadline
            days_left = (value - today).days
            # Categorize tasks based on days left
            if 0 <= days_left <= 7:
               High_priority.append(Task)
            elif 8 <= days_left <= 15:
               Medium_priority.append(Task)
            else:
               Low_priority.append(Task)

   # Display sorted tasks by priority
   if High_priority:
   
      print("----------------------------------------------------------------------------------")
      print("High priority tasks")
      print("----------------------------------------------------------------------------------")
      High_priority.sort(key = lambda x:x['deadline'])
      
      for Task in High_priority:
         Task_detail(Task)
        

   if Medium_priority:
      print("----------------------------------------------------------------------------------")
      print("Medium priority tasks")
      print("----------------------------------------------------------------------------------")
      Medium_priority.sort(key = lambda x:x['deadline'])
      for Task in Medium_priority:
         Task_detail(Task)
        

      
   if Low_priority:
      print("----------------------------------------------------------------------------------")
      print("Low priority tasks")
      print("----------------------------------------------------------------------------------")
      Low_priority.sort(key = lambda x:x['deadline'])
      for Task in Low_priority:
         Task_detail(Task)
        


# Define the file path for saving/loading tasks
file_path = 'Tasks.json'


# Load existing tasks from the file if it exists
if os.path.exists(file_path):
   try:
      # Open the file in read mode and load the tasks from JSON format
      with open(file_path, 'r') as Tasks_file:
            Tasks = json.load(Tasks_file)
            # Convert string field datetime back to datetime objects
            for task in Tasks:
               task['deadline'] = datetime.strptime(task['deadline'], "%Y-%m-%d %H:%M:%S")

      print("---------------------------------------------------------------------\n")
      print("Tasks have been loaded from the file.\n")
   except Exception as e:
      print("---------------------------------------------------------------------\n")
      print(f"Error loading tasks from file: {e}")
      quit()
      
else:
   print("No task file found, starting with an empty task list.\n")



# Infinite loop that repeatedly prompts the user for input until they decide to exit
while True:

    # Display the main menu options to the user
    print("---------------------------------------------------------------------")
    print("Please,enter 'add' to add a new task.")
    print("Please,enter 'show' to Show all tasks.")
    print("Please,enter 'edit' to edit an existing task.")
    print("Please,enter 'delete' to delete an existing task.")
    print("Please,enter 'exit' or press enter to exit the program.")
    select=input("Please,enter your choose: ").lower().strip()
    print("\n")

   # If user chooses 'add', prompt for task details and create a new task
    if select in User_input_create:

      print("-----------------------------Create a task----------------------------")
      name=input("Please,enter the task title: ")
      description=input("Please,enter the task description: ")
      deadline=Check_deadline()
      status=Check_status()
            
     # Create a new task dictionary and append it to the tasks list
      new_task={"title":name ,"description":description,"status":status,"deadline":deadline}
      Tasks.append(new_task)
      print("The task has been added successfully.\n") 


 
        
    # If user chooses 'show', display all tasks
    elif select in User_input_show:

      print("-----------------------------Show all tasks--------------------------")
      # Display each task in the list
      for index,Task in enumerate(Tasks):
         print(f'The task number {index+1} :')
         Task_detail(Task)

      # Ask the user if they want to sort tasks by priority
      if Message("Sort tasks by their priority"):
         Task_Sort()
     # Ask the user if they want to filter tasks by status
      if Message("filter the tasks  by their status"):
         status=Check_status()
         Filter_status(status) # Filter tasks by the selected status
           
       



    # If user chooses 'edit', allow them to edit an existing task
    elif select in User_input_edit:

      print("-----------------------------Edit a task--------------------------")
      # Search for the task to edit by ID or title
      index=Task_Search()
      if index>=0:
       print(f'The task number {index+1} :')
       Task=Tasks[index]  
       Task_detail(Task)# Show details of the selected task
       
       # Ask the user if they want to edit the task
       if Message('edit this task'):
        Task_update(index) # Update the selected task
       else:
          print("Good Luck")
       
      else:
         print("Please,Try_Again Later")
              
                  

   # If user chooses 'delete', allow them to delete an existing task
    elif select in User_input_delete:
      
      print("-----------------------------Delete a task--------------------------")
      # Search for the task to delete by ID or title
      index=Task_Search()
      if index>=0:
       print(f'The task number {index+1} :')
       Task=Tasks[index]  
       Task_detail(Task)# Show details of the selected task

       # Ask the user if they want to delete the task
       if Message('delete this task'):
        Tasks.pop(index) # Remove the task from the list
        print("The task has been deleted successfully.\n")
       else:
          print("Good Luck")
      else:
         print("Please,Try_Again Later")
      
   # If user chooses 'exit', exit the program
    elif select in User_input_exit : 
        print("---------------------------------------------------------------------")
        print(" Thank you for using me! Work hard! ")
        
        break

   # If user enters an invalid option, show an error message
    else:
       
        print("---------------------------------------------------------------------")
        print(" Invalid income, please enter please enter the correct choice.")

# After the user exits, save the tasks to the file
try:
   with open(file_path, 'w') as Tasks_file:
      # Save the tasks in JSON format, converting datetime objects to string format
      json.dump(Tasks, Tasks_file, default=str, indent=4)
      print("\n Tasks have been saved to the file.")
      print("---------------------------------------------------------------------")
except Exception as e:
   # Handle any errors that occur while saving to the file
   print(f"Error saving tasks to file: {e}")
   print("---------------------------------------------------------------------")