users = {

}
courses = []

active_user = None
#=======================================================================================
def check_password(password):
    alpha = 0
    special_chars = "@#$&-_."
    special = 0
    if len(password) < 16:
        return False
    for char in password:
        if char.isalpha():
            alpha += 1
        if char in special_chars:
            special += 1
    if alpha < 2 or special < 2:
        return False 
    for user in users:
        if users[user]["password"] == password.strip():
            return False
    return True

def decorator_for_register(func):
    def wrapper():
        requirements = """
-user name must be Unique.
-password mst be : 
\t1-16 characters long.
\t2-does not contain user name.
\t3-contain at least 2 letters and 2 special characters such as : (@ # $ & - _ .).
-finally if want to be admin enter YES if not enter NO ."""
        print(requirements)
        func()
    return wrapper

@ decorator_for_register
def register_new_user():
    user_name = input("Please enter your uesr name : ").strip().lower()
    password = input("Please enter your password : ").strip().lower()
    admin_input = input("do you want to register as adime ( yes or no ) :").strip().lower()
    if admin_input == "yes":
        admin = True
    else:
        admin = False

    if user_name not in users and user_name not in password and check_password(password):
        user = {
            "password" : password,
            "admin" : admin, 
            "courses" : {}
        }
        
        users.update({user_name : user})
    else:
        print("username exists or password is invalid !")


def login():
    global active_user,users
    user_name = input("Please enter your uesr name : ").strip().lower()
    password = input("Please enter your password : ").strip().lower()
    for user in users:
        if user_name in users and password == users[user_name]["password"]:
            active_user = user_name
            print("you are loged in")
            break
        else:
            print("username or password is incorrect !")
    
def logout():
    global active_user
    active_user = None
    print("you are loged out")

def decorator_for_user_courses(func):
    def wrapper():
        if users[active_user]["admin"]:
            func()
            print(f"new user courses list : \n {users[admin_input]["courses"]}")
        else:
            func()
            print(f"new user courses list : \n {users[active_user]["courses"]}")
    return wrapper
    


@decorator_for_user_courses
def add_course():
    global admin_input
    print(f"avilable courses {courses}")
    course_input = input("Enter course name here : ").strip().lower()
    if users[active_user]["admin"]:
        admin_input = input("Please enter the user name for user you want to add course for him .").strip().lower()
        if course_input in courses and admin_input in users:
            users[admin_input]["courses"].update({course_input : None})
        else:
            print("something is not correct in your entry !")
    else:
        if course_input in courses:
            users[active_user]["courses"].update({course_input : None})
        else:
            print("something is not correct in your entry !")

@decorator_for_user_courses
def withdraw_course():
    if users[active_user]["admin"]:
        admin_input = input("Please enter the user name for user you want to withdraw course form him .").strip().lower()
        if admin_input in users:
            print(users[admin_input]["courses"])
            removed_course = input(f"choose of {admin_input} courses to remove it ")
            if removed_course in users[admin_input]["courses"]:
                users[admin_input]["courses"].pop(removed_course)
        else:
            print("something is not correct in your entry !")
    else:
        if active_user in users:
            print(users[active_user]["courses"])
            removed_course = input(f"choose of {active_user} courses to remove it ").strip().lower()
            if removed_course in users[active_user]["courses"]:
                users[active_user]["courses"].pop(removed_course)
        else:
            print("something is not correct in your entry !")

def decorator_for_courses_list(func):
    def wrapper():
        print(f"avilable courses list : \n {courses}")
        func()
        print(f"new avilable courses list : \n {courses}")
    return wrapper


@decorator_for_courses_list
def add_new_course():
    if users[active_user]["admin"]:
        course_name = input("Please enter name of new course : ").strip().lower()
        if not course_name in courses:
            courses.append(course_name)
            print("done")
        else:
            print("The course is exists !")

@decorator_for_register
def remove_exists_course():
    if users[active_user]["admin"]:
        course_name = input("Please enter name of course you want to remove it from courses : ").strip().lower()
        if course_name in courses:
            courses.remove(course_name)
            print("done")
        else:
            print("The course is not exists !")


def set_mark():
    if users[active_user]["admin"]:
        admin_input = input("Please enter the user name for user you want to set mark for him : ").strip().lower()
        if admin_input in users:
            print(users[admin_input]["courses"])
            course_input = input("Enter the course you want to set mark for it : ").strip().lower()
            if course_input in users[admin_input]["courses"]:
                mark_input = input("Please enter the mark : ").strip().lower()
                users[admin_input]["courses"][course_input] = float(mark_input)
            else:
                print("something is not correct in your entry !")
        else:
            print("something is not correct in your entry !")


def show_num_users():
    if users[active_user]["admin"]:
        print(f"the total number of users = {len(users)}")


def show_marks():
    if users[active_user]["admin"]:
        for user in users:
            print(user,":")
            print(users[user]["courses"])
            print("="*50)
    else:
        print(users[active_user]["courses"])



def calculate_avg():
    if users[active_user]["admin"]:
        number = 0
        marks = 0
        for course in courses:
            for user in users:
                keys_ = users[user]["courses"].keys()
                for key in keys_:
                    if course == key:
                        number += 1
                        marks += users[user]["courses"][key]
            print(f"{course} course contain {number} of students with AVG = {marks/number}") 
            number = 0
            marks = 0


def delete_account():
    global specific_account
    if users[active_user]["admin"]:
        specific_account = input("you want to delete your account or another user account ?\n (your account ==> M \\ another account ==> A)").strip().lower()
        if specific_account == "m":
            sure = input("are you sure ? \nif you sure enter sure if not enter no : ").strip().lower()
            if sure == "sure":
                print("Thacnk you")
                deleted_user = active_user
                logout()
                users.pop(deleted_user)
                print("account has been deleted")
            else:
                print("Operation canceled.")
        elif specific_account == "a":
            name_account = input("please enter the user name you want to delete his account : ").strip().lower()
            if name_account in users:
                sure = input('are you sure ? \nif you sure enter sure if not enter no : ').strip().lower()
                if sure == "sure":
                    print("Thacnk you")
                    users.pop(name_account)
                    print("account has been deleted")
                else:
                    print("Operation canceled.")
            else:
                print("user not exists")
                
    else:
        sure = input('are you sure ? \nif you sure enter sure if not enter no : ').strip().lower()
        user_name = input("enter your user name : ")
        if user_name == active_user:
            if sure == "sure":
                print("Thacnk you")
                logout()
                users.pop(user_name)
                print("account has been deleted")
            else:
                print("Operation canceled.")


def create_account():
    register_new_user()

class system_manager:
    def __enter__(self):
        print("system is runing")
        return self
    
    def __exit__(self, exc_type, exc_val, exe_tb):
        print("you turned off system")

def active():
    if active_user != None:
        if users[active_user]["admin"]:
            return "admin"
        else:
            return "user"
    else:
        return False

def run_the_system():
    with system_manager():
        while True:
            print("="*50)
            command = input("please choose a command : \n[1] register new user.\n[2] log in.\n[3] exit.\nenter here please : ").strip().lower()
            if command == "1":
                register_new_user()
            elif command == "2":
                login()
            elif command == "3":
                print("you are out of the system")
                break
            else:
                print("the command is not exists")
            if active_user:
                while True:
                    if active() == "admin":
                        command_list = """
[1] add new course to courses list
[2] remove course from courses list
[3] show courses list
[4] add course for user
[5] withdraw course from user
[6] show marks and courses
[7] shaw AVG
[8] set mark
[9] show number of users
[10] delete account
[11] create account for user
[12] log out
"""
                        print(command_list)
                        command = input("please choose a command :")
                        print("="*50)
                        if command == "1":
                            add_new_course()
                        elif command == "2":
                            remove_exists_course()
                        elif command == "3":
                            print(courses)
                        elif command == "4":
                            add_course()
                        elif command == "5":
                            withdraw_course()
                        elif command == "6":
                            show_marks()
                        elif command == "7":
                            calculate_avg()
                        elif command == "8":
                            set_mark()
                        elif command == "9":
                            show_num_users()
                        elif command == "10":
                            delete_account()                   
                        elif command == "11":
                            create_account()
                        elif command == "12":
                            logout()
                            break
                        
                        else:
                            print("the command is not exists")
                        print("="*50)

                    elif active() == "user":
                        command_list = """
[1] show courses list                      
[2] add course 
[3] withdraw course
[4] show marks
[5] delete account
[6] log out"""
                        print(command_list)
                        command = input("please choose a command :")
                        print("="*50)
                        if command == "1":
                            print(courses)
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
                            print("the command is not exists")
                        print("="*50)

                    else:
                        break
#=======================================================================================
run_the_system()