
Use uwi_ourvledb;

-- Student Count
SELECT Count(*) as StudentCount FROM uwi_ourvledb.users Where use_type = "student";

-- Course Count
SELECT Count(*) FROM uwi_ourvledb.course;

-- Max Number of Courses of Student
Select Count(course_id) as course_count from studentcourse group by student_id order by course_count desc limit 1;

-- Min Number of Courses of Student
Select Count(course_id) as course_count from studentcourse group by student_id order by course_count asc limit 1;

-- Number of Student in course 
Select course_id,Count(student_id) as student_count from studentcourse group by course_id order by student_count asc limit 1;

-- Max Number of Courses
Select lecturer_id,Count(course_id) As course_count from LecturerCourse group by lecturer_id order by course_count desc limit 1;

-- Min Number of Courses
Select lecturer_id,Count(course_id) As course_count from LecturerCourse group by lecturer_id order by course_count asc limit 1;

