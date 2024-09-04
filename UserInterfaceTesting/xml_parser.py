#https://docs.python.org/3/library/xml.etree.elementtree.html
#xml.etree is a library within python that allows for quick and easy parsing of xmls.
import xml.etree.cElementTree as ET
import sys
sys.path.insert(0, '')
import classes

def populate_course_list(xml_file):
    
    #Generates a tree from the XML file suggested.
    #tree = ET.parse('./course_data.xml')
    tree = ET.parse(xml_file)
    #Roots the tree for the xml file.
    root = tree.getroot()

    #Storage for course objects
    course_list=[]
    #List of General Course Types as defined by course_data.xml
    types=["CoreCourses","Electives","MathandStatistics","OtherCourses","UnknownCourses","Gen.edCourses","Free.ElectiveCourses"]

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
            classes.Course(course.find("course_name").text, 
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
