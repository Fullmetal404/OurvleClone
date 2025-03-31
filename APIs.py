from flask import Flask, request, make_response
import mysql.connector
from datetime import datetime


app = Flask(__name__)

@app.route('/hello_world', methods=['GET'])
def hello_world():
    return "hello world"


# Ueser API

@app.route('/New_user', methods=['POST'])
def New_user():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        user_id = content['User_id']
        user_name = content['User_name']
        password = content['Password']
        use_type = content['Use_type']
        cursor.execute("INSERT INTO User (user_id, user_name, password, use_type) VALUES (%s, %s, %s, %s);",(user_id, user_name, password, use_type))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Course added"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/UserLogin', methods=['POST'])
def UserLogin():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        user_name = content['User_name']
        password = content['Password']
        cursor.execute("SELECT User.user_id FROM User WHERE User.user_name = %s AND User.password = %s;",(user_name, password))
        user_id = cursor.fetchall()[0][0]
        if not user_id:
            return make_response({"Access Denied": "Incorrect username or password"}, 400)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Access granted": f"Hello User {user_id}"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


# Course API

@app.route('/Course', methods=['POST'])
def Course():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        user_id = content['User_id']
        course_id = content['Course_id']
        course_name = content['Course_name']
        cursor.execute("SELCET User.use_type FROM User WHERE User.user_id = %s;",(user_id))
        admin = cursor.fetchall()[0][0]
        if admin != "admin":
            return make_response({"Permission denied" : "Admin status required"}, 400)
        cursor.execute("SELCET * FROM Course;")
        courseList = cursor.fetchall()
        if (course_id,course_name) in courseList:
            return make_response({"Error" : "Course already exist"}, 400)
        cursor.execute("INSERT INTO Course (course_id, course_name) VALUES ( %s, %s);",(course_id, course_name))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Course added"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Participants/<course_id>', methods=['GET'])
def Participants(course_id):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()      
        query = f'''SELECT User.user_id, User.user_name, User.use_type FROM User
                       JOIN (SELECT lecturer_id FROM LecturerCourse WHERE course_id = {course_id}) 
                       AS Lecturers ON User.user_id = Lecturers.lecturer_id
                       JOIN (SELECT student_id FROM StudentCourse WHERE course_id = {course_id}) 
                       AS Students ON User.user_id = Students.student_id;'''  
        cursor.execute(query)
        course = []
        for user_id, user_name, use_type in cursor:
            participant = {}
            participant['User_id'] = user_id
            participant['User_name'] = user_name
            participant['Use_type'] = use_type
            course.append(participant)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(course, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Assigned_course', methods=['POST'])
def Assigned_course():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        lecturer_id = content['Lecturer_id']
        course_id = content['Course_id']
        cursor.execute("SELECT COUNT(LecturerCourse.course_id) AS course_count WHERE LecturerCourse.Lecturer_id")
        num_course = cursor.fetchall()[0][0]
        if num_course == 5:
            return make_response({'error': "Max number of courses (5)"}, 400)
        cursor.execute("INSERT INTO LecturerCourse (lecturer_id,course_id) VALUES ( %s, %s);",(lecturer_id,course_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Lecturer assigned"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Enrolled_course', methods=['POST'])
def Enrolled_course():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        student_id = content['Student_id']
        course_id = content['Course_id']
        cursor.execute("SELECT COUNT(StudentCourse.course_id) AS course_count WHERE StudentCourse.student_id")
        num_course = cursor.fetchall()[0][0]
        if num_course == 6:
            return make_response({'error': "Max number of courses (6)"}, 400)
        cursor.execute("INSERT INTO StudentCourse (student_id,course_id) VALUES ( %s, %s);",(student_id,course_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Enrolled"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/All_course', methods=['GET'])
def All_course():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()      
        cursor.execute("SELECT * FROM Course;")
        courseList = []
        for course_id, course_name in cursor:
            course = {}
            course['Course_id'] = course_id
            course['Course_name'] = course_name
            courseList.append(course)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(courseList, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/StudentCourse/<student_id>', methods=['GET'])
def StudentCourse(student_id):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()      
        query = f'''SELECT  course_id, course_name FROM Course
                       JOIN (SELECT StudentCourse.student_id FROM StudentCourse WHERE StudentCourse.student_id = {student_id}) 
                       AS Courses ON Course.course_id = StudentCourse.course_id;'''  
        cursor.execute(query)
        courseList = []
        for course_id, course_name in cursor:
            course = {}
            course['Course_id'] = course_id
            course['Course_name'] = course_name
            courseList.append(course)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(courseList, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/LecturerCourse/<lecturer_id>', methods=['GET'])
def LecturerCourse(lecturer_id):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()      
        query = f'''SELECT  course_id, course_name FROM Course
                       JOIN (SELECT LecturerCourse.lecturer_id FROM LecturerCourse WHERE LecturerCourse.lecturer_id = {lecturer_id}) 
                       AS Courses ON Course.course_id = LecturerCourse.course_id;'''  
        cursor.execute(query)
        courseList = []
        for course_id, course_name in cursor:
            course = {}
            course['Course_id'] = course_id
            course['Course_name'] = course_name
            courseList.append(course)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(courseList, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


# Calendar Event API

@app.route('/Calendar_event', methods=['POST'])
def Calendar_event():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        event_name = content['Event_name']
        event_date = content['Event_date']
        course_id = content['Course_id']
        cursor.execute("INSERT INTO Calendar_Events (event_name, event_date, course_id) VALUES ( %s, %s, %s);",(event_name, event_date, course_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Event added"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Course_event/<course_id>', methods=['GET'])
def Course_event(course_id):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()        
        cursor.execute(f'''SELECT Calendar_Event.event_name, Calendar_Event.event_date FROM Calendar_Event WHERE course_id = {course_id};''')
        calendar = []
        for event_name, event_date in cursor:
            event = {}
            event['Event_name'] = event_name
            event['Event_date'] = event_date
            calendar.append(event)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(calendar, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
@app.route('/Course_event/<student_id>/<event_date>', methods=['GET'])
def Student_course_event(student_id, event_date):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        query = f'''
                SELECT Calendar_Event.event_date, Calendar_Event.event_name FROM Calendar_Event
                JOIN (
                SELECT course_id FORM StudentCourse
                WHERE student_id = {student_id}
                )AS Course_event ON Calendar_Event.course_id = StudentCourse.course_id
                Where Calendar_Event.event_date = {event_date.replace("@"," ")};'''
        cursor.execute(query)
        calendar = []
        for event_name, event_date in cursor:
            event = {}
            event['Event_date'] = event_date
            event['Event_name'] = event_name
            calendar.append(event)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(calendar, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


# Discussion Forum API

@app.route('/Forum', methods=['POST'])
def Forum():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        forum_name = content['Forum_name']
        course_id = content['Course_id']
        cursor.execute("INSERT INTO Discussion_Forum (forum_name, course_id) VALUES ( %s, %s);",(forum_name, course_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Forum added"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Discussion_forum/<course_id>', methods=['GET'])
def Discussion_forum(course_id):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()        
        cursor.execute(f'''SELECT Discussion_Forum.forum_name FROM Discussion_Forum WHERE course_id = {course_id};''')
        result = []
        for forum_name in cursor:
            item = {}
            item['Forum_name'] = forum_name
            result.append(item)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(result, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


# Discussion Thread API

@app.route('/Discussion_thread', methods=['POST'])
def Discussion_thread():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        thread_title = content['Thread_title']
        thread_post = content['Thread_post']
        Forum_id = content['Forum_id']
        cursor.execute("INSERT INTO Discussion_Thread (thread_title, thread_post, Forum_id) VALUES ( %s, %s, %s);",(thread_title, thread_post, Forum_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Discussion_thread added"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Replie_thread', methods=['POST'])
def Replie_thread():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        thread_title = content['Thread_title']
        thread_post = content['Thread_post']
        Forum_id = content['Forum_id']
        Parent_thread_id = content['Parent_thread_id']
        cursor.execute("INSERT INTO Discussion_Thread (thread_title, thread_post, Forum_id, Parent_thread_id) VALUES ( %s, %s, %s, %s);",(thread_title, thread_post, Forum_id, Parent_thread_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Replie_thread added"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Forum_thread/<forum_name>', methods=['GET'])
def Forum_thread(forum_name):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        query = f'''
            SELECT Discussion_Thread.thread_title, Discussion_Thread.thread_post
            FROM Discussion_Thread JOIN (SELECT forum_id
            FROM Discussion_Forum WHERE forum_name = {forum_name}
            ) AS Forum ON Discussion_Thread.forum_id = Discussion_Forum.forum_id;'''
        cursor.execute(query)
        result = []
        for thread_title, thread_post in cursor:
            thread = {}
            thread['Thread_title'] = thread_title
            thread['thread_post'] = thread_post
            result.append(thread)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(result, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


# Course Content API

@app.route('/Section', methods=['POST'])
def Section():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        section_title = content['Section_title']
        course_id = content['Course_id']
        cursor.execute("INSERT INTO Section (section_title, course_id) VALUES ( %s, %s);",(section_title, course_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Section added"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Section_item', methods=['POST'])#----
def Section_item():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        section_id = content['Section_id']
        section_title = content['Section_title']
        item_type = content['Item_type']
        item_content = content['Item_content']
        #Upload actural files...
        cursor.execute("INSERT INTO Section_Item (item_type, item_content, section_id) VALUES ( %s, %s, %s);",(item_type, item_content, section_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Section item added"}, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Course_content/<course_id>', methods=['GET'])#----
def Course_content(course_id):
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()        
        query = f'''
            SELECT Section_item.item_type, Section_item.item_content
            FROM Section_item
            JOIN (
                SELECT section_id
                FROM Section
                WHERE course_id = {course_id}
                GROUP BY section_id
            ) AS Section ON Section.section_id = Section_item.section_id;'''
        cursor.execute(query)
        #Upload actural files...
        result = []
        for item_type, item_content in cursor:
            item = {}
            item['Item_type'] = item_type
            item['Item_content'] = item_content
            result.append(item)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(result, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


# Assignments API

@app.route('/Assignment', methods=['POST'])#----
def Assignment():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        course_id = content['Course_id']
        assignment_name = content['Assignment_name']
        deadline = content['Deadline']
        progress = 'incompleted'
        #Upload actural files...
        cursor.execute(f"SELECT StudentCourse.student_id FROM StudentCourse WHERE StudentCourse.course_id = {course_id};")
        student_ids = cursor.fetchall()
        for student_id in student_ids:
            cursor.execute(f"INSERT INTO Assignment (course_id, student_id, assignment_name, deadline, progress) VALUES ({course_id}, {student_id[0]}, '{assignment_name}', '{deadline}', '{progress}');")
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Success" : "Assignment added"}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Submit', methods=['PUT'])#----
def Submit():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        assignment_name = content['Assignment_name']
        course_id = content['Course_id']
        student_id = content['Student_id']
        #Upload actural files...
        cursor.execute("SELECT deadline FROM Assignment WHERE Assignment.course_id = %s AND Assignment.assignment_name = %s ;",(course_id,assignment_name))
        deadline = cursor.fetchall()[0][0]
        entrytime = datetime.now()
        if deadline >= entrytime:
            progress = 'completed'
        elif deadline < entrytime:
            progress = 'late'
        # Impliment overdue status...
        cursor.execute("UPDATE Assignment SET progress = %s WHERE Assignment.course_id = %s AND Assignment.assignment_name = %s AND Assignment.student_id = %s;",(progress,course_id,assignment_name,student_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Submitted" : "Assignment uploaded"}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Grade', methods=['PUT'])
def Grade():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        content = request.json
        assignment_name = content['Assignment_name']
        course_id = content['Course_id']
        student_id = content['Student_id']
        grade = content['Grade']
        cursor.execute("SELECT Assignment.progress FROM Assignment WHERE Assignment.course_id = %s AND Assignment.assignment_name = %s AND Assignment.student_id = %s;",(course_id,assignment_name,student_id))
        progress = cursor.fetchall()[0][0]
        if progress == "incompleted":
            return make_response({'File not found': f"No submission for student id: {student_id}"}, 404)
        cursor.execute("UPDATE Assignment SET Assignment.grade = %s WHERE Assignment.course_id = %s AND Assignment.assignment_name = %s AND Assignment.student_id = %s;",(grade,course_id,assignment_name,student_id))
        cursor.execute("UPDATE  StudentCourse SET StudentCourse.grade = (SELECT SUM(Assignment.grade) FROM Assignment WHERE Assignment.course_id = StudentCourse.course_id AND Assignment.student_id = StudentCourse.student_id) WHERE StudentCourse.course_id = %s AND StudentCourse.student_id = %s;",(course_id,student_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"Graded" : "Assignment marked"}, 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)


# Report API

@app.route('/Courses_50_or_more_students', methods=['GET'])
def Courses_50_or_more_students():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()        
        cursor.execute("DROP VIEW IF EXISTS Courses_50_or_more_students")
        query = '''CREATE VIEW Courses_50_or_more_students AS
            SELECT Course.course_id, Course.course_name
            FROM Course
            JOIN (
                SELECT course_id, COUNT(*) AS num_students
                FROM StudentCourse
                GROUP BY course_id
            ) AS course_student_count ON Course.course_id = course_student_count.course_id
            WHERE course_student_count.num_students >= 50'''
        cursor.execute(query)
        cursor.execute("SELECT course_id, course_name FROM Courses_50_or_more_students")
        report = []
        for course_id, course_name in cursor:
            course = {}
            course['course_id'] = course_id
            course['course_name'] = course_name
            report.append(course)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/Students_5_or_more_courses', methods=['GET'])
def Students_5_or_more_courses():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()        
        cursor.execute("DROP VIEW IF EXISTS Students_5_or_more_courses")
        query = '''CREATE VIEW Students_5_or_more_courses AS
            SELECT user_id, username
            FROM Users
            JOIN (
                SELECT student_id, COUNT(*) AS num_courses
                FROM StudentCourse
                GROUP BY student_id
            ) AS student_course_count ON Users.user_id = student_course_count.student_id
            WHERE Users.use_type = 'student' AND student_course_count.num_courses >= 5;'''
        cursor.execute(query)
        cursor.execute("SELECT user_id, username FROM Students_5_or_more_courses")
        report = []
        for user_id, username in cursor:
            student = {}
            student['student_id'] = user_id
            student['student_name'] = username
            report.append(student)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
@app.route('/Lecturers_3_or_more_courses', methods=['GET'])
def Lecturers_3_or_more_courses():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()        
        cursor.execute("DROP VIEW IF EXISTS Lecturers_3_or_more_courses")
        query = '''CREATE VIEW Lecturers_3_or_more_courses AS
            SELECT user_id, username
            FROM Users
            JOIN (
                SELECT lecturer_id, COUNT(*) AS num_courses
                FROM LecturerCourse
                GROUP BY lecturer_id
            ) AS lecturer_course_count ON Users.user_id = lecturer_course_count.lecturer_id
            WHERE Users.use_type = 'lecturer' AND lecturer_course_count.num_courses >= 3;'''
        cursor.execute(query)
        cursor.execute("SELECT user_id, username FROM Lecturers_3_or_more_courses")
        report = []
        for user_id, username in cursor:
            lecturer = {}
            lecturer['lecturer_id'] = user_id
            lecturer['lecturer_name'] = username
            report.append(lecturer)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
@app.route('/Top_10_most_enrolled_courses', methods=['GET'])
def Top_10_most_enrolled_courses():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        cursor.execute("DROP VIEW IF EXISTS Top_10_most_enrolled_courses")
        query = '''CREATE VIEW Top_10_most_enrolled_courses AS
            SELECT Course.course_id, course_name, COUNT(*) AS num_students
            FROM Course
            JOIN StudentCourse ON Course.course_id = StudentCourse.course_id
            GROUP BY course_id
            ORDER BY num_students DESC
            LIMIT 10;'''
        cursor.execute(query)
        cursor.execute("SELECT course_id, course_name, num_students FROM Top_10_most_enrolled_courses")
        report = []
        for course_id, course_name, num_students in cursor:
            course = {}
            course['course_id'] = course_id
            course['course_name'] = course_name
            course['enrolled'] = num_students
            report.append(course)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
@app.route('/Top_10_students', methods=['GET'])
def Top_10_students():
    try:
        cnx = mysql.connector.connect(user='uwi_user', password='uwi876',
                                host='localhost',
                                database='Uwi_OurvleDB')
        cursor = cnx.cursor()
        cursor.execute("DROP VIEW IF EXISTS Top_10_students")
        query = '''CREATE VIEW Top_10_students AS
            SELECT student_id, username, ROUND(AVG(grade), 2) AS avg_grade
            FROM Users
            JOIN StudentCourse ON Users.user_id = StudentCourse.student_id
            GROUP BY student_id
            ORDER BY avg_grade DESC
            LIMIT 10;'''
        cursor.execute(query)
        cursor.execute("SELECT student_id, username, avg_grade FROM Top_10_students")
        report = []
        for user_id, username, avg_grade in cursor:
            student = {}
            student['student_id'] = user_id
            student['student_name'] = username
            student['GPA'] = avg_grade
            report.append(student)
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response(report, 200)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

if __name__ == '__main__':
    app.run(debug=True)#app.run(port=6000)
