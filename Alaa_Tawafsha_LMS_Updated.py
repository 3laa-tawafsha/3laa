users = {} # data storage
available_courses = []

active_user = None # save active user

#==================================================================================================================
# registering new user
def check_password(password):
    alpha = 0
    special_chars = "@#$&-_."
    special = 0
    if len(password) < 16: # check password length
        return False
    for char in password: #===================== 
        if char.isalpha():                     #
            alpha += 1                         #
        if char in special_chars:              # ===> check password content
            special += 1                       #
    if alpha < 2 or special < 2:               #
        return False    #=======================
    for user in users:
        if users[user]["password"] == password.strip(): # ===> is the password in storage ?
            return False
    return True  # return True if evrything is ok
def decorator_for_register(func):
    def wrapper():
        requirements = """
-user name must be Unique.
-password mst be : 
\t1-16 characters long.
\t2-does not contain user name.
\t3-contain at least 2 letters and 2 special characters such as : (@ # $ & - _ .).
-finally if want to be admin enter YES if not enter NO ."""
        print(requirements,"\n")
        func()
    return wrapper
@decorator_for_register
def register_new_user():
    user_name = input("Please enter your uesr name : ").strip().lower() # take a username
    password = input("Please enter your password : ").strip().lower() # tale a password
    admin_input = input("do you want to register as adime ( yes or no ) :").strip().lower() # you are admin or not ?
    if admin_input == "yes":  # check if admin
        admin = True
    else:
        admin = False

    if user_name not in users and user_name not in password and check_password(password): # check if user in srtorage pr not and check user name
        user = {                  #=====
            "password" : password,     #
            "admin" : admin,           # ===> new user data
            "courses" : {}             #
        }                        #=====
        
        users.update({user_name : user}) # store new user data
        print("You have successfully registered.\nLog in now .")
    else:
        print("username exists or password is invalid !")
#==================================================================================================================
# log in and log out
def login():
    global active_user # make change at the global variable level
    user_name = input("Please enter your uesr name : ").strip().lower() # take username
    password = input("Please enter your password : ").strip().lower() # take password
    if user_name in users and password == users[user_name]["password"]: # check username and password
        active_user = user_name # change value
        print(f"Hello {user_name} you are loged in successfully .")
    else:
        print("Username or Password is not correct !")
def logout():
    global active_user # make change at the global variable level
    active_user = None # change value
    print("You are loged out successfully .")
#==================================================================================================================
# add and withdraw courses
def decorator_for_user_courses(func):
    def wrapper():
        if users[active_user]["admin"]: # check admin or not : if admin print specific user courses to  choice from it
            func()
            print(f"New user courses list : \n {users[admin_input]["courses"]}") # print courses after func
        else:
            func()
            print(f"New user courses list : \n {users[active_user]["courses"]}") # print activate courses because he is not admin after func
    return wrapper
@decorator_for_user_courses
def add_course():
    global admin_input # make change at the global variable level
    if users[active_user]["admin"]: # check if user admin or not
        admin_input = input("Please enter the user name for user you want to add course for him .").strip().lower() # take username that admin want to add course to him
        print(f"Avilable courses {available_courses}") # print available courses in course list (added by admin)
        course_input = input("Enter course name here : ").strip().lower() # take a available course name
        if course_input in available_courses and admin_input in users: # check if course available and user is exists
            users[admin_input]["courses"].update({course_input : None}) # add course to storsge with mark as None value
        else:
            print("Something is not correct in your entry !")
    else: # if user is not admin :
        print(f"Avilable courses {available_courses}") # print available courses in course list (added by admin)
        course_input = input("Enter course name here : ").strip().lower() # take a available course name
        if course_input in available_courses: # check if course available
            users[active_user]["courses"].update({course_input : None}) # add course to storsge with mark as None value
        else:
            print("Something is not correct in your entry !")
@decorator_for_user_courses
def withdraw_course():
    if users[active_user]["admin"]: # check if user admin or not
        admin_input = input("Please enter the user name for user you want to withdraw course form him .").strip().lower() # take username that admin want to withdraw course from him
        if admin_input in users: # check if user is exists
            print(users[admin_input]["courses"]) # print user courses that admin want to withdraw the course from him
            removed_course = input(f"choose of {admin_input} courses to remove it ") # take course name
            if removed_course in users[admin_input]["courses"]: # check if course in user courses
                users[admin_input]["courses"].pop(removed_course) # withdraw the course 
        else:
            print("Something is not correct in your entry !")
    else: # if user is not admin :
        if active_user in users:
            print(users[active_user]["courses"]) # print user courses
            removed_course = input(f"choose of {active_user} courses to remove it ").strip().lower() # take the course that user want to withdraw it
            if removed_course in users[active_user]["courses"]: # check if taken course in user courses
                users[active_user]["courses"].pop(removed_course) # withdraw the course
        else:
            print("Something is not correct in your entry !")
#==================================================================================================================
# for admin only
# adding and removing course to and from couses list
def decorator_for_courses_list(func):
    def wrapper():
        print(f"Available courses list : \n {available_courses}") # print available course
        func()
        print(f"New available courses list : \n {available_courses}") # print available course after adding new one
    return wrapper
@decorator_for_courses_list
def add_new_course():
    if users[active_user]["admin"]: # check if user is admin or not
        course_name = input("Please enter name of new course : ").strip().lower() # take course name he want to add it
        if not course_name in available_courses: # check if taken course name is exists
            available_courses.append(course_name) # add new course
            print("Adding new course is done .")
        else:
            print("The course is exists !")
@decorator_for_register
def remove_exists_course():
    if users[active_user]["admin"]: # check if user is admin or not
        course_name = input("Please enter name of course you want to remove it from courses : ").strip().lower() # take course name he want to remove it
        if course_name in available_courses: # check if taken course name is exists
            available_courses.remove(course_name) # remove course
            print("Removing a course is done .")
        else:
            print("The course is not exists !")
#==================================================================================================================
# for admin only
# total number of user
def show_num_users():
    if users[active_user]["admin"]: # check if user is admin or not
        print(f"the total number of users = {len(users)}") 
def show_num_users_in_each_course():
    if users[active_user]["admin"]: # check if user is admin or not
        number = 0 # counter to count students number
        for course in available_courses: # loop on available_course
            for user in users: # loop on users
                user_courses = users[user]["courses"].keys() # take user courses kyes
                for user_course in user_courses: # loop on kyes
                    if course == user_course: # if kye is course add 1 to number
                        number += 1
            print(f"{course} course contain {number} of students")
            number = 0 # return the value of a number to zero
#==================================================================================================================
# for admin only
# set user marks and shaw it 
def set_mark():
    if users[active_user]["admin"]: # check if admin or not
        admin_input = input("Please enter the user name for user you want to set mark for him : ").strip().lower() # take user username to set his marks
        if admin_input in users: # check if username in users
            print(users[admin_input]["courses"]) # print user courses
            course_input = input("Enter the course you want to set mark for it : ").strip().lower() # admin will chose of user courses to set mark to it
            if course_input in users[admin_input]["courses"]: # check if course that admin chose it in user courses
                mark_input = float(input("Please enter the mark : ").strip().lower()) # take a value of mark
                if mark_input in range(0,101):
                    users[admin_input]["courses"][course_input] = mark_input # add mark to user
                else:
                    print("The entered mark is invalid .")
            else:
                print("Something is not correct in your entry !")
        else:
            print("Something is not correct in your entry !")
# user and admin can use it ==>
def show_marks():
    if users[active_user]["admin"]: # check if admin or not
        for user in users: # loop on users
            print(user,":",users[user]["courses"],) # print user and his courses and marks
    else: # if not admin
        print(users[active_user]["courses"]) # print user courses and marks
#==================================================================================================================
# for admin only
# calculate AVG
def calculate_avg():
    if users[active_user]["admin"]:
        for course in available_courses: # loop on courses list
            number = 0 
            marks = 0
            for user in users: # loop on users
                user_courses = users[user]["courses"]
                for key in user_courses: # loop on user courses
                    if course == key: # check if key is course
                        number += 1
                        marks += float(users[user]["courses"][key])
            if number > 0:
                print(f"{course.capitalize()} course contain {number} of students with AVG = {marks/number}") 
            else:
                print(f"{course.capitalize()} course contain zero of students with AVG = 0")
#==================================================================================================================
# for admin only
# create account for user
def create_account():
    register_new_user() # use registration function
#==================================================================================================================
# delete exists account
def delete_account():
    global specific_account
    if users[active_user]["admin"]: # check if admin
        specific_account = input("You want to delete your account or another user account ?\nTo delete your account ==> M\nTo delete another account ==> A\nEnter here please : ").strip().lower()
        # specific_account ==> take account that admin want to delete it
        if specific_account == "m": # check if admin want to delete his account
            sure = input("Are you sure ? \nIf you sure enter Sure if not enter No : ").strip().lower() # take confirmation
            if sure == "sure": # check if confirmation is done or not
                print("Thacnk you")
                deleted_user = active_user # take a copy of username of active user
                logout() # log out
                users.pop(deleted_user) # delete the account
                print("Your account has been deleted")
            else:
                print("Operation canceled.")
        elif specific_account == "a": # check if admin want to delete another user account
            name_account = input("Please enter the user name you want to delete his account : ").strip().lower()
            # name_account ==> take username of account that admin want to delete it
            if name_account in users: # check if username in users
                sure = input('Are you sure ? \nif you sure enter sure if not enter no : ').strip().lower() # take confirmation
                if sure == "sure": # check if confirmation is done or not
                    print("Thacnk you")
                    users.pop(name_account) # delete the account
                    print("account has been deleted")
                else:
                    print("Operation canceled.")
            else:
                print("User not exists")
                
    else: # if not
        sure = input("If you sure enter Sure if not enter No : \nAre you sure ? ").strip().lower() # take confirmation
        if sure == "sure": # check if confirmation is done or not
            print("Thacnk you")
            user_name = active_user # take a copy of username of active user
            logout() # log out
            users.pop(user_name) # delete user account
            print("Your account has been deleted")
        else:
            print("Operation canceled.")
#==================================================================================================================
# context manager
class system_manager:
    def __enter__(self):
        print("system is runing")
        return self
    
    def __exit__(self, exc_type, exc_val, exe_tb):
        print("you turned off system")
def active():
    if active_user != None: # check if there are user in system
        if users[active_user]["admin"]: # check if user admin
            return "admin"
        else: # if not
            return "user"
    else: # if no user in system
        return False
#==================================================================================================================
# run the system
def run_the_system():
    with system_manager():
        while True:
            print("="*50)
            command = input("please choose a command : \n[1] Register new user.\n[2] Log in.\n[3] Exit.\nEnter number of command here please : ").strip().lower()
            if command == "1":
                register_new_user()
            elif command == "2":
                login()
            elif command == "3":
                print("you are out of the system")
                break
            else:
                print("the command is not exists")
            print("="*50)
            if active_user:
                while True:
                    if active() == "admin":
                        command_list = """
[01] Add new course to courses list.
[02] Remove course from courses list.
[03] Show courses list.
[04] Add course for user.
[05] Withdraw course from user.
[06] Show totla number of users.
[07] Show number of users in each course.
[08] Set mark.
[09] Show courses and marks.
[10] Calculate the average.
[11] Create account for new user.
[12] Delete accont.
[13] Log out"""
                        print(command_list)
                        command = input("Please choose a command :")
                        print("="*50)
                        if command == "1":
                            add_new_course()
                        elif command == "2":
                            remove_exists_course()
                        elif command == "3":
                            print(available_courses)
                        elif command == "4":
                            add_course()
                        elif command == "5":
                            withdraw_course()
                        elif command == "6":
                            show_num_users()
                        elif command == "7":
                            show_num_users_in_each_course()
                        elif command == "8":
                            set_mark()
                        elif command == "9":
                            show_marks()
                        elif command == "10":
                            calculate_avg()                   
                        elif command == "11":
                            create_account()
                        elif command == "12":
                            delete_account()
                        elif command == "13":
                            logout()
                            break
                        else:
                            print("The command is not exists")
                        print("="*50)

                    elif active() == "user":
                        command_list = """
[1] Show courses list                      
[2] Add course 
[3] Withdraw course
[4] Show courses and marks
[5] Delete account
[6] Log out"""
                        print(command_list)
                        command = input("Please choose a command :")
                        print("="*50)
                        if command == "1":
                            print(available_courses)
                        elif command == "2":
                            add_course()
                        elif command == "3":
                            withdraw_course()
                        elif command == "4":
                            show_marks()
                        elif command == "5":
                            delete_account()
                        elif command == "6":
                            logout()
                            break                       
                        else:
                            print("The command is not exists")
                        print("="*50)

                    else:
                        break 
#==================================================================================================================
run_the_system()



































































