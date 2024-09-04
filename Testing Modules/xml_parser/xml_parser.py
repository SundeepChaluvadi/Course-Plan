#https://docs.python.org/3/library/xml.etree.elementtree.html
#xml.etree is a library within python that allows for quick and easy parsing of xmls.
import xml.etree.cElementTree as ET

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
            newsem=['SP','SU','FA']
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

def populate_course_list(xml_file):
    
    #Generates a tree from the XML file suggested.
    #tree = ET.parse('./course_data.xml')
    tree = ET.parse(xml_file)
    #Roots the tree for the xml file.
    root = tree.getroot()

    #Storage for course objects
    course_list=[]
    #List of General Course Types as defined by course_data.xml
    types=["CoreCourses","Electives","MathandStatistics","OtherCourses","UnknownCourses"]

    #For loop to iteratively parse the object tree and generate course objects to populate couse_list.
    #During initialization, this would be used on the list of available courses instead.

    #for course in root.findall("course"):
    #Options are CoreCourse, Electives, and 
    for course_type in types:
        for course in root.find(course_type).findall("course"):
            course_list.append(
            #root.find() seeks out a child relative to the root.course.. Its name, combined with .text, gives the value contained in it.
            #This can be done iteratively such that children of children can use .find. 
            #In cases where multiple children are within a root, .find all with a for loop can be used to iteratively generate a list format.
            Course(course.find("course_name").text, 
                course.find("course_number").text, 
                course.find("subject").text, 
                #For loop to generate list from i.find().findall().text
                [values.text for values in course.find('prerequisite').find("or_choice").findall("and_required")] if course.find('prerequisite') else [],
                course.find("paired").text if course.findall("paired") else '',
                course.find("credit").text,
                #Hard coded to CMP SCI for now
                course_type,
                [values.find("term").text for values in course.findall("rotation_term")] if course.find("rotation_term") else [],
                [[values.find("time_code").text] for values in course.findall("rotation_term")] if course.find("rotation_term") else [],
                course.find("course_description").text,
                )
            )
    return course_list
