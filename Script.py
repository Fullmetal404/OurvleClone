from faker import Faker
import random


# Generating Sample Data
fake = Faker()

# Sample size
#num_admins = 1
num_students = 100000
num_courses = 200
num_lecturers = 40

# Generates Lecturers Info
lecturers = [(fake.unique.random_int(min=100000, max=500000), fake.name(), fake.password(),"lecturer") for _ in range(0, num_lecturers)]

# Generates Students Info
students = [(fake.unique.random_int(min=600000, max=999999), fake.name(), fake.password(), "student") for _ in range(0, num_students)]

# Generates Courses
courses = [(fake.unique.random_int(min=0000, max=3999), fake.random_element(["COMP", "MATH", "PHY", "BIO", "CHEM", "ELET"])) for _ in range(0, num_courses)]


# Generate an sql file to make the database
with open('Queries.sql', 'w') as f:
    f.write("-- Create and select database\n")
    f.write("Create database Uwi_OurvleDB;\n")
    f.write("Use Uwi_OurvleDB;")
    f.write("\n\n")

    # # Granting user access
    # f.write("Create user 'uwi_user'@'localhost' identified by 'uwi876';\n")
    # f.write("Grant all privileges on uwi.* to 'uwi_user'@'localhost';\n")
    # f.write("FLUSH PRIVILEGES;")
    # f.write("\n\n")
    
    f.write("-- Creating table")
    f.write("\n\n")
    f.write("-- Create Users table\n")
    f.write("CREATE TABLE Users(user_id INT PRIMARY KEY,username VARCHAR(50) NOT NULL,password VARCHAR(50) NOT NULL,use_type ENUM('admin', 'lecturer', 'student') NOT NULL);")
    f.write("\n\n")
    f.write("-- Create Cousre table\n")
    f.write("CREATE TABLE Course(course_id INT PRIMARY KEY,course_name VARCHAR(100) NOT NULL);")
    f.write("\n\n")
    f.write("-- Create table for lecturer-course relationship\n")
    f.write("CREATE TABLE LecturerCourse (lecturer_id INT,course_id INT,PRIMARY KEY (lecturer_id, course_id),FOREIGN KEY (lecturer_id) REFERENCES Users(user_id),FOREIGN KEY (course_id) REFERENCES Course(course_id));")
    f.write("\n\n")
    f.write("-- Create table for student-course relationship\n")
    f.write("CREATE TABLE StudentCourse (student_id INT,course_id INT,grade INT,PRIMARY KEY (student_id, course_id),FOREIGN KEY (student_id) REFERENCES Users(user_id),FOREIGN KEY (course_id) REFERENCES Course(course_id));")
    f.write("\n\n")
    f.write("-- Create Discussion_Forum table\n")
    f.write("CREATE TABLE Discussion_Forum (forum_id INT AUTO_INCREMENT PRIMARY KEY,forum_name VARCHAR(255) NOT NULL,course_id INT,FOREIGN KEY (course_id) REFERENCES Course(course_id));")
    f.write("\n\n")
    f.write("-- Create Discussion_Thread table\n")
    f.write("CREATE TABLE Discussion_Thread (thread_id INT AUTO_INCREMENT PRIMARY KEY,thread_title VARCHAR(255) NOT NULL,thread_post TEXT NOT NULL,forum_id INT,parent_thread_id INT,FOREIGN KEY (forum_id) REFERENCES Discussion_Forum(forum_id));")
    f.write("\n\n")
    f.write("-- Create Section table\n")
    f.write("CREATE TABLE Section (section_id INT AUTO_INCREMENT PRIMARY KEY,section_title VARCHAR(255) NOT NULL,course_id INT,FOREIGN KEY (course_id) REFERENCES Course(course_id));")
    f.write("\n\n")
    f.write("-- Create Section_Item table\n")
    f.write("CREATE TABLE Section_Item (item_id INT AUTO_INCREMENT PRIMARY KEY,item_type ENUM('link', 'file', 'slides') NOT NULL,item_content TEXT NOT NULL,section_id INT);")
    f.write("\n\n")
    f.write("-- Create Calendar_Events table\n")
    f.write("CREATE TABLE Calendar_Events (event_id INT AUTO_INCREMENT Primary KEY,event_name VARCHAR(100) NOT NULL,event_date DATE NOT NULL,course_id INT,FOREIGN KEY (course_id) REFERENCES Course(course_id));")
    f.write("\n\n")
    f.write("-- Create Assignment table\n")
    f.write("CREATE TABLE Assignment (course_id INT,student_id INT,assignment_name VARCHAR(100) NOT NULL,deadline DATE NOT NULL,progress ENUM('completed', 'incompleted', 'late', 'overdue') NOT NULL,grade INT,PRIMARY KEY(course_id,student_id, assignment_name),FOREIGN KEY (course_id, student_id) REFERENCES StudentCourse(course_id, student_id));")
    f.write("\n\n")
    f.write("-- Add foreign key constraints to Discussion_Thread table\n")
    f.write("ALTER TABLE Discussion_Thread\nADD FOREIGN KEY (parent_thread_id) REFERENCES Discussion_Thread(thread_id);")
    f.write("\n\n")
    f.write("-- Add foreign key constraints to Section table\n")
    f.write("ALTER TABLE Section\nADD FOREIGN KEY (course_id) REFERENCES Course(course_id);")
    f.write("\n\n")
    f.write("-- Add foreign key constraints to Section_Item table\n")
    f.write("ALTER TABLE Section_Item\nADD FOREIGN KEY (section_id) REFERENCES Section(section_id);")
    f.write("\n\n")

    f.write("-- Inserting sample data")
    f.write("\n\n")

    f.write("-- Insert Admin")
    f.write("INSERT INTO Users (user_id, username, password, use_type) VALUES(1, 'Grand Master', 'Adim', 'admin');")
    f.write("\n\n")
    
    f.write("-- Insert Lecturers\n")
    f.write("".join(f"INSERT INTO Users (user_id, username, password, use_type) VALUES({lec[0]}, '{lec[1]}', '{lec[2]}', '{lec[3]}');\n" for lec in lecturers))
    f.write("\n\n")

    f.write("-- Insert Students\n")
    f.write("".join(f"INSERT INTO Users (user_id, username, password, use_type) VALUES({student[0]}, '{student[1]}', '{student[2]}', '{student[3]}');\n" for student in students))
    f.write("\n\n")

    f.write("-- Insert Courses\n")
    f.write("".join(f"INSERT INTO Course (course_id, Course_name) VALUES({course[0]}, '{course[1]}');\n" for course in courses))
    f.write("\n\n")

    f.write("-- Assigning Lecturer to Course\n")
    for i, lec in enumerate(lecturers):
        assigned_courses = courses[i * 5: (i + 1) * 5]
        for course in assigned_courses:
            f.write(f"INSERT INTO LecturerCourse (lecturer_id, course_id) VALUES ({lec[0]}, {course[0]});\n")
    f.write("\n\n")

    f.write("-- Assigning Student to Course\n")
    for student in students:
        num_courses = random.randint(5, 6)
        assigned_courses = list(set(fake.random_elements(elements=courses, length=num_courses)))
        for course in assigned_courses:
            f.write(f"INSERT INTO StudentCourse (student_id, course_id) VALUES ({student[0]}, {course[0]});\n")
    f.write("\n\n")
