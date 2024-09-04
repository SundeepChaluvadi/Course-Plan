#Order:
#Courses should be pre-generated
#Calendar should be generated first.
#Calendar, in turn, should generate semesters. 
import xml.etree.cElementTree as ET
import math

class Course:    
    #Assuming that all course data is generated on inception, all attributes should be filled out
    #on creation.
    credits=3

    def __init__(self, 
                 class_name, 
                 class_number, 
                 department,
                 prereqs, 
                 coreqs, 
                 credits,
                 dept_core,
                 sem_availability,
                 online,
                 course_description):
        #Name of class. Should be unique
        self.class_name=class_name
        #Class Number. Unique int
        self.class_number=class_number
        #Class subject
        self.department=department
        #Prerequisites, form of class number and subject
        self.prereqs=prereqs
        #Corequisites, form of class number and subject.
        self.coreqs=coreqs
        #Credits. Should be between 0 (if waived) and 5.
        if credits=='1-3':
            credits=3
        self.credits=int(credits)
        #Identifies the type of course, (ie elective, gened, core, other)
        self.dept_core=dept_core
        #What times of year is it available? Includes SP,SU,FA.
        #Substitution for spring fall and summer for abbreviation
        newsem=[sub.replace('Fall','FA').replace('Summer','SU') .replace('Spring','SP')  for sub in sem_availability]        
        #Assumes if course has no availability listed that it is online year round. For now.
        if not sem_availability:
            newsem=['SP','FA','SU']
        self.sem_availability=newsem
        #Online availability
        self.online=online
        #Course Description. 
        self.course_description=course_description
        #Set course class number
        self.class_deptnumber=self.department+" "+self.class_number

    
    #Print class for Courses. Simply states values. When a list is not available for a list value, NA is provided instead.
    #(Exception: Available semesters. This should always have FA, SU, or SP)
    def print_stats(self):
        print("Class name: ", self.class_name)
        print("Class number: ", self.class_number)
        print("Subject: ", self.department)
        print("Department Number: ", self.class_deptnumber)
        if self.prereqs:
            print("Prerequisites: ", self.prereqs)
        else:
            print("Prequisites: NA")
        if self.coreqs:
            print("Paired: ", self.coreqs)
        else:
            print("Paired: NA")
        print("Credits: ",self.credits)
        if self.dept_core:
            print("Course Type: ",self.dept_core)
        else:
            print("Course Type: NA")
        print("Available semesters: ", self.sem_availability)
        print("Attendence: ", self.online)
        print(self.course_description)


class Semester:
    #List of Course objects within the semester.
    sem_courses=[]
    #List of course names within the semester
    sem_course_names=[]
    #hours from sem_courses
    hours=0
    max_hours=0

    #Semesters (like summer) may be empty, but should still be included for modification.
    #Initialization takes in both the time of year and semester number order.
    def __init__(self,position,season,year,max_hours):
        self.position=position 
        #Time of year, i.e. SP, SU, or FA.
        #self.time_of_year=time_of_year
        #Semester's relative position in queue. 
        #self.semester_number=semester_number
        self.sem_courses=[]
        #Initializing self.sem_courses within the 
        self.season=season
        self.hours=0
        self.year=year
        self.max_hours=max_hours
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
    def print_attributes(self):
        print("Semester ",self.position+1)
        print("Hours:",self.hours)
        print("Season:",self.season)
        print("Courses: ")
        for i in self.sem_courses:
            print("   ",i.class_deptnumber)
    def calc_hours(self):
        n=0
        for i in self.sem_courses:
            n=n+i.credits
        self.hours=n
            
    
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
    def print_values(self):
        print("Completed Courses:")
        for cour in self.course_list:
            print("   ",cour.class_deptnumber)

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
    def print_values(self):
        print("Waived Courses:")
        for cour in self.course_list:
            print("   ",cour.class_deptnumber)

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
    electivemax=15
    genedelectivemax=27
    corecredits=0
    electivecredits=0
    starting_gened=0
    starting_free=0
    def __init__(self,start_season,summer_inc,sems,waived,completed,available,credits_persem,credits_persummer,starting_gened,starting_free):
        self.semesters=[]
        self.semnames=[]
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
        #for i in  range(self.sems):
        for i in range(100):
            self.semnames.append([])
        self.available=available
        self.credits_persem=credits_persem
        #return semseasons
        self.credits_persummer=credits_persummer
        self.starting_gened=starting_gened
        self.starting_free=starting_free

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
        #counter for gen.ed
        gen_eds=0
        #counter for free electives
        free_elective_hours=0
        #counter for prereq hours
        prereq_hours=0
        #initialization of waived and completed semesters        
        self.semesters.append(Semester(0,"WA",2024,100))
        self.semesters[0].sem_courses=self.waived.course_list
        #Addition of completed courses
        self.semesters.append(Semester(1,"CO",2024,100))
        self.semesters[1].sem_courses=self.completed.course_list
        for i in self.semesters[1].sem_courses:
            if i.dept_core=="Core_Course":
                corecount=corecount+i.credits
                #print("corecount",corecount)
            if i.dept_core=="Core_Prereq":
                prereq_hours=prereq_hours+i.credits
            if i.dept_core=="Elective" and elective<=15:
                elective=elective+i.credits
            else:
                #if gen_eds<=27:
                #    gen_eds=gen_eds+i.credits
                #else:
                    free_elective_hours=free_elective_hours+i.credits
                #print("electivecount",elective)
            if i.dept_core=="Gen.Ed" and gen_eds<=27:
                gen_eds=gen_eds+i.credits
            else:
                free_elective_hours=free_elective_hours+i.credits
                #print("gen_eds",gen_eds)
        #Initial tracking of completed courses for credit counters. 

        #For the range of available courses
        hourspersem=[]
        #for i in range(self.sems+2):
        for i in range(100):
            hourspersem.append(0)
        
        #populate the hourspersem for completed courses
        for course in self.semesters[1].sem_courses:
            hourspersem[1]=hourspersem[1]+course.credits 
        for i in range(len(sortcourselist)):
            pos=2
            #print("pos:",pos)
            #Set to only sort Core Courses/Core_prereq, check that semesters available matches semesters in calendar.
            if sortcourselist[i].dept_core=="Core_Course" or sortcourselist[i].dept_core=="Core_Prereq" and not set(sortcourselist[i].sem_availability).isdisjoint(self.seasons):
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
                                    
                                    """
                                    print("sort course list len:",len(sortcourselist))
                                    print("seasons len:",len(self.seasons))
                                    print("hoursepersem :", hourspersem)
                                    print("semavailability at i",len(sortcourselist[i].sem_availability))        
                                    print("2:",self.credits_persem)
                                    print("pos+1",(pos+1))
                                    print("1:",hourspersem[pos+1])
                                    print("3:",hourspersem[pos+1]+sortcourselist[i].credits>self.credits_persem)
                                    print("pos:", pos)
                                    """
                                    #Checks current semesters if it is summer or not and sets credit check to that value
                                    pos=pos+1
                                    if self.seasons[(pos)%len(self.seasons)-2]=="SU":
                                        cred=self.credits_persummer
                                    else:
                                        cred=self.credits_persem
                                    #while ((hourspersem[pos]+sortcourselist[i].credits)>math.ceil(cred*0.6)) or (self.seasons[(pos)%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                    print("Checking 1",sortcourselist[i].class_deptnumber)
                                    print("Checking 2",self.seasons[(pos)%len(self.seasons)-2])
                                    print("Checking 3",sortcourselist[i].sem_availability)
                                    print(len(hourspersem))
                                    print("Checking 4", hourspersem[pos])
                                    while ((hourspersem[pos]+sortcourselist[i].credits)>cred) or (self.seasons[(pos)%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                        #print("1:",hourspersem[pos+1]+sortcourselist[i].credits,cred, self.seasons[(pos)%len(self.seasons)-2])
                                        pos=pos+1
                                        testing=testing+1

                                                                            
                                        if self.seasons[(pos)%len(self.seasons)-2]=="SU":
                                            cred=self.credits_persummer
                                        else:
                                            cred=self.credits_persem

                    if (pos)>=len(semlist):
                        print('Error: The number of semesters requested is insufficient for map generation.')
                        print('Please adjust the number of semesters or update waive/completed courses')
                        exit()
                    #Once the latest positioned prereq is identified, the current course is placed one iter above it
                    semlist[pos].append(sortcourselist[i].class_deptnumber)
                    hourspersem[pos]+=sortcourselist[i].credits
                    if sortcourselist[i].dept_core=="Core_Course":
                        corecount=corecount+int(sortcourselist[i].credits)
                    if sortcourselist[i].dept_core=="Core_Prereq":
                        prereq_hours=prereq_hours+int(sortcourselist[i].credits)
                else:   
                    #If no prereqs, the course is placed at the front of the list.
                    if self.seasons[pos%len(self.seasons)-2]=="SU":
                        cred=self.credits_persummer
                    else:
                        cred=self.credits_persem
                    
                    while ((hourspersem[pos]+sortcourselist[i].credits)>math.ceil(cred)) or (self.seasons[(pos)%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                        #print("2:",hourspersem[pos+1]+sortcourselist[i].credits,cred, self.seasons[(pos)%len(self.seasons)-2])
                                        pos=pos+1
                                        #testing=testing+1
                                        if self.seasons[(pos)%len(self.seasons)-2]=="SU":
                                            cred=self.credits_persummer
                                        else:
                                            cred=self.credits_persem
                    if pos>=len(semlist):
                        print('Error: The number of semesters requested is insufficient for map generation.')
                        print('Please adjust the number of semesters or update waive/completed courses')
                        exit()
                    semlist[pos].append(sortcourselist[i].class_deptnumber)
                    hourspersem[pos]+=sortcourselist[i].credits
                    print("Attaching ",sortcourselist[i].class_deptnumber,"to semester",pos,"hours",hourspersem[pos])
                    if sortcourselist[i].dept_core=="Core_Course":
                        corecount=corecount+int(sortcourselist[i].credits)
                    if sortcourselist[i].dept_core=="Core_Prereq":
                        prereq_hours=prereq_hours+int(sortcourselist[i].credits)
        #Cycles through list of courses for electives
        if elective<15:
            for i in range(len(sortcourselist)):
                #i=len(sortcourselist)-x-1
                pos=2
                #elective=0
                #Set to only sort Elective Courses that are lvl 3000 or greater, and semesters available are in calendar semesters.
                if sortcourselist[i].dept_core=="Elective" and int(sortcourselist[i].class_number)>=3000 and sortcourselist[i].department=='CMP SCI' and not set(sortcourselist[i].sem_availability).isdisjoint(self.seasons):
                    #Checks if course hs prereqs, and if so, it identifies the latest position of any prereq.
                    if sortcourselist[i].prereqs:
                        for newcour in sortcourselist[i].prereqs:
                            if any(newcour in val for val in semlist):
                                for val in range(len(semlist)):
                                    if newcour in semlist[val]:
                                        if pos < val:
                                            pos=val
                                        #Check if existing name has season associated with it.
                                        pos=pos+1
                                        testing=0
                                        #print("Season ",self.seasons[pos%len(self.seasons)-2], sortcourselist[i].sem_availability, newcour)
                                        if self.seasons[(pos)%len(self.seasons)-2]=="SU":
                                            cred=self.credits_persummer
                                        else:
                                            cred=self.credits_persem
                                        print(sortcourselist[i].class_deptnumber,sortcourselist[i].sem_availability,self.seasons[(pos)%len(self.seasons)-2])
                                        
                                        while ((hourspersem[pos]+sortcourselist[i].credits)>cred) or (self.seasons[(pos)%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                            #print("3:",hourspersem[pos+1]+sortcourselist[i].credits,cred, self.seasons[(pos)%len(self.seasons)-2])
                                            pos=pos+1
                                            testing=testing+1
                                            if self.seasons[(pos)%len(self.seasons)-2]=="SU":
                                                cred=self.credits_persummer
                                            else:
                                                cred=self.credits_persem
                        if (pos)>=len(semlist):
                            print('Error: The number of semesters requested is insufficient for map generation.')
                            print('Please adjust the number of semesters or update waive/completed courses, or hours per semester')
                            exit()
                        #Once the latest positioned prereq is identified, the current course is placed one iter above it
                        #corecount=corecount+int(sortcourselist[i].credits)
                        #Once the latest positioned prereq is identified, the current course is placed one iter above it
                        semlist[pos].append(sortcourselist[i].class_deptnumber)
                        #Updates total elective credit hours
                        hourspersem[pos]+=sortcourselist[i].credits
                        #print("Attaching ",sortcourselist[i].class_deptnumber,"to semester",pos,"hours",hourspersem[pos])
                        elective=elective+int(sortcourselist[i].credits)
                    
                    else:   
                        #If no prereqs, the course is placed at the front of the list.
                        if self.seasons[pos%len(self.seasons)-2]=="SU":
                            cred=self.credits_persummer
                        else:
                            cred=self.credits_persem
                        while ((hourspersem[pos]+sortcourselist[i].credits)>cred) or (self.seasons[(pos)%len(self.seasons)-2] not in sortcourselist[i].sem_availability):
                                            #print("4:",hourspersem[pos]+sortcourselist[i].credits,cred, self.seasons[(pos)%len(self.seasons)-2])
                                            pos=pos+1
                                            testing=testing+1
                                            if self.seasons[(pos)%len(self.seasons)-2]=="SU":
                                                cred=self.credits_persummer
                                            else:
                                                cred=self.credits_persem 
                        if pos>=len(semlist):
                            print('Error: The number of semesters requested is insufficient for map generation.')
                            print('Please adjust the number of semesters or update waive/completed courses, or hours per semester')
                            exit()
                            
                        semlist[pos].append(sortcourselist[i].class_deptnumber)
                        hourspersem[pos]+=sortcourselist[i].credits
                        print("Attaching ",sortcourselist[i].class_deptnumber,"to semester",pos,"hours",hourspersem[pos])
                        #Updates total elective hours
                        elective=elective+int(sortcourselist[i].credits)
                #Assumes elective hours is 27, stops adding classes once credits is exceeded
                if elective>=15:
                    break

        #Cycling through Gen.ed completion
        print('Hours per sem',hourspersem)
        cur_hours=sum(hourspersem)
        print("Cur hours:",cur_hours)
        test=0
        if gen_eds<27:
            for x in range(len(sortcourselist)):
                i=len(sortcourselist)-x-1
                pos=2
                #Add gen ed courses, select only courses where sem availability matches with self.seasons
                if sortcourselist[i].dept_core=="Gen.Ed" and not set(sortcourselist[i].sem_availability).isdisjoint(self.seasons):  
                        #Check for summer semesters
                        if self.seasons[pos%len(self.seasons)-2]=="SU":
                            cred=self.credits_persummer
                        else:
                            cred=self.credits_persem
                        
                        while ((hourspersem[pos]+sortcourselist[i].credits)>cred):
                                            #print("4:",hourspersem[pos+1]+sortcourselist[i].credits,cred, self.seasons[(pos-1)%len(self.seasons)-2])
                                            pos=pos+1
                                            if self.seasons[(pos)%len(self.seasons)-2]=="SU":
                                                    cred=self.credits_persummer
                                            else:
                                                cred=self.credits_persem
                                            print(hourspersem[pos])
                        if pos>=len(semlist):
                            print('Error: The number of semesters requested is insufficient for map generation.')
                            print('Please adjust the number of semesters or update waive/completed courses, or hours per semester')
                            exit()
                            
                        semlist[pos].append(sortcourselist[i].class_deptnumber)
                        hourspersem[pos]+=sortcourselist[i].credits
                        print("Attaching ",sortcourselist[i].class_deptnumber,"to semester",pos,"hours",hourspersem[pos])
                        #Updates total elective hours
                        gen_eds=gen_eds+int(sortcourselist[i].credits)
                        cur_hours=cur_hours+int(sortcourselist[i].credits)
                        test=test+1
                print('GENED TESTING',test,'hours',gen_eds)
                #Checks the total hours of existing courses, then increments gen_eds until it equals total hours
                if gen_eds>=27:
                    break
            
        #Cycle through Free Electives
        print('Hours per sem Free',hourspersem)
        cur_hours=sum(hourspersem)
        print("Cur hours:",cur_hours)
        for x in range(len(sortcourselist)):
            i=len(sortcourselist)-x-1
            pos=2
            #Add gen ed courses, select only courses where sem availability matches with self.seasons
            if sortcourselist[i].dept_core=="Free_Elective" and not set(sortcourselist[i].sem_availability).isdisjoint(self.seasons):  
                    print("ding")
                    #Check for summer semesters
                    if self.seasons[pos%len(self.seasons)-2]=="SU":
                        cred=self.credits_persummer
                    else:
                        cred=self.credits_persem
                    
                    while ((hourspersem[pos]+sortcourselist[i].credits)>cred):
                                        #print("4:",hourspersem[pos+1]+sortcourselist[i].credits,cred, self.seasons[(pos-1)%len(self.seasons)-2])
                                        pos=pos+1
                                        if self.seasons[(pos)%len(self.seasons)-2]=="SU":
                                                cred=self.credits_persummer
                                        else:
                                            cred=self.credits_persem
                                        print(hourspersem[pos])
                    if pos>=len(semlist):
                        print('Error: The number of semesters requested is insufficient for map generation.')
                        print('Please adjust the number of semesters or update waive/completed courses, or hours per semester')
                        exit()
                        
                    semlist[pos].append(sortcourselist[i].class_deptnumber)
                    hourspersem[pos]+=sortcourselist[i].credits
                    print("Attaching ",sortcourselist[i].class_deptnumber,"to semester",pos,"hours",hourspersem[pos])
                    #Updates total elective hours
                    free_elective_hours=free_elective_hours+int(sortcourselist[i].credits)
                    cur_hours=cur_hours+int(sortcourselist[i].credits)
            #Checks the total hours of existing courses, then increments gen_eds until it equals total hours
            if cur_hours>=self.tothours:
                break
            
        
        #Population of the semesters list with Semester objects, populated with course objects
        #Addition of waived courses.
        #Addition of semesters and semester courses
        years=0
        for i in range(100):
        #for i in range(self.sems):
            if self.seasons[i%len(self.seasons)]=="SP":
                #print("bing")
                years=years+1
            #Sets the semester number and season of semester (moluar with season list)
            if self.seasons[i%len(self.seasons)]=="SU":
                cred=self.credits_persummer
            else:
                cred=self.credits_persem
            self.semesters.append(Semester(i,self.seasons[(i)%len(self.seasons)],2024+years,cred))
        for i in range(100):
        # for i in range(self.sems+2):
            for j in range(len(semlist[i])):
                for k in range(len(sortcourselist)):
                    if sortcourselist[k].class_deptnumber==semlist[i][j]:
                        self.semesters[i].sem_courses.append(sortcourselist[k])
            self.semesters[i].calc_hours()

        
        #Start core credits and electives with completed courses.

        
        #Populate 
        self.corecredits=corecount
        self.electivecredits=elective
        self.gen_ed_hours=gen_eds
        self.prereq_hours=prereq_hours
        self.free_elective_hours=free_elective_hours

        #genhours=self.tothours-(corecount+elective)-self.starting_gened
        #gencourses=int(math.ceil(genhours/3))
        #self.gen_ed_hours=gencourses*3+self.starting_gened
        #self.hours=corecount+elective+self.gen_ed_hours
        
        freehours=self.tothours-(corecount+elective+gen_eds+prereq_hours)-self.starting_free
        freecourses=int(math.ceil(freehours/3))
        self.free_hours=freecourses*3+self.starting_free
        print("CHECK HOURS:")
        print("Core",corecount)
        print("elective", elective)
        print("Gened",gen_eds)
        print("Prereq",prereq_hours)
        print("Free",self.free_hours)
        self.hours=corecount+elective+gen_eds+self.free_hours+prereq_hours
        print("Total hours:",self.hours)
        
        #Removes courses from Available
        for i in self.semesters:
            if len(self.semesters)>self.sems:
                self.available.pop_courses(i.sem_courses)
    
        #Calculation and set up for general electives

        #Remove semesters after the latest semester.
        #This section seeks out the latest semester with hours in it, then removes all semesters with 0 hours after it.
        pos=0
        for sem in range(len(hourspersem)):
            #print("hourspersem:",sem,hourspersem[sem])
            if hourspersem[sem]>0:
                if sem>pos:
                    pos=sem+1
        print(pos)
        if pos>self.sems:
            self.sems=pos
        else:
            pos=self.sems
        
        #for sem in range(pos+1,len(hourspersem)+1):
        #    print(sem,len(hourspersem),len(self.semnames),len(self.semesters))
        #    self.semnames.pop(pos)
        #    self.semesters.pop(pos)
        #    hourspersem.pop(pos)
        
        #COME BACK TO THIS. Reorganize this so that it removes the last 2 semesters.    
        while len(hourspersem)>self.sems:
            #print("leng hours per sem",len(hourspersem))
            self.semnames.pop(len(hourspersem)+1)
            self.semesters.pop(len(hourspersem)+1)
            hourspersem.pop(len(hourspersem)-1)
        
            
        print(len(self.semesters))
        
        
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
        print("Preferred Hours per semester: ", self.credits_persem)
        print()
        print("Waived: ")
        for i in self.semesters[0].sem_courses:
            print("   ",i.class_deptnumber,", Credits: ",i.credits)
        print()
        print("Completed: ")
        for i in self.semesters[1].sem_courses:
            print("   ",i.class_deptnumber,", Credits: ",i.credits)
        for i in range(len(self.semesters)-2):
            print()
            print("Semester",i+1,",",self.semesters[i+2].season,": ")
            for j in self.semesters[i+2].sem_courses:
                print("   ",j.class_deptnumber,", Credits:",j.credits, j.sem_availability)
        print()
        print("Core credits:",self.corecredits)
        print("Elective credits:",self.electivecredits)
        print("Remaining credits:",self.tothours-self.hours)