""" 	Task [  
       index (id),
        title,
        description,
        status,in:(pending, ongoing, finished)
        ]
"""
Tasks=[{"title":"Python 1","description":"I have homework","status":"pending"},{"title":"C#","description":"I have exam","status":"ongoing"},
{"title":"Java ","description":"final exam","status":"finished"},{"title":"C++","description":"I have final","status":"pending"} ]

User_input_show=["s","show","sh","sho"];
User_input_create=["c","create","cr","cre","crea","creat","new","n","add","a","ad"];
User_input_edit=["ed","edit","sh","edi","update","updated","up"];
User_input_delete=["dell","delete","d","del","delet"];
User_input_exit=["ex","","exit","exi","fenish","fin","end"];
statuses=["pending","ongoing","finished"];
User_input_status_pending=["pending","p","pen","pend","pendi","pendin"]
User_input_status_ongoing=["ongoing","o","on","ong","ongo","ongoi","ongoin","continue","con"]
User_input_status_finished=["finished","finish","end","f","fi","fin","fini","finis","finishe"]


#Check user input (number or index) if it exists in our list
def Check_index(index):
   
   if index in range(0,len(Tasks)) :
      return True
   else:
      return False

#Check user input (title) if it exists in our list
def Check_title(title):
   indexes=[] #to store index for titles that have similar title 
   for index,Task in enumerate(Tasks):
      for key,value in Task.items():
            if key=='title':
              res=value.lower().find(title)
              if res>=0:
                indexes.append(index)
   return indexes
  

def Check_status():
   User_input_status=""
   status_input=input("Please,enter the task status [pending, ongoing ,finished]: ").lower().strip()
  
   if status_input in User_input_status_pending:
      User_input_status="pending"
   elif status_input in User_input_status_ongoing:
      User_input_status="ongoing"
   elif status_input in User_input_status_finished:
      User_input_status="finished"
   else:
      User_input_status=""
   return User_input_status
 

def Filter_status(status):
   find_status=False # if there is no status matching
   for index,Task in enumerate(Tasks):
      for key,value in Task.items():
         if key=='status'and value==status:
            Task_detail(index)
            find_status=True
   if not find_status:
      print(f"There aren\'t any {status} tasks")



def Change_status(Task):
      status=Check_status()
      if status in statuses:
         for key,value in Task.items():
            if key=='status':
               #change the status of a task (pending → ongoing → finished)
               if not value=="finished" and not(value=="ongoing" and status=="pending"):#value==status and not(value=="pending" and status=="finished"
                  Task[key]=status  
               else:    
                  print(f"You can\'t change the status from {value} to {status}.")            
      else:
         print("Error,invalid status. Try Again.\n")
      return Task





def Task_detail(index):
   
   Task=Tasks[index]
   print(f'The task number {index+1} :')
   for key,value in Task.items():
         print(f'{key} : {value} ')
   print("*****************************************************************")



# To ask user if he want continue /edit / delete
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
         

def Task_update(index):
   
   Task=Tasks[index]
   
   if Message("change only the status of a task (pending → ongoing → finished"):
     Task=Change_status(Task)
   else:
      for key,value in Task.items():
         if Message(f"change the {key}"):
            if key=='status':
               Task=Change_status(Task)
            else:
              Task[key]=input(f"Please,enter the new { key} ?")
   Tasks[index]=Task
   print("The task has been updated successfully.\n")
  

def Task_Search():
    while True:
         search=input("Please,enter the task number or title: ")
         message=''
         # if user enter space or press enter, it will exit from loop 
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
                  Task_detail(index)
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
   


#This creates an infinite loop that will repeatedly prompt the user for input until they decide to exit.
while True:

    #User Prompt
    print("---------------------------------------------------------------------")
    print("Please,enter 'add' to add a new task.")
    print("Please,enter 'show' to Show all tasks.")
    #New Tasks
    print("Please,enter 'edit' to edit an existing task.")
    print("Please,enter 'delete' to delete an existing task.")
    #End
    print("Please,enter 'exit' or press enter to exit the program.")
    select=input("Please,enter your choose: ").lower().strip()
    print("\n")


    if select in User_input_create:

      # Add a task
      print("-----------------------------Create a task----------------------------")
      name=input("Please,enter the task title: ")
      description=input("Please,enter the task description: ")
      status=Check_status()
      if status in statuses:
         new_task={"title":name ,"description":description,"status":status}
         Tasks.append(new_task)
         print("The task has been added successfully.\n")
      else:
         print("Error,invalid status. Try Again.\n")
        
      
        
    
    elif select in User_input_show:

      print("-----------------------------Show all tasks--------------------------")
      # Show all tasks
      for index in range(0,len(Tasks)):
         Task_detail(index)
      if Message("filter the tasks  by their status"):
         status=Check_status()
         if status in statuses:
            Filter_status(status)
         else:
            print("Error,invalid status. Try Again.\n")



   
    elif select in User_input_edit:

      print("-----------------------------Edit a task--------------------------")
      
      index=Task_Search()
      if index>=0:
       Task_detail(index)
       if Message('edit this task'):
        Task_update(index)
       else:
          print("Good Luck")
       
      else:
         print("Please,Try_Again Later")
              
                  


    elif select in User_input_delete:
      
      print("-----------------------------Delete a task--------------------------")

      index=Task_Search()
      if index>=0:
       Task_detail(index)
       if Message('delete this task'):
        Tasks.pop(index)
        print("The task has been deleted successfully.\n")
       else:
          print("Good Luck")
      else:
         print("Please,Try_Again Later")
      
      
   




    elif select in User_input_exit : 
        print("---------------------------------------------------------------------")
        print(" Thank you for using me! Work hard! ")
        print("---------------------------------------------------------------------")
        break

    else:
        print("---------------------------------------------------------------------")
        print(" Invalid income, please enter please enter the correct choice.")
