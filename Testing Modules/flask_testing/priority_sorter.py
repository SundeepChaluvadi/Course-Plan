#imports xml parser
import sys
sys.path.insert(0, '')
import xml_parser
sys.path.insert(0, '')
import classes



#Labels course objects as Core_Course or Elective based on core_courses list
def populate_sortlist(tmplist,poplist):
    for i in poplist:
        if i.class_deptnumber in core_courses:
            i.dept_core="Core_Course"
        else:
            i.dept_core="Elective"
        tmplist.append(i)
    #Sorts courses based on class number
    tmplist.sort(key=lambda x: x.class_number, reverse=True)
    #Sorts courses based on Core vs. Elective
    tmplist.sort(key=lambda x: x.dept_core)
    return tmplist


#Print function
def print_list(tmplist):    
    for i in tmplist:
        print(i.class_deptnumber+" "+i.dept_core+" ", i.prereqs)




#Semester generator for storing courses
def semester_generator(sems,waived,completed):
    tmplist=[]
    #Append semesters for each semester, plus two in the front for Waived and completed
    for i in range(sems):
        tmplist.append(classes.Semester(i))
    return tmplist

#Semester generator with seasons and completed/waived
#Completed/waived courses are represetned with semesters[0] and semesters[1]. Semesters following will follow a cyclical format
def calendar_generator(start_season,summer_inc,sems):
    semseasons=["WA","CO"]
    if start_season=="SP":
        seasons=["SP","SU","FA"]
    elif start_season=="SU":
        seasons=["SU","FA","SP"]
    else:
        seasons=["FA","SP","SU"]
    if summer_inc==False:
        seasons.remove("SU")
    for i in range(sems):
        semseasons.append(seasons[i%len(seasons)])
    return semseasons

#Sort_prereqs, sorts courses based on highest course, then progressively reprioritizes courses based on prereqs
def sort_prereqs(tmplist):
    for i in range(len(tmplist)):
        #Iterates through each course in tmplist to see if pre-requisites are higher priority
        for newcour in tmplist[i].prereqs:
            if not any(newcour in val for val in (x.class_deptnumber for x in tmplist[0:i])):
                for tmpcourse in range(len(tmplist)):
                    #If the listed prerequ in course is not found, it is reprioritized and place at the top of tmplist.
                    if tmplist[tmpcourse].class_deptnumber==newcour:
                        tmplist.insert(0,tmplist.pop(tmpcourse))
    return tmplist

def iter_sort(tmplist):
    copylist=[]
    while (copylist!=tmplist):
        copylist=tmplist.copy()
        tmplist=sort_prereqs(tmplist)
    return tmplist

#Loads courses into Semesters (semester surrogate) based on position of previous pre-reqs
def load_courses(sortcourselist,semlist):
    #Position to ensure courses with pre-reqs are at semesester[0]
    pos=0
    for i in range(len(sortcourselist)):
        pos=2
        #Set to only sort Core Courses
        if sortcourselist[i].dept_core=="Core_Course":
            #Checks if course hs prereqs, and if so, it identifies the latest position of any prereq.
            if sortcourselist[i].prereqs:
                for newcour in sortcourselist[i].prereqs:
                    if any(newcour in val for val in semesters):
                        for val in range(len(semlist)):
                            if newcour in semlist[val]:
                                if pos < val:
                                    pos=val
                        
                #Once the latest positioned prereq is identified, the current course is placed one iter above it
                semlist[pos+1].append(sortcourselist[i].class_deptnumber)
            else:   
                #If no prereqs, the course is placed at the front of the list.
                semlist[pos].append(sortcourselist[i].class_deptnumber)
    return semlist

def load_waivedcomp(waive,comp,semlist):
    semlist[0]=waive
    semlist[1]=comp
    return semlist

def depop_list(tmplist,semlist):
    tmp=[]
    for i in semlist:
        for j in i:
            tmp.append(j)
    for i in tmp:
        for j in range(len(tmplist)):
            if tmplist[j].class_deptnumber==i:
                tmplist.pop(j)
                break
    return tmplist

def retrieve_object(coursetext,sortedlist):
    for i in sortedlist:
        if i.class_deptnumber==coursetext:
            course=i        
    return course
def deptnumber_to_course(courselist,deptnumber):
    for course in courselist:
        if deptnumber==course.class_deptnumber:
            return course
#converts updated course list to xml

#Initial xml parsing object
prime_course_list=xml_parser.populate_course_list('course_data_updated.xml')

courselist=[]

#sortlist, list of class department
sortlist=[]

#List of core courses (based on core list provided plus courses referred to by prereqs)
core_courses=['CMP SCI 1000',
              'CMP SCI 1250',
              'CMP SCI 2250',
              'CMP SCI 2261',
              'CMP SCI 2700',
              'CMP SCI 2750',
              'CMP SCI 3010',
              'CMP SCI 3130',
              'CMP SCI 4250',
              'CMP SCI 4280',
              'CMP SCI 4500',
              'CMP SCI 4760',
              'MATH 1030',
              'MATH 1035',
              'MATH 1100',
              'MATH 1320',
              'MATH 1800',
              'MATH 1900',
              'MATH 2450',
              'MATH 3000',
              'ENGLISH 3130',
              'ENGLISH 1100']


courselist=populate_sortlist(courselist,prime_course_list)


sortlist=sort_prereqs(courselist)
sortlist=iter_sort(sortlist)

#Object for estabilishing available courses
##########

available=classes.Available(sortlist)

###
#User Interface goes here
###


#used to populuate waived
#used to populate completed

#the populated waived and populated completed course lists are then passed to calendar later
##########

#SET VARIABLE BELOW HERE
#############################################################################

#Sets waived courses. Converts string to Course object
prewaived=[deptnumber_to_course(sortlist,'MATH 1035')]

#Sets completed courses.
precomped=[deptnumber_to_course(sortlist,'CMP SCI 4250'),
        deptnumber_to_course(sortlist,'CMP SCI 2250'),
        deptnumber_to_course(sortlist,'CMP SCI 1250'),
        deptnumber_to_course(sortlist,'CMP SCI 2261'),
        deptnumber_to_course(sortlist,'MATH 1030')]
#prewaived=[]
#precomped=[]

#Semesters
sems=9
#Starting season
seas='FA'
#Will you take summers?
summer=True
#How many credits per semester?
credits_persem=12

#############################################################################
#SET VARIABLES ABOVE HERE.

available=classes.Available(sortlist)
waived=classes.Waived(prewaived)
available.pop_courses(prewaived)
comped=classes.Completed(precomped)
available.pop_courses(precomped)
print()

calendar=classes.Calendar(seas,summer,sems,waived,comped,available,credits_persem)
calendar.load_courses(available)

calendar.print_values()

#for i in calendar.available.course_list:
#    print(i.class_deptnumber)

#########
#This section for making editable course map
#Use the Calendar object and access the Course objects within the Semester Objects to
#change the position of Course Objects based on user input. i.e., change the position of
#one course from one semester to another semester, removing courses from semesters, or 
#adding new courses entirely. This should update the Calendar.Avaialble object accordingly
#Additional cross check for course validity should be included.
########