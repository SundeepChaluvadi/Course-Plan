from flask import Flask, render_template, request
#import xml.etree.cElementTree as ET
#Import XML Parser from Project5500/Aaron_Testing/xml_parser
import sys
sys.path.insert(0, '../xml_parser/')
import xml_parser

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def dropdown():
    #Calls the xml_parser.py method "populate_course_list" to make a list of Course objects
    course_list=xml_parser.populate_course_list('../xml_parser/course_data.xml')
    
    #Parses the list of Course objects to create a list of course names (Course Subject Course Number)
    course_names = [classi.class_deptnumber for classi in course_list]
    print(course_names)
    #Passes Coursenames to the droptest.html template.
    #return render_template('htmltest.html', course_names=course_names)
    return render_template('dropdown_testing.html', course_names=course_names)

if __name__ == "__main__":
    app.run()