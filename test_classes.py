#Order:
#Courses should be pre-generated
#Calendar should be generated first.
#Calendar, in turn, should generate semesters. 

class Course:    
    #Assuming that all course data is generated on inception, all attributes should be filled out
    #on creation.
    def __init__(self, class_name, class_number, department, prereqs, coreqs, credits,dept_core,sem_availability):
        #Name of class. Should be unique
        self.class_name=class_name
        #Class Number. Unique int
        self.class_number=class_number
        #Department. Comes from list?
        self.department=department
        #Prerequisites, form of class number.
        self.prereqs=prereqs
        #Corequisites, form of class number.
        self.coreqs=coreqs
        #Credits. Should be between 0 (if waived) and 5.
        self.credits=credits
        #Shows what department the course is a core requirement. Should be list (Could be multiple?)
        self.dept_core=dept_core
        #What times of year is it available? Includes SP,SU,FA.
        self.sem_availability=sem_availability


class Semester:
    #List of Course objects within the semester.
    sem_courses=[]
    #Max Hours. Warns/prohibits populating higher. Arbitrarily set at 17.
    max_hours=17
    #Min Hours. Attempts to populate a semester with at least enough credits. Set to 3.
    min_hours=0
    #hours from sem_courses
    hours=0

    #Semesters (like summer) may be empty, but should still be included for modification.
    #Initialization takes in both the time of year and semester number order.
    def __init__(self,time_of_year,semester_number,year):
        #Time of year, i.e. SP, SU, or FA.
        self.time_of_year=time_of_year
        #Semester's relative position in queue. 
        self.semester_number=semester_number
        #year
        self.year=year
    
    #Defines the max hours for the semester.
    def new_max_hours(self,max_hours):
        self.max_hours=max_hours
    #Defines the min hours for the semester.
    def new_min_hours(self,min_hours):
        self.min_hours=min_hours
    #Allows a course to be added to the semester.
    #(As a note, there should hypothetically be another list of "available" courses that
    #this function should also pull from. Any course added should NOT be considered "available".
    def add_course(self, course):
        self.sem_courses.append(course)
        self.hours=0
        for i in self.sem_courses:
            self.hours=self.hours+course.credits
    def pop_course(self, course):
        self.sem_courses.pop(course)
        self.hours=0
        for i in self.sem_courses:
            self.hours=self.hours+course.credits
    
#Courses should be pre-generated. 
            
class Calendar:
    semesters=[]
    #Contains the list of courses including Completed, waived, and each semester.
    total_courses=[]
    #Total hours caclulated from  total courses.
    tot_hours=0
    #Hours caclulated from gen.ed in total courses
    gened_hours=0

    #On initizliation, calendar should hypothetically only need total hours and gened hours required.
    def __init__(self,total_hours_req,gened_hours_req):
        #Required minimum number of courses. Assume this is 120.
        self.total_hours_req=total_hours_req
        #Required hours from courses listed as "Gen.ed". What is this again?
        self.gened_hours_req=gened_hours_req
    
    #Using "years", this initalizas and populates the calendar with the appropriate semesters.
    #The start of the year in this case is arbitrarily set at the start of fall.
    #This could potentially be fixed with another initialization setting?
    #3 semesters are generated for every year
    def add_semesters(self,years):
        #Generates 3 semesters per year, SP, SU, and FA.
        self.years=years
        for year in range(self.years):
            for sem in ["FA","SP","SU"]:
                self.semesters.append(Semester(sem,len(self.semesters),year))

class Completed:
    #Courses listed as "completed"
    complete_courses=[]
    #Hours from completed courses
    hours=0
    def add_course(self,course):
        self.complete_courses.append(course)
    def pop_course(self,course):
        self.complete_courses.pop(course)

class Waived:
    #Courses listed as waived
    waived_courses=[]
    #Note: Waived courses do not count toward cumulative hours. 
    def add_course(self,course):
        self.waived_courses.append(course)
    def pop_course(self,course):
        self.waived_courses.pop(course)

class Available:
    #List of available courses including core, gen.ed, and electives.
    course_list=[]
    def add_course(self,course):
        self.course_list.append(course)
    def pop_course(self,course):
        return self.course_list.pop(course)

#Example of initial population of course list.
Available.add_course(Course("Study Period", 2222, "CompSci", [2221], [2221], 3, "CS", ["FA","SP","SU"]))
Available.add_course(Course("Pre Study Period", 2221, "CompSci", [], [], 3, "CS", ["FA","SP","SU"]))
student_calendar=Calendar(120,27)
student_calendar.add_semesters(4)
print(student_calendar.semesters[1].time_of_year)

#Courses are pop'd from course_list and added to the semesters. (This should also be done for "completed" and "waived")
student_calendar.semesters[0].add_course(Available.pop_course(0))
student_calendar.semesters[1].add_course(Available.pop_course(1))
print("Year",student_calendar.semesters[1].year)

for sem in student_calendar.semesters:
    print("Year ",sem.year)
    print("Semester ",sem.time_of_year)
    print("Courses: ")
    for cour in sem.sem_courses:
        print(cour.class_number," ",
              cour.class_name,
              ", ",cour.credits," credits")
