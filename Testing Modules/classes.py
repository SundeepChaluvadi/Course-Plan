#Order:
#Courses should be pre-generated
#Calendar should be generated first.
#Calendar, in turn, should generate semesters. 
import xml.etree.cElementTree as ET

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
        if credits=="1-3":
            #Some credits are displayed as between 1-3. We curently don't have a proper
            #Method to assign course credits manually, so this is automatically assiged
            #automatically as "3"
            credits=3
        self.credits=credits
        #Shows what department the course is a core requirement. Should be list (Could be multiple?)
        self.dept_core=dept_core
        #What times of year is it available? Includes SP,SU,FA.
        self.sem_availability=sem_availability


class Semester:
    #List of Course objects within the semester.
    sem_courses=[]
    #List of course names within the semester
    sem_course_names=[]
    #hours from sem_courses
    hours=0

    #Semesters (like summer) may be empty, but should still be included for modification.
    #Initialization takes in both the time of year and semester number order.
    def __init__(self,position,season):
        self.position=position 
        #Time of year, i.e. SP, SU, or FA.
        #self.time_of_year=time_of_year
        #Semester's relative position in queue. 
        #self.semester_number=semester_number
        self.sem_courses=[]
        #Initializing self.sem_courses within the 
        self.season=season
        self.hours=0
    
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
        self.sem_course_names.append(course.class_deptnumber)
        self.hours=0
        for i in self.sem_courses:
            self.hours=self.hours+course.credits
    def set_season(self,season):
        self.season=season
    def pop_course(self, course):
        self.names_list.remove(course.class_deptnumber)
        self.sem_courses.remove(course)
    
class Completed:
    #List of available courses including core, gen.ed, and electives.
    course_list=[]
    names_list=[]
    def __init__(self,courselist):
        self.course_list=courselist
        for i in courselist:
            self.names_list.append(i.class_deptnumber)
    def add_course(self,coursen):
        self.course_list.append(coursen)
        self.names_list.append(coursen.class_deptnumber)
    def pop_course(self,course):
        self.names_list.remove(course.class_deptnumber)
        self.course_list.remove(course)

class Waived:
    #List of available courses including core, gen.ed, and electives.
    course_list=[]
    names_list=[]
    def __init__(self,courselist):
        self.course_list=courselist
        for i in courselist:
            self.names_list.append(i.class_deptnumber)
    def add_course(self,coursen):
        self.course_list.append(coursen)
        self.names_list.append(coursen.class_deptnumber)
    def pop_course(self,course):
        self.names_list.remove(course.class_deptnumber)
        self.course_list.remove(course)

class Available:
    #List of available courses including core, gen.ed, and electives.
    course_list=[]
    names_list=[]
    def __init__(self,courselist):
        self.course_list=courselist
        for i in courselist:
            self.names_list.append(i.class_deptnumber)
    def add_course(self,coursen):
        self.course_list.append(coursen)
        self.names_list.append(coursen.class_deptnumber)
    def pop_course(self,course):
        self.names_list.remove(course.class_deptnumber)
        #self.course_list.remove(course)
        cour=self.course_list.pop(course)
        return cour
    def pop_courses(self,courses):
        for i in courses:
            if i in self.course_list:
                self.course_list.remove(i)
            if i.class_deptnumber in self.names_list:
                self.names_list.remove(i.class_deptnumber)
        
    def print_available(self):
        for i in self.course_list:
            print(i.class_deptnumber)
            

class Calendar:
    #Semesters 0 and 1 are reserved for waived and completed courses.
    #Calendar list for holding Semester objects, which in turn hold course objects.
    semesters=[]
    #Semester names list, reduces course objects to their "class_deptnum" attribute for
    #quick manipulation
    semnames=[]
    semseasons=["WA","CO"]
    hours=0
    tothours=120
    corecredits=0
    electivecredits=0
    def __init__(self,start_season,summer_inc,sems,waived,completed,available,credits_persem):
        
        #Determins number of semesters
        self.sems=sems
        self.start_season=start_season
        self.summer_inc=summer_inc
        #Establishes starting season for semester
        if start_season=="SP":
            self.seasons=["SP","SU","FA"]
        elif start_season=="SU":
            self.seasons=["SU","FA","SP"]
        else:
            self.seasons=["FA","SP","SU"]
        #Establishes if summer semester is available.
        if summer_inc==False:
            self.seasons.remove("SU")

        #Adds "Waived" object
        self.waived=waived
        #Adds the waived course object names to semnames
        self.semnames.append(self.waived.names_list)
        #Adds "Completed" object
        self.completed=completed
        #Adds "completed" course object names to semnames
        self.semnames.append(self.completed.names_list)
        #Creates nested lists for semnames equal to sems.
        for i in  range(self.sems):
            self.semnames.append([])
        self.available=available
        self.credits_persem=credits_persem
        #return semseasons

    def load_courses(self,available):
        #shorthand for the Available courses
        sortcourselist=available.course_list
        #sets up semlist for population
        semlist=self.semnames
        pos=0
        #Count for core course credits
        corecount=0
        #counter for electives
        elective=0
        #initialization of waived and completed semesters
        self.semesters.append(Semester(0,"WA"))
        self.semesters[0].sem_courses=self.waived.course_list
        #Addition of completed courses
        self.semesters.append(Semester(1,"CO"))
        self.semesters[1].sem_courses=self.completed.course_list
        for i in self.semesters[1].sem_courses:
            if i.dept_core=="Core_Course":
                corecount=corecount+i.credits
            if i.dept_core=="Elective":
                elective=elective+i.credits
        #Initial tracking of completed courses for credit counters. 

        #For the range of available courses
        hourspersem=[]
        #Holding list for the number of hours currently in each semester
        for i in range(self.sems+2):
            hourspersem.append(0)
        for i in range(len(sortcourselist)):
            pos=2
            #Set to only sort Core Courses
            if sortcourselist[i].dept_core=="Core_Course":
                #Checks if course hs prereqs, and if so, it identifies the latest position of any prereq.
                if sortcourselist[i].prereqs:
                    #Cycles through preqs
                    for newcour in sortcourselist[i].prereqs:
                        #Checks the class_deptnum names of courses in semlist
                        if any(newcour in val for val in semlist):
                            #Identifies the position of the prereq
                            for val in range(len(semlist)):
                                if newcour in semlist[val]:
                                    #Checks if the prereq is the "latest" prereq, and updates the position
                                    if pos < val:
                                        pos=val
                                    #Check if existing name has season associated with it.
                                    testing=0
                                    #print("Season ",self.seasons[pos%len(self.seasons)-2], sortcourselist[i].sem_availability, newcour)
                                    while ((hourspersem[pos+1]+sortcourselist[i].credits)>self.credits_persem) or (self.seasons[pos%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                        pos=pos+1
                                        testing=testing+1
                                        if testing>3:
                                            print("WARNING! No semester could be generated for", sortcourselist[i].class_deptnumber)
                                            print("Please investigate course in question. Seasons:", sortcourselist[i].sem_availability)
                                            exit()

                    if (pos+1)>=len(semlist):
                        print('Error: The number of semesters requested is insufficient for map generation.')
                        print('Please adjust the number of semesters or update waive/completed courses')
                        exit()
                    #Once the latest positioned prereq is identified, the current course is placed one iter above it
                    semlist[pos+1].append(sortcourselist[i].class_deptnumber)
                    hourspersem[pos+1]+=sortcourselist[i].credits
                    corecount=corecount+int(sortcourselist[i].credits)
                else:   
                    #If no prereqs, the course is placed at the front of the list.
                    while ((hourspersem[pos]+sortcourselist[i].credits)>self.credits_persem) or (self.seasons[pos%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                        pos=pos+1
                                        testing=testing+1
                                        if testing>self.sems:
                                            print("WARNING! No semester could be generated for", sortcourselist[i].class_deptnumber)
                                            print("Please investigate course in question. Seasons:", sortcourselist[i].sem_availability)
                                            print("Hours across semesters: ", hourspersem)
                                            exit()
                    if pos>=len(semlist):
                        print('Error: The number of semesters requested is insufficient for map generation.')
                        print('Please adjust the number of semesters or update waive/completed courses')
                        exit()
                    semlist[pos].append(sortcourselist[i].class_deptnumber)
                    hourspersem[pos]+=sortcourselist[i].credits
                    corecount=corecount+int(sortcourselist[i].credits)
        
        #Cycles through list of courses for Electives
        for x in range(len(sortcourselist)):
            i=len(sortcourselist)-x-1
            pos=2
            #elective=0
            #Set to only sort Elective Courses that are lvl 3000 or greater
            if sortcourselist[i].dept_core=="Elective" and int(sortcourselist[i].class_number)>=3000:
                #Checks if course hs prereqs, and if so, it identifies the latest position of any prereq.
                if sortcourselist[i].prereqs:
                    for newcour in sortcourselist[i].prereqs:
                        if any(newcour in val for val in semlist):
                            for val in range(len(semlist)):
                                if newcour in semlist[val]:
                                    if pos < val:
                                        pos=val
                                    #Check if existing name has season associated with it.
                                    testing=0
                                    #print("Season ",self.seasons[pos%len(self.seasons)-2], sortcourselist[i].sem_availability, newcour)
                                    while ((hourspersem[pos+1]+sortcourselist[i].credits)>self.credits_persem) or (self.seasons[pos%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                        pos=pos+1
                                        testing=testing+1
                                        if testing>self.sems:
                                            print("WARNING! No semester could be generated for", sortcourselist[i].class_deptnumber)
                                            print("Please investigate course in question. Seasons:", sortcourselist[i].sem_availability)
                                            exit()

                    if (pos+1)>=len(semlist):
                        print('Error: The number of semesters requested is insufficient for map generation.')
                        print('Please adjust the number of semesters or update waive/completed courses, or hours per semester')
                        exit()
                    #Once the latest positioned prereq is identified, the current course is placed one iter above it
                    corecount=corecount+int(sortcourselist[i].credits)
                    #Once the latest positioned prereq is identified, the current course is placed one iter above it
                    semlist[pos+1].append(sortcourselist[i].class_deptnumber)
                    #Updates total elective credit hours
                    hourspersem[pos+1]+=sortcourselist[i].credits
                    elective=elective+int(sortcourselist[i].credits)
                    
                else:   
                    #If no prereqs, the course is placed at the front of the list.
                    while ((hourspersem[pos]+sortcourselist[i].credits)>self.credits_persem) or (self.seasons[pos%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                        pos=pos+1
                                        testing=testing+1
                                        if testing>self.sems:
                                            print("WARNING! No semester could be generated for", sortcourselist[i].class_deptnumber)
                                            print("Please investigate course in question. Seasons:", sortcourselist[i].sem_availability)
                                            print("Hours across semesters: ", hourspersem)
                                            exit()
                    if pos>=len(semlist):
                        print('Error: The number of semesters requested is insufficient for map generation.')
                        print('Please adjust the number of semesters or update waive/completed courses, or hours per semester')
                        exit()
                    semlist[pos].append(sortcourselist[i].class_deptnumber)
                    hourspersem[pos]+=sortcourselist[i].credits
                    #Updates total elective hours
                    elective=elective+int(sortcourselist[i].credits)
            #Assumes elective hours is 27, stops adding classes once credits is exceeded
            if elective>=15:
                break
        #Population of the semesters list with Semester objects, populated with course objects
        #Addition of waived courses.
        
        #Addition of semesters and semester courses
        for i in range(self.sems):
            #Sets the semester number and season of semester (moluar with season list)
            self.semesters.append(Semester(i,self.seasons[i%len(self.seasons)]))
            for j in range(len(semlist[i])):
                for k in range(len(sortcourselist)):
                    if sortcourselist[k].class_deptnumber==semlist[i][j]:
                        self.semesters[i].sem_courses.append(sortcourselist[k])
        
        #Start core credits and electives with completed courses.

        
        #Populate 
        self.corecredits=corecount
        self.electivecredits=elective
        self.hours=corecount+elective

        #Removes courses from Available
        for i in self.semesters:
            self.available.pop_courses(i.sem_courses)
    
        
        
    def populuate_waived(self,waived):
        self.waived=waived
    def populate_completed(self,completed):
        self.completed=completed
    def populate_semesters(self,semesters):
        for i in semesters:
            semesters.append(i)
    def print_values(self):
        print("Starting season: ", self.start_season)
        print("Semesters: ", self.sems)
        print("Summer available?: ", self.summer_inc)
        print()
        print("Waived: ")
        for i in self.semesters[0].sem_courses:
            print(i.class_deptnumber,", Credits: ",i.credits)
        print()
        print("Completed: ")
        for i in self.semesters[1].sem_courses:
            print(i.class_deptnumber,", Credits: ",i.credits)
        for i in range(len(self.semesters)-2):
            print()
            print("Semester",i+1,",",self.semesters[i+2].season,": ")
            for j in self.semesters[i+2].sem_courses:
                print(j.class_deptnumber,", Credits:",j.credits)
        print()
        print("Core credits:",self.corecredits)
        print("Elective credits:",self.electivecredits)
        print("Remaining credits:",self.tothours-self.hours)
