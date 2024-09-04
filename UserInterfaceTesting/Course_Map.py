from flask import Flask, render_template, request, redirect, url_for
from flask import request
import sys
sys.path.insert(0,'')
import priority_sorter
import xml.etree.cElementTree as ET
import math
import json



tree = ET.parse('course_data_updated.xml')
root = tree.getroot()

user_interface_data = None

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
def process_user_interface_data(user_interface):
    global user_interface_data
    user_interface_data = user_interface
    waived_courses = user_interface_data.waivedCourses
    user_interface_data.waivedCourses = [course.strip() for course in waived_courses[0].split(',')]
    completed_courses = user_interface_data.completedCourses
    user_interface_data.completedCourses = [course.strip() for course in completed_courses[0].split(',')]
    #print_user_interface_data()


def print_user_interface_data():
    
    if user_interface_data is not None:
        print("Student Name:", user_interface_data.student_name)
        print("Waived Courses:", user_interface_data.waivedCourses)
        print("Completed Courses:", user_interface_data.completedCourses)
        print("Current Credits:", user_interface_data.current_credits)
        print("Semesters:", user_interface_data.semesters)
        print("Summer:", user_interface_data.summer)
        print("Summer Credits:", user_interface_data.summer_credits)
        print("Starting Season:", user_interface_data.starting_season)
        print("Credits Per Semester:", user_interface_data.credits)


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

course_type_order = ['Core Prereq', 'Core Course', 'Elective', 'Gen.Ed', 'Free Elective','Unknown']

sorted_credit_list = sorted(credit_list, key=lambda x: course_type_order.index(x.course_type))

starting_season = ['FS', 'SP', 'SS']





app = Flask(__name__)
app.secret_key = 'your_secret_key'

#Testing list option for listing variables in html list

#updates for sundeep
#Return avail here if it doesn't work.
items=[]
hours=[]
avail=priority_sorter.pass_available()
for course in avail:
    items.append(course.class_deptnumber)
    hours.append(str(course.class_deptnumber)+", Credits: "+str(course.credits))

data_list=[]
starting_season = ['FS', 'SP', 'SS']
@app.route('/course_map', methods=['GET','POST'])
def course_map():

    #updates to coursemap for sundeep info pass
    #html_data = request.form['enter_value']
    #if request.method == 'POST':



    #     student_name = request.form['Student_name']
    #     waived_courses = request.form.getlist('Waived_course')
    #     completed_courses = request.form.getlist('Completed_course')
    #     semesters = request.form['Semesters']
    #     summer = request.form.get('Summer', '')  
    #     starting_season = request.form['Starting_season']
    #     credits_per_sem = request.form['credits_persem']


    #     user_interface = UserInterface(student_name, waived_courses, completed_courses,
    #                                    semesters, summer, starting_season, credits_per_sem)
        
    #     process_user_interface_data(user_interface)
    #calendar="hello"
    if request.method == 'POST':
        student_name = request.form['Student_name']
        print(student_name)
        waived_courses = request.form.getlist('Waived_course')
        print(waived_courses)
        completed_courses = request.form.getlist('Completed_course')
        print(completed_courses)
        current_credits = request.form['current_credits']
        print(current_credits)
        semesters = request.form['semesters']
        print(semesters)
        summer = request.form.get('Summer', '')  
        print(summer)
        summer_credits = request.form['summer_credits']
        print(summer_credits)
        starting_season = request.form['Starting_season']
        print(starting_season)
        credits_per_sem = request.form['credits_persem']
        print(credits_per_sem)
        html_data=student_name

        print("Student Name",student_name)
        user_interface = UserInterface(student_name, waived_courses, completed_courses, 
                                       current_credits, semesters, summer, summer_credits, 
                                       starting_season, credits_per_sem)
        
        process_user_interface_data(user_interface)

        calendar1=priority_sorter.run_project(user_interface.semesters,
                                              user_interface.starting_season,
                                              user_interface.summer,
                                              user_interface.credits,
                                              user_interface.summer_credits,
                                              user_interface.waivedCourses,
                                              user_interface.completedCourses)
        print()
        #Populating dictionary
        calendardeets={}
        calendardeets["core_credits"]=calendar1.corecredits
        calendardeets["elective_credits"]=calendar1.electivecredits
        calendardeets["gen_ed_credits"]=calendar1.gen_ed_hours
        calendardeets["free_elective_credits"]=calendar1.free_elective_hours
        calendardeets["total_hours"]=calendar1.hours
        calendar={}
        for i in calendar1.semesters:

            #Populates the semester level information
            calendar["semester_"+str(i.position+1)]={'name':('Semester '+str(i.position+1)),
                                                    'season':i.season,
                                                    'position':str(i.position+1),
                                                    'hours':i.hours,
                                                    'year':i.year,
                                                    'courses':{}}
            
            #Populates course information with class_deptnumber, credits, online availability, type (i.e., gen ed, elective, or core), and season availability
            for j in range(len(i.sem_courses)):
    
                calendar["semester_"+str(i.position+1)]['courses']["course_"+str(j)]={'course_name':i.sem_courses[j].class_deptnumber,
                                                                                    'credits':i.sem_courses[j].credits,
                                                                                    'online':i.sem_courses[j].online,
                                                                                    'type':i.sem_courses[j].dept_core,
                                                                                    'season_available':{},
                                                                                    'prereqs':{}}
                #Populates season availability
                for k in range(len(i.sem_courses[j].sem_availability)):
                    sea=str(i.sem_courses[j].sem_availability[k])
                    #print("length: ", i.sem_courses[j].online)
                    if len(i.sem_courses[j].online)==0:
                        onl='-'
                    else:
                        onl=str(i.sem_courses[j].online[k])
                    calendar["semester_"+str(i.position+1)]['courses']["course_"+str(j)]['season_available'][sea]=onl  
                #for k in range(len(i.sem_courses[j].prereqs)):  
                #    calendar["semester_"+str(i.position+1)]['courses']["course_"+str(j)]['prereqs']=str(i.sem_courses[j].prereqs[k])
                calendar["semester_"+str(i.position+1)]['courses']["course_"+str(j)]['prereqs']=i.sem_courses[j].prereqs
            #print("Course Online: ",course.online)
        available={}
        for i in range(len(calendar1.available.course_list)):
            available["course_"+str(i)]={'course_name':calendar1.available.course_list[i].class_deptnumber,
                                            'credits':calendar1.available.course_list[i].credits,
                                            'online':calendar1.available.course_list[i].online,
                                            'type':calendar1.available.course_list[i].dept_core,
                                            'season_available':{},
                                            'prereqs':{},
                                            'sem_availability':calendar1.available.course_list[i].sem_availability}
            for j in range(len(calendar1.available.course_list[i].sem_availability)):
                sea=str(calendar1.available.course_list[i].sem_availability[j])
                if len(calendar1.available.course_list[i].online)==0:
                    onl='-'
                else:
                    #print(calendar1.available.course_list[i])
                    onl=str(calendar1.available.course_list[i].online[j])
                available["course_"+str(i)]['season_available'][sea]=onl
            available["course_"+str(i)]['prereqs']=calendar1.available.course_list[i].prereqs
            #for j in range(len(calendar1.available.course_list[i].prereqs)):
            #    available["course_"+str(i)]['prereqs']=str(calendar1.available.course_list[i].prereqs[j])
        waived={}
        for i in range(len(calendar1.waived.course_list)):
            waived["course_"+str(i)]={'course_name':calendar1.waived.course_list[i].class_deptnumber,
                                            'credits':calendar1.waived.course_list[i].credits,
                                            'online':calendar1.waived.course_list[i].online,
                                            'type':calendar1.waived.course_list[i].dept_core,
                                            'season_available':{},
                                            'prereqs':{},
                                            'sem_availability':calendar1.waived.course_list[i].sem_availability}
            for j in range(len(calendar1.waived.course_list[i].sem_availability)):
                sea=str(calendar1.waived.course_list[i].sem_availability[j])
                if len(calendar1.waived.course_list[i].online)==0:
                    onl='-'
                else:
                    #print(calendar1.available.course_list[i])
                    onl=str(calendar1.waived.course_list[i].online[j])
                waived["course_"+str(i)]['season_available'][sea]=onl
            waived["course_"+str(i)]['prereqs']=calendar1.waived.course_list[i].prereqs
            #for j in range(len(calendar1.waived.course_list[i].prereqs)):
            #    waived["course_"+str(i)]['prereqs']=str(calendar1.waived.course_list[i].prereqs[j])
        
        completed={}
        for i in range(len(calendar1.completed.course_list)):
            completed["course_"+str(i)]={'course_name':calendar1.completed.course_list[i].class_deptnumber,
                                            'credits':calendar1.completed.course_list[i].credits,
                                            'online':calendar1.completed.course_list[i].online,
                                            'type':calendar1.completed.course_list[i].dept_core,
                                            'season_available':{},
                                            'prereqs':{},
                                            'sem_availability':calendar1.completed.course_list[i].sem_availability}
            for j in range(len(calendar1.completed.course_list[i].sem_availability)):
                sea=str(calendar1.completed.course_list[i].sem_availability[j])
                if len(calendar1.completed.course_list[i].online)==0:
                    onl='-'
                else:
                    #print(calendar1.available.course_list[i])
                    onl=str(calendar1.completed.course_list[i].online[j])
                completed["course_"+str(i)]['season_available'][sea]=onl
            print("Prereq check",len(calendar1.completed.course_list[i].prereqs))
            #for j in range(len(calendar1.completed.course_list[i].prereqs)):
            completed["course_"+str(i)]['prereqs']=calendar1.completed.course_list[i].prereqs
                #completed["course_"+str(i)]['prereqs']=calendar1.completed.course_list[i].prereqs[j]
                #completed["course_"+str(i)]['prereqs']['prereq_'+str(j)]=calendar1.completed.course_list[i].prereqs[j]
            print("complted prereqs",completed["course_"+str(i)]['prereqs'])
        print("Available: ",available)
        print()
        print('Calendar:',calendar)
        print("Waived:",waived)
        print("Completed:",completed)
        
    return render_template(
        'map_editor.html',
        calendar=calendar,
        student_name=student_name,
        html_data=html_data,
        semesters=semesters,
        starting_season=starting_season,
        summer=summer,
        credits_per_sem=credits_per_sem,
        waived_courses=waived_courses,
        completed_courses=completed_courses,
        items=items,
        hours=hours,
        calendardeets=calendardeets,
        available=available,
        waived=waived,
        completed=completed)

# @app.route('/user_info', methods = ['GET','POST'])
# def home():

#    return render_template('submission_form.html',items=items,starting_season=starting_season)

@app.route('/user_info', methods=['GET','POST'])
def index():
    name = "Sundeep Chaluvadi"
    return render_template('form.html', name=name, starting_season=starting_season, credit_list=sorted_credit_list)

# @app.route('/data/', methods=['GET', 'POST'])
# def handle_data():
#     if request.method == 'POST':
#         student_name = request.form['Student_name']
#         waived_courses = request.form.getlist('Waived_course')
#         completed_courses = request.form.getlist('Completed_course')
#         current_credits = request.form['current_credits']
#         semesters = request.form['semesters']
#         summer = request.form.get('Summer', '')  
#         summer_credits = request.form['summer_credits']
#         starting_season = request.form['Starting_season']
#         credits_per_sem = request.form['credits_persem']

#         user_interface = UserInterface(student_name, waived_courses, completed_courses, 
#                                        current_credits, semesters, summer, summer_credits, 
#                                        starting_season, credits_per_sem)
        
#         process_user_interface_data(user_interface)
#         print("Student name",student_name)
        
#         return redirect(url_for('course_map'))       
    

@app.route('/success')
def success():
    return "Data processed successfully!"

@app.route('/course_map_edit1', methods=['GET','POST'])
def course_map_edit1():
    calendar=request.json.get('copy')
    print("Data",calendar)
    #print('Printing data',data['semester_1'])
    #return render_template('course_map_edit.html',
    #                       input_values=input_values)
    #return render_template('course_map_edit.html')
    return render_template('course_map_edit.html',my_variable=calendar)

# @app.route('/store-variable', methods=['POST'])
# def store_variable():
#     data_received = request.json.get('data')
#     session['my_variable'] = data_received
#     print(data_received)
#     return "Data stored successfully!"

# @app.route('/process_data', methods=['GET','POST'])
# def process_data():
#     data = request.json
#     #selected_value = data.get(data)
#     # Process the received data
#     print("priting data",data)
#     #print("Received selected value from dropdown:", selected_value)
#     # You can process the data further here
#     return "Data received successfully!"


@app.route('/', methods=['GET','POST'])
def start_page():
    
    return render_template('introduction_page.html')

data_recieved={}
@app.route('/course_map_edit', methods=['GET','POST'])
def course_map_edit():

    data_received = request.json.get('data')
    print("NEW DATA!",data_received)

    return render_template('course_map_edit.html')

app.secret_key = 'your_secret_key'  # Secret key is needed for session variables

@app.route('/store-variable', methods=['POST'])
def store_variable():
    data_received = request.json.get('data')
    session['my_variable'] = data_received
    return "Data stored successfully!"

