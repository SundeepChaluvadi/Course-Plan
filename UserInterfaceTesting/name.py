from flask import Flask, render_template, request, redirect, url_for
from run_server import process_user_interface_data
# import priority_sorter
import xml.etree.cElementTree as ET
import json

app = Flask(__name__)

#app.static_folder = 'static'

tree = ET.parse('course_data_updated.xml')
root = tree.getroot()

coreCourses = ['CMP SCI 1000',
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
               'MATH 1320',
               'MATH 1800',
               'MATH 1900',
               'MATH 2450',
               'MATH 3000',
               'ENGLISH 3130']

corePrereq = ['MATH 1030',
              'MATH 1035',
              'MATH 1100',
              'ENGLISH 1100']

elective = ["CMP SCI 3410",
            "CMP SCI 3411",
            "CMP SCI 3702",
            "CMP SCI 3780",
            "CMP SCI 3990",
            "CMP SCI 4010",
            "CMP SCI 4011", 
            "CMP SCI 4012", 
            "CMP SCI 4151", 
            "CMP SCI 4020", 
            "CMP SCI 4200", 
            "CMP SCI 4220", 
            "CMP SCI 4222", 
            "CMP SCI 4300", 
            "CMP SCI 4320", 
            "CMP SCI 4340", 
            "CMP SCI 4342", 
            "CMP SCI 4370", 
            "CMP SCI 4390", 
            "CMP SCI 4410", 
            "CMP SCI 4420", 
            "CMP SCI 4610", 
            "CMP SCI 4700", 
            "CMP SCI 4730", 
            "CMP SCI 4732", 
            "CMP SCI 4750", 
            "CMP SCI 4782", 
            "CMP SCI 4792", 
            "CMP SCI 4794", 
            "CMP SCI 4880"]

freeElective = ['INFSYS 3806']

class UserInterface:
    def __init__(self,name,waivedCourses,completedCourses,current_credits,semesters,summer,summer_credits,starting_season,credits):
        self.student_name = name
        self.waivedCourses = waivedCourses
        self.completedCourses = completedCourses
        self.current_credits = current_credits
        self.semesters = semesters
        self.summer = summer
        self.summer_credits = summer_credits
        self.starting_season = starting_season
        self.credits = credits


class Credits:
    def __init__(self,
                 department,
                 class_number,
                 credits):
        self.class_deptnumber = department+" "+class_number
        if credits=='1-3' or int(credits) in range(1, 4):
            credits=3
        self.credits=int(credits)
        if self.class_deptnumber in coreCourses:
            self.course_type = 'Core Course'
        elif self.class_deptnumber in corePrereq:
            self.course_type = 'Core Prereq'
        elif department == 'Gen.Ed':
            self.course_type = 'Gen.Ed'
        elif self.class_deptnumber in elective:
            self.course_type = 'Elective'
        elif self.class_deptnumber in freeElective or department == 'Free.Elective':
            self.course_type = 'Free Elective'
        else:
            self.course_type = 'Unknown'

types=["CoreCourses","Electives","MathandStatistics","OtherCourses","UnknownCourses","Gen.edCourses","Free.ElectiveCourses"]

credit_list = []

for course_type in types:
        for course in root.find(course_type).findall("course"):
            credit_list.append(
                Credits(course.find("subject").text,
                        course.find("course_number").text,
                        course.find("credit").text
                        )
            )

course_type_order = ['Core Prereq', 'Core Course', 'Elective', 'Gen.Ed', 'Free Elective']

sorted_credit_list = sorted(credit_list, key=lambda x: course_type_order.index(x.course_type))

starting_season = ['FS', 'SP', 'SS']

@app.route('/')
def index():
    name = "Sundeep Chaluvadi"
    return render_template('form.html', name=name, starting_season=starting_season, credit_list=sorted_credit_list)

@app.route('/data/', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        student_name = request.form['Student_name']
        waived_courses = request.form.getlist('Waived_course')
        completed_courses = request.form.getlist('Completed_course')
        current_credits = request.form['current_credits']
        semesters = request.form['semesters']
        summer = request.form.get('Summer', '')  
        summer_credits = request.form['summer_credits']
        starting_season = request.form['Starting_season']
        credits_per_sem = request.form['credits_persem']

        user_interface = UserInterface(student_name, waived_courses, completed_courses, 
                                       current_credits, semesters, summer, summer_credits, 
                                       starting_season, credits_per_sem)
        
        process_user_interface_data(user_interface)
        
        return redirect(url_for('success'))       
    

@app.route('/success')
def success():
    return "Data processed successfully!"


if __name__ == "__main__":
    app.run(debug=True)

    


    
