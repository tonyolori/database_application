import sqlite3
from tkinter import *


global user_status


def show_instructor():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("select * from instructor")
      items = c.fetchone()

      while items is not None:
            for item in items:
                  print(item, end=" ")
            items = c.fetchone()
            print()
      conn.close()


def show_creds():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("select * from creds")
      items = c.fetchone()

      while items is not None:
          for item in items:
              print(item, end=" ")
          items = c.fetchone()
          print()
      conn.close()
      items = get_creds()
      print(items)
      for item in items:
            for i in item:
                  print(i, end=" ")
            print()


def get_creds(user_state):
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute(
          "select username,password from creds where user_state = ?", (user_state,))
      items = c.fetchall()  # [(194234,sand,3)]
      conn.close()

      return items


def get_student_courses(username):
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute(
          "select course_id from takes where yr= 2021 and id = ?", (username,))
      items = c.fetchall()
      conn.close()
      return items


def get_instructor_courses(username):
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute(
          "select course_id from teaches where yr= 2021 and id = ?", (username,))
      items = c.fetchall()
      conn.close()
      return items


def get_other_students(course):
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT takes.id,name from takes,student where student.id = takes.id and yr= 2021 and course_id = ?", (course,))
      items = c.fetchall()
      conn.close()
      return items


def get_name(username):
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      if user_status == 2:
            c.execute("SELECT name from instructor where id= ?", (username,))
      elif user_status == 3:
            c.execute("SELECT name from student where id= ?", (username,))
      items = c.fetchone()
      conn.close()
      return items


def get_student_department(student_id):
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT dept_name from student where id= ?", (student_id,))
      item = c.fetchone()
      conn.close()
      return item


def get_instructor_department(instructor_id):
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT dept_name from instructor where id= ?", (instructor_id,))
      items = c.fetchone()
      conn.close()
      return items


def get_course_details(course):
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT * from course where course_id = ?", (course,))
      items = c.fetchone()
      conn.close()
      return items


def get_course_list():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT course_id,title,dept_name from course ")
      items = c.fetchall()
      conn.close()
      return items


def get_instructor_list():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT * from instructor ")
      items = c.fetchall()
      conn.close()
      return items


def get_student_list():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT * from student ")
      items = c.fetchall()
      conn.close()
      return items


def get_teaches_list():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT * from teaches ")
      items = c.fetchall()
      conn.close()
      return items


def get_teaches_list_with_names():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT dept_name,course_id,semester,instructor.id,name from teaches,instructor where instructor.id = teaches.id  and yr =2021")
      items = c.fetchall()
      conn.close()
      return items


def get_advisor_list():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT i_id,instructor.name,s_id,student.name from advisor,instructor,student where advisor.i_id=instructor.id and advisor.s_id=student.id")
      items = c.fetchall()
      conn.close()
      return items


def get_department_list():
      conn = sqlite3.connect("db1.db")

      c = conn.cursor()
      c.execute("SELECT * from department ")
      items = c.fetchall()
      conn.close()
      return items


# END OF GET RELATED FUNCTIONS

# BEGIN OF ADD RELATED FUNCTIONS

def add_course(course_id, title, dept_name,credits):
      conn = sqlite3.connect("db1.db")
      c = conn.cursor()

      department_list = get_department_list()


      flag = 0
      # department validation
      for d in department_list:
            #this converts all letters to lowercase to avoid errors if the user provides a correct entry
            #but is inconsistent with the formatting present in the database
            if (d[0].lower()) == (dept_name.lower()): 
                  flag=1
                  dept_name = d[0] #this replaces the user input with a version consistent with the database
      if flag == 0:
            clear_text_widget()
            print_to_widget(
                "Invalid department name, Assign a valid department name")
            return

      try:
            c.execute("INSERT INTO course(course_id,title,dept_name,credits) VALUES (?,?,?,?)",
                (course_id, title, dept_name, credits))

      except Exception as e:
            text_widget.delete("1.0", END)
            print_to_widget(e)

      else:
            clear_text_widget()
            print_to_widget("Addition successful")

      conn.commit()
      conn.close()


def add_instructor(instructor_id, name, dept_name, salary):
      conn = sqlite3.connect("db1.db")
      c = conn.cursor()

      instructor_list = get_instructor_list()
      department_list = get_department_list()

      flag = 0
      # instructor validation
      if instructor_id.isnumeric():
            flag = 1

      if flag == 0:
            clear_text_widget()
            print_to_widget(
                "Invalid instructor id, Assign a valid instructor id")
            return

      flag = 0
      # department validation
      for d in department_list:
            #this converts all letters to lowercase to avoid errors if the user provides a correct entry
            #but is inconsisten with the formatting present in the database
            if (d[0].lower()) == (dept_name.lower()): 
                  flag=1
                  dept_name = d[0] #this replaces the user input with a version consistent with the database
      if flag == 0:
            clear_text_widget()
            print_to_widget(
                "Invalid department name, Assign a valid department name")
            return

      try:
            c.execute("INSERT INTO instructor(id,name,dept_name,salary) VALUES (?,?,?,?)",
                      (instructor_id, name, dept_name, salary))

      #any other sqlite errors are reported to the user 
      except Exception as e:
            text_widget.delete("1.0", END)
            print_to_widget(e)
      else:
            clear_text_widget()
            print_to_widget("Addition successful")

      conn.commit()
      conn.close()


def add_student(student_id, name, dept_name):
      conn = sqlite3.connect("db1.db")
      c = conn.cursor()

      student_list = get_student_list()
      department_list = get_department_list()

      flag = 0
      # student validation
      if student_id.isnumeric():
            flag = 1

      if flag == 0:
            clear_text_widget()
            print_to_widget(
                "Invalid student id, Assign a valid student number")
            return

      flag = 0
      # department validation
      for d in department_list:
            #this converts all letters to lowercase to avoid errors if the user provides a correct entry
            #but is inconsisten with the formatting present in the database
            if (d[0].lower()) == (dept_name.lower()): 
                  flag=1
                  dept_name = d[0] #this replaces the user input with a version consistent with the database
      if flag == 0:
            clear_text_widget()
            print_to_widget(
                "Invalid department name, Assign a valid department name")
            return

      try:
            c.execute("INSERT INTO student(id,name,dept_name) VALUES (?,?,?)",
                      (student_id, name, dept_name))

      except Exception as e:
            text_widget.delete("1.0", END)
            print_to_widget(e)
      else:
            clear_text_widget()
            print_to_widget("Addition successful")

      conn.commit()
      conn.close()

def add_to_teaches(teaches_id, course_id, sec_id):
      conn=sqlite3.connect("db1.db")
      c=conn.cursor()

      course_list=get_course_list()
      instructor_list=get_instructor_list()

      flag=0
      # student validation
      for course in course_list:
            if (str(course[0]) == str(course_id)):
                  flag=1

      if flag == 0:
            clear_text_widget()
            print_to_widget("Invalid course id, Assign a valid course")
            return

      flag=0
      # instructor validation
      for i in instructor_list:
            if (str(i[0]) == str(teaches_id)):
                  flag=1
      if flag == 0:
            clear_text_widget()
            print_to_widget("Invalid instructor id, Assign a valid instructor")
            return


      try:
            c.execute('INSERT INTO teaches(id,course_id,sec_id,semester,yr) VALUES (?,?,?,"FALL",2021)',
                (teaches_id, course_id, sec_id))

      except Exception as e:
            text_widget.delete("1.0", END)
            print_to_widget(e)
      else:
            clear_text_widget()
            print_to_widget("Addition successful")

      conn.commit()
      conn.close()


def add_student_to_course(stdno, course):
      conn=sqlite3.connect("db1.db")
      c=conn.cursor()

      try:
            c.execute('INSERT INTO takes(id,course_id,sec_id,semester,yr) VALUES (?,?,100,"FALL",2021)',
                      (stdno, course))

      except Exception as e:
            text_widget.delete("1.0", END)
            print_to_widget(e)

      conn.commit()
      conn.close()


def add_advisor(i_id, s_id):
      conn=sqlite3.connect("db1.db")
      c=conn.cursor()
      flag=0

      student_list=get_student_list()
      instructor_list=get_instructor_list()

      # student validation
      for s in student_list:
            if (str(s[0]) == str(s_id)):
                  flag=1

      if flag == 0:
            clear_text_widget()
            print_to_widget("Invalid student id, Assign a valid student")
            return

      flag=0
      # instructor validation
      for i in instructor_list:
            if (str(i[0]) == str(i_id)):
                  flag=1
      if flag == 0:
            clear_text_widget()
            print_to_widget("Invalid instructor id, Assign a valid instructor")
            return


      s_dept=get_student_department(s_id)
      i_dept=get_instructor_department(i_id)

      if(s_dept != i_dept):
            clear_text_widget()
            print_to_widget(
                "Department names mismatch!\n Please assign advisor to student in the same department")
            return

      try:
            c.execute('INSERT INTO advisor(i_id,s_id) VALUES (?,?)',
                (i_id, s_id))

      except Exception as e:
            clear_text_widget()
            print_to_widget(e)

            conn.close()
            return

      else:
            clear_text_widget()
            print_to_widget("Data inserted successfully")



      conn.commit()
      conn.close()


#END OF ADD RELATED FUNCTIONS




def update_student_name(new_name):
      conn=sqlite3.connect("db1.db")
      c=conn.cursor()

      c.execute("update student set name = ? where id = ?",
                (new_name, Username))

      conn.commit()
      conn.close()

# end of database related definitions




# Function to set focus (cursor)
def focus1(event):
      # set focus on the course_field box
      Password_box.focus_set()



# Function to set focus
def focus2(event):
      # set focus on the sem_field box
      authenticate()


# Function to take data from GUI and input into the creds table
# def insert():

#       # if user not fill any entry
#       # then print "empty input"
#       if (Username_box.get() == "" or
#               Password_box.get() == ""):

#             print("empty input")

#       else:
#             add_login(Username_box.get(), Password_box.get())

#             # call the clear() function
#             clear()
#             # set focus on the name_field box
#             Username_box.focus_set()


# Function to take data from GUI
def authenticate():

      # if user not fill any entry
      # then print "empty input"
      if (Username_box.get() == "" or
              Password_box.get() == ""):

            print("empty input")

      else:
            global Username
            Username = Username_box.get()
            global Password
            Password = Password_box.get()
            # e.g[(194234,sand),(195219,stone)]
            Credentials = get_creds(user_status)

            for login in Credentials:
                  if Username == login[0] and Password == login[1]:
                        error.destroy()
                        frame1.grid_remove()
                        set_view()
                        break
            else:
                  print("wr input")  # remove in final
                  error.grid(row=7, column=3)

            # call the clear() function
            clear()
            # set focus on the name_field box
            Username_box.focus_set()

# Function for clearing the
# contents of text entry boxes
def clear():

      # clear the content of text entry box
      Username_box.delete(0, END)
      Password_box.delete(0, END)



#VERY USEFUL TOOLS

def print_to_widget(string):
      text_widget.insert(END, "%s" % string)

def clear_text_widget():
      text_widget.delete("1.0",END)

def print_items_to_widget(items,no_of_tabs=2):

      if no_of_tabs == 2:
            tabs = "\t\t"
      else:
            tabs="\t"
      text_widget.insert(END,
                         "\n")
      for item in items:
            for i in item:
                  text_widget.insert(END, "%s" % i + tabs)
            text_widget.insert(END, "\n")



# START OF VIEW RELATED FUNCTIONS

def view_courses_registered():
      items = get_student_courses(Username)

      clear_text_widget()
      print_to_widget("Courses")

      print_items_to_widget(items)


def view_courses_assigned():
      items = get_instructor_courses(Username)

      clear_text_widget()
      print_to_widget("Courses this semester")

      print_items_to_widget(items)


def view_other_students_registered():
      clear_text_widget()
      items = get_student_courses(Username)

      for item in items:
            print_to_widget(item)
            result = get_other_students(item[0])
            print_items_to_widget(result)


def view_students_registered():
      clear_text_widget()

      courses = get_instructor_courses(Username)

      for items in courses:
            for item in items:
                  print_to_widget(item)
                  result = get_other_students(item)
                  print_items_to_widget(result)


def view_course_details(course):
      clear_text_widget()

      course_list= get_course_list()
      details = get_course_details(course)

      if details == None:
            clear_text_widget()
            print_to_widget("Error! invalid course id")
            return 
      listname = ['course_id: ', 'course_title: ', 'dept_name: ', 'credits: ']

      for i, item in enumerate(details):
            print_to_widget(listname[i])
            print_to_widget(item)
            print_to_widget('\n')



# this function is used to print a button to the screen to grab the course details and send
# the details to the function that will grab the result from the database and print it

def check_course_details():
      course = Label(frame2, text="Enter course code", anchor="e",bg="#9fafca")
      course.grid(row=4, column=0, pady=(10,0))

      course_value = StringVar

      course_box = Entry(frame2, textvariable=course_value)
      # S_name_box.delete("1.0", "end")

      # commands to print the current student name to the box
      # course_id = get_name(Username)

      course_box.grid(row=5, column=0, ipadx="30",pady=(5,0))
      course_box.bind(
          "<Return>", lambda event: view_course_details(course_box.get()))

      Button(frame2, text="submit", relief="sunken", bg="#4d648c",
             command=lambda: view_course_details(course_box.get())
             ).grid(row=6, column=0, pady=(10,0))

def student_registration():

      std_no_value = StringVar
      course_value = StringVar

      std_no = Label(frame2, text="Enter student number", anchor="e",bg="#9fafca")
      std_no.grid(row=8, column=0, pady=(10,0))
      std_no_box = Entry(frame2, textvariable=std_no_value)
      std_no_box.grid(row=9, column=0, ipadx="30",pady=(5,0))
      course = Label(frame2, text="Enter course code", anchor="e",bg="#9fafca")
      course.grid(row=10, column=0, pady=(10,0))
      course_box = Entry(frame2, textvariable=course_value)
      course_box.grid(row=11, column=0, ipadx="30",pady=(5,0))




      std_no_box.bind("<Return>", lambda event: course_box.focus_set())
      course_box.bind("<Return>", lambda event: add_student_to_course(
          std_no_box.get(), course_box.get()))

      Button(frame2, text="submit", relief="sunken", bg="#4d648c",
             command=lambda: add_student_to_course(std_no_box.get(), course_box.get())).grid(row=12, column=0,pady=(10,3))

###################### faculty functions begin #################

def forget_frame_contents(frame):
      for widget in frame.winfo_children():
            widget.grid_forget()

def set_frame3():
      forget_frame_contents(frame3)
      text_widget.configure(width=70, height=20)
      text_widget.grid(row=0, column=0)

      text_widget.delete("1.0","end")

def add_course_button():
      set_frame3()

      print_to_widget("CURRENT COURSES\n")
      items= get_course_list()
      print_items_to_widget(items)

      course_id = Label(frame3, text="Enter Course ID", anchor="e",bg='#9fafca')
      course_id.grid(row=1, column=0, pady=(5,0), padx=(400,0))
      course_title = Label(frame3, text="Enter Course Title", anchor="e",bg='#9fafca')
      course_title.grid(row=2, column=0,pady=(5,0), padx=(400,0))
      dept_name = Label(frame3, text="Enter Department Name", anchor="e",bg='#9fafca')
      dept_name.grid(row=3, column=0,pady=(5,0), padx=(400,0))
      credits = Label(frame3, text="Enter Credit Value", anchor="e",bg='#9fafca')
      credits.grid(row=4, column=0,pady=(5,0), padx=(400,0))

      course_id_value = StringVar
      course_title_value = StringVar
      dept_name_value = StringVar
      credits_value = IntVar


      course_id_box = Entry(frame3, textvariable=course_id_value)
      course_title_box = Entry(frame3, textvariable=course_title_value)
      dept_name_box = Entry(frame3, textvariable=dept_name_value)
      credits_box = Entry(frame3, textvariable=credits_value)

      course_id_box.grid(row=1, column=1, ipadx="30")
      course_title_box.grid(row=2, column=1, ipadx="30")
      dept_name_box.grid(row=3, column=1, ipadx="30")
      credits_box.grid(row=4, column=1, ipadx="30")

      course_id_box.bind("<Return>", lambda event: course_title_box.focus_set())
      course_title_box.bind("<Return>", lambda event: dept_name_box.focus_set())
      dept_name_box.bind("<Return>", lambda event: credits_box.focus_set())
      credits_box.bind("<Return>", lambda event: add_course(course_id_box.get(),
            course_title_box.get(),dept_name_box.get(),credits_box.get()))


      Button(frame3, text="Submit", bg="#54626f",
             command=lambda: add_course(course_id_box.get(),
            course_title_box.get(),dept_name_box.get(),credits_box.get())).grid(row=5, column=0,pady=(5,0), padx=(400,0))



def add_instructor_button():

      set_frame3()

      print_to_widget("CURRENT INSTRUCTOR\n")
      items= get_instructor_list()
      print_items_to_widget(items)

      instructor_id = Label(frame3, text="Enter Instructor ID", anchor="n", bg="#9fafca")
      instructor_id.grid(row=1, column=0, pady=(5,0), padx=(400,0))
      name = Label(frame3, text="Enter Instructor Name", anchor="n",bg='#9fafca')
      name.grid(row=2, column=0, pady=(5,0), padx=(400,0))
      dept_name = Label(frame3, text="Enter Department Name", anchor="n",bg='#9fafca')
      dept_name.grid(row=3, column=0, pady=(5,0), padx=(400,0))
      salary = Label(frame3, text="Enter Instructor Salary", anchor="n",bg='#9fafca')
      salary.grid(row=4, column=0, pady=(5,0), padx=(400,0))

      instructor_id_value = IntVar
      name_value = StringVar
      dept_name_value = StringVar
      salary_value = IntVar


      instructor_id_box = Entry(frame3, textvariable=instructor_id_value)
      name_box = Entry(frame3, textvariable=name_value)
      dept_name_box = Entry(frame3, textvariable=dept_name_value)
      salary_box = Entry(frame3, textvariable=salary_value)

      instructor_id_box.grid(row=1, column=1, ipadx="30")
      name_box.grid(row=2, column=1, ipadx="30")
      dept_name_box.grid(row=3, column=1, ipadx="30")
      salary_box.grid(row=4, column=1, ipadx="30")

      instructor_id_box.bind("<Return>", lambda event: name_box.focus_set())
      name_box.bind("<Return>", lambda event: dept_name_box.focus_set())
      dept_name_box.bind("<Return>", lambda event: salary_box.focus_set())
      salary_box.bind("<Return>", lambda event: add_instructor(instructor_id_box.get(),
            name_box.get(),dept_name_box.get(),salary_box.get()))


      Button(frame3, text="Submit",bg='#54626f',
             command=lambda: add_instructor(instructor_id_box.get(),
            name_box.get(),dept_name_box.get(),salary_box.get())).grid(row=5, column=0, pady=(5,0), padx=(400,0))


def add_student_button():

      set_frame3()

      print_to_widget("CURRENT STUDENTS\n")
      items= get_student_list()
      print_items_to_widget(items)

      student_id = Label(frame3, text="Enter Student ID", anchor="n",bg='#9fafca')
      student_id.grid(row=1, column=0, pady=(5,0), padx=(400,0))
      name = Label(frame3, text="Enter Student Name", anchor="n",bg='#9fafca')
      name.grid(row=2, column=0, pady=(5,0), padx=(400,0))
      dept_name = Label(frame3, text="Enter Department Name", anchor="n",bg='#9fafca')
      dept_name.grid(row=3, column=0, pady=(5,0), padx=(400,0))

      student_id_value = IntVar
      name_value = StringVar
      dept_name_value = StringVar


      student_id_box = Entry(frame3, textvariable=student_id_value)
      name_box = Entry(frame3, textvariable=name_value)
      dept_name_box = Entry(frame3, textvariable=dept_name_value)


      student_id_box.grid(row=1, column=1, ipadx="30")
      name_box.grid(row=2, column=1, ipadx="30")
      dept_name_box.grid(row=3, column=1, ipadx="30")

      student_id_box.bind("<Return>", lambda event: name_box.focus_set())
      name_box.bind("<Return>", lambda event: dept_name_box.focus_set())
      dept_name_box.bind("<Return>", lambda event: add_student(student_id_box.get(),
            name_box.get(),dept_name_box.get()))


      Button(frame3, text="Submit", bg="#54626f",
             command=lambda: add_student(student_id_box.get(),
            name_box.get(),dept_name_box.get())).grid(row=5, column=0, pady=(5,0), padx=(400,0))



def assign_course_to_instructor_button():

      set_frame3()

      print_to_widget("CURRENT COURSE ASSIGNMENTS\n")
      items= get_teaches_list_with_names()
      print_items_to_widget(items,2)

      instructor_id = Label(frame3, text="Enter Instructor ID", anchor="n",bg='#9fafca')
      instructor_id.grid(row=1, column=0, pady=(5,0), padx=(400,0))
      course_id = Label(frame3, text="Enter Course ID", anchor="n",bg='#9fafca')
      course_id.grid(row=2, column=0, pady=(5,0), padx=(400,0))
      sec_id = Label(frame3, text="Enter Section ID", anchor="n",bg='#9fafca')
      sec_id.grid(row=3, column=0, pady=(5,0), padx=(400,0))

      instructor_id_value = IntVar
      course_id_value = StringVar
      sec_id_value = IntVar


      instructor_id_box = Entry(frame3, textvariable=instructor_id_value)
      course_id_box = Entry(frame3, textvariable=course_id_value)
      sec_id_box = Entry(frame3, textvariable=sec_id_value)


      instructor_id_box.grid(row=1, column=1, ipadx="30")
      course_id_box.grid(row=2, column=1, ipadx="30")
      sec_id_box.grid(row=3, column=1, ipadx="30")

      instructor_id_box.bind("<Return>", lambda event: course_id_box.focus_set())
      course_id_box.bind("<Return>", lambda event: sec_id_box.focus_set())
      sec_id_box.bind("<Return>", lambda event: add_to_teaches(instructor_id_box.get(),
            course_id_box.get(),sec_id_box.get()))


      Button(frame3, text="Submit", bg="#54626f",
             command=lambda:  add_to_teaches(instructor_id_box.get(),
            course_id_box.get(),sec_id_box.get())).grid(row=5, column=0, pady=(5,0), padx=(400,0))

def assign_advisor_button():

      set_frame3()

      print_to_widget("CURRENT ADVISOR PAIRS\n")
      items= get_advisor_list()
      print_items_to_widget(items,1)

      instructor_id = Label(frame3, text="Enter Instructor ID", anchor="n",bg='#9fafca')
      instructor_id.grid(row=1, column=0, pady=(5,0), padx=(400,0))
      student_id = Label(frame3, text="Enter Student ID", anchor="n",bg='#9fafca')
      student_id.grid(row=2, column=0, pady=(5,0), padx=(400,0))

      instructor_id_value = IntVar
      student_id_value = IntVar


      instructor_id_box = Entry(frame3, textvariable=instructor_id_value)
      student_id_box = Entry(frame3, textvariable=student_id_value)


      instructor_id_box.grid(row=1, column=1, ipadx="30")
      student_id_box.grid(row=2, column=1, ipadx="30")

      instructor_id_box.bind("<Return>", lambda event: student_id_box.focus_set())
      student_id_box.bind("<Return>", lambda event: add_advisor(instructor_id_box.get(),
            student_id_box.get()))


      Button(frame3, text="Submit",bg='#54626f',
             command=lambda: add_advisor(instructor_id_box.get(),
            student_id_box.get())).grid(row=5, column=0, pady=(5,0), padx=(400,0))



# end of faculty functions ###############

def manage_student_update(new_name):

      update_student_name(new_name)
      successful = Label(frame2, text="update successful")
      successful.grid(row=7, column=0)


def update_student_details():
      S_name = Label(frame2, text="student name", anchor="e", relief="raised")
      S_name.grid(row=4, column=0, pady=(5,5))

      S_name_value = StringVar

      S_name_box = Entry(frame2, textvariable=S_name_value)
      # S_name_box.delete("1.0", "end")

      # commands to print the current student name to the box
      std_name = get_name(Username)
      S_name_box.insert(END, str(std_name[0]))

      S_name_box.grid(row=5, column=0, ipadx="50")

      Button(frame2, text="Update", relief="raised",
             command=lambda: manage_student_update(S_name_box.get())
             ).grid(row=6, column=0, pady=(5,5))

def update_instructor_details():
      name = Label(frame2, text="instructor name", anchor="e",bg="#9fafca")
      name.grid(row=14, column=0, pady=(10,0))

      name_value = StringVar

      name_box = Entry(frame2, textvariable=name_value)
      # S_name_box.delete("1.0", "end")

      # commands to print the current student name to the box
      i_name = get_name(Username)
      name_box.insert(END, str(i_name[0]))

      name_box.grid(row=15, column=0, ipadx="50", pady=(5,0))

      Button(frame2, text="Update", relief="sunken", bg="#4d648c",
             command=lambda: manage_student_update(name_box.get())
             ).grid(row=16, column=0, pady=(10,0))



def set_student_view():
      table= "student"
      name = Label(frame2, text=f"Welcome, {get_name(Username)[0]}", bg='#9fafca',
                   font="time 15 bold")
      name.grid(row=0, column=0,pady=(250,0))

      Button(frame2, text="view_courses", relief="sunken", bg='#8691B0',
             command=view_courses_registered).grid(row=1, column=0, pady=(10,0))

      Button(frame2, text="See other students registered in the class", relief="sunken", bg='#8691B0',
             command=view_other_students_registered).grid(row=2, column=0, pady=(10,0))

      Button(frame2, text="update personal details", relief="sunken", bg='#8691B0',
             command=update_student_details).grid(row=3, column=0, pady=(10,0))
      set_general_view()




def grid_faculty_frames():
      text_widget.insert(END,"Weclome to the database")

      text_widget.grid(row=0, column=0)

      frame2.grid(row=0, column=1, padx=100, pady=10)#,rowspan=10,columnspan=3, sticky="nw"
      # frame2.grid_propagate(0)
      frame3.grid(row=0, column=0, padx=0, pady=10)#,rowspan=10,columnspan=3


def set_faculty_view():
      name = Label(frame2, text="WELCOME",font="time 15 bold", anchor="n",bg="#9fafca")
      name.grid(row=0, column=0,pady=(0,25))

      Button(frame2, text="add a new course",bg="#d6dbe0",
             command=add_course_button).grid(row=1, column=0,pady=(0,5),ipadx=(9))

      Button(frame2, text="add a new instructor", bg="#dee3eb",
             command=add_instructor_button).grid(row=2, column=0,pady=(0,5))

      Button(frame2, text="add a new student",bg="#d6dbe0",
             command=add_student_button).grid(row=3, column=0,pady=(0,5),ipadx=(9))

      Button(frame2, text="assign a course to an instructor",bg="#dee3eb",
             command=assign_course_to_instructor_button).grid(row=4, column=0,pady=(0,5))

      Button(frame2, text="assign an instructor to a student",bg='#d6dbe0',
             command=assign_advisor_button).grid(row=5, column=0,pady=(0,200))

      grid_faculty_frames()


def set_instructor_view():
      table = "instructor"
      name = Label(frame2, text=f"Welcome, {get_name(Username) [0]}",font="time 15 bold", anchor="n",bg="#9fafca")
      name.grid(row=0, column=0,pady=(100,0))

      Button(frame2, text="View Courses", relief="sunken",
             command=view_courses_assigned).grid(row=1, column=0, pady=(10,0))

      Button(frame2, text="See Other Students Registered In Each Class",relief="sunken", 
             command=view_students_registered).grid(row=2, column=0, pady=(10,0))

      Button(frame2, text="View Course Details",relief="sunken",
             command=check_course_details).grid(row=3, column=0, pady=(10,0)) 

      std_reg= Button(frame2, text="Add A Student To A Class",relief="sunken",
             command=student_registration).grid(row=7, column=0, pady=(10,0))

      Button(frame2, text="Update Personal Details",relief="sunken",
             command=update_instructor_details).grid(row=13, column=0, pady=(10,0))

      set_general_view()

def set_view():
      if user_status == 1:
            set_faculty_view()
      elif user_status == 2:
            set_instructor_view()
      elif user_status == 3:
            set_student_view()


def set_general_view():


      text_widget.grid(row=0, column=0, pady=(20,10), padx=(20,2) )

      frame2.grid(row=0,column=1,pady=10, sticky="nws", padx=(0,100)) # rowspan=10,columnspan=3, sticky="ns")
      # frame2.grid_propagate(0)
      frame3.grid(row=0, column=0,pady=10,sticky="nwes", padx=(0,200) )#,rowspan=10,columnspan=3)



def set_user_status(val):
      global user_status
      user_status=val



def set_begining():
      frame0.grid(row=0,column=0,sticky="nsew")

      frm_3btn.rowconfigure([0,1,2],minsize=50,weight=1)
      frm_3btn.columnconfigure([0,1,2], minsize=50, weight=1)
      frame0.rowconfigure(0, minsize=50, weight=1)
      frame0.rowconfigure(1, minsize=200, weight=1)
      frame0.columnconfigure(0, minsize=50, weight=1)
      frm_sel_welc.columnconfigure(0, minsize=100, weight=1)
      frm_sel_welc.rowconfigure([0,1], minsize=50, weight=1)

      frm_sel_welc.grid(row=0,column=0, sticky="nsew")

      lbl_welcome.grid(row=0,column=0)
      lbl_sel_user.grid(row=1,column=0)

      btn_fc=Button(frm_3btn,text="Faculty \nCordinator",font="times 10 bold",bg="#c7afff",height=5, width=8,command = lambda : [set_login_page(),set_user_status(1)])
      btn_instr=Button(frm_3btn,text="Instructor",font="times 10 bold",bg="#8f60ff", height=5, width=8,command = lambda : [set_login_page(),set_user_status(2)])
      btn_std=Button(frm_3btn,text="Student",font="times 10 bold",bg="#9fafca", height=5, width=8,command = lambda : [set_login_page(),set_user_status(3)])

      frm_3btn.grid(row=1,column=0, sticky="nsew")
      btn_fc.grid(row=1, column=0, padx=10, pady=10)
      btn_instr.grid(row=1, column=1, pady=50,)
      btn_std.grid(row=1, column=2, padx=10, pady=50)

def set_login_page():
      frame0.grid_remove()
      welcome.grid(row=0, column=3)
      Username.grid(row=1, column=2, padx=2)
      Password.grid(row=2, column=2, padx=2)
      Username_box.grid(row=1, column=3, ipadx="100")
      Password_box.grid(row=2, column=3, ipadx="100")
      frame1.grid(row=0, column=0)
      submit.grid(row=8, column=3)



# start of main function

root = Tk()

# Setting the size of the window
root.geometry("%dx%d" % (root.winfo_screenwidth(), root.winfo_screenheight())) # to make it fullpage
root.title("Welcome to the database")
root.configure(background='#9fafca')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.resizable('False','False')
# root.rowconfigure(0, minsize=50, weight=1)
# root.columnconfigure(0, minsize=50, weight=1)




frame0=Frame(root)
frm_3btn=Frame(frame0,bg="#210070")
frm_sel_welc=Frame(frame0,bg="#9fafca")
lbl_welcome=Label(frm_sel_welc, text="WELCOME TO EUL MANAGEMENT SYSTEM")
lbl_sel_user=Label(frm_sel_welc,text="Select User",bg="#caba9f")


# login page
frame1 = Frame(root,width=500, height=500, bg='#9fafca')
welcome = Label(frame1, text="WELCOME, Please Login", font="italica 15 bold", bg="#9fafca", fg="#3B2440")



error = Label(frame1, text="wrong input", bg='#9fafca')

Username = Label(frame1, text="username",bg="#9fafca", fg="white")
Password = Label(frame1, text="password",bg="#9fafca", fg="white")

Username_value = StringVar
Password_value = StringVar
check_value = IntVar

Username_box = Entry(frame1, textvariable=Username_value)
Password_box = Entry(frame1, textvariable=Password_value, show="*")

# end of login page entitites

# whenever the enter key is pressed
# then call the focus function
Username_box.bind("<Return>", focus1)
Password_box.bind("<Return>", focus2)

submit = Button(frame1, text="Submit", bg="#664F59", command=authenticate)


frame2 = Frame(root, relief=RIDGE, bg='#9fafca')
#highlightbackground="black", highlightthickness=2)

frame3 = Frame(root, relief=RIDGE,bg="#9fafca") 
#highlightbackground="black", highlightthickness=2

set_begining()

text_widget = Text(frame3,width=100, height=40, wrap="word", relief="sunken")

entry_box = Entry(frame3, relief="raised")

root.mainloop()
