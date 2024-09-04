from flask import Flask, render_template
from flask import request
import sys
sys.path.insert(0,'')
import priority_sorter
import math
import json



class UserInterface:
    def __init__(self,name,waivedCourses,completedCourses,semesters,summer,starting_season,credits):
        self.student_name = name
        self.waivedCourses = waivedCourses
        self.completedCourses = completedCourses
        self.semesters = semesters
        self.summer = summer
        self.starting_season = starting_season
        self.credits = credits


def process_user_interface_data(user_interface):
    #global user_interface_data
    user_interface_data = user_interface
    print_user_interface_data(user_interface_data)
    return user_interface_data

def print_user_interface_data(user_interface_data):
    waived_courses = user_interface_data.waivedCourses
    user_interface_data.waivedCourses = [course.strip() for course in waived_courses[0].split(',')]
    completed_courses = user_interface_data.completedCourses
    user_interface_data.completedCourses = [course.strip() for course in completed_courses[0].split(',')]
    if user_interface_data is not None:
        print("Student Name:", user_interface_data.student_name)
        print("Waived Courses:", user_interface_data.waivedCourses)
        print("Completed Courses:", user_interface_data.completedCourses)
        print("Semesters:", user_interface_data.semesters)
        print("Summer:", user_interface_data.summer)
        print("Starting Season:", user_interface_data.starting_season)
        print("Credits Per Semester:", user_interface_data.credits)

user_interface_data = None





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
starting_season = ['FA', 'SP', 'SU']
@app.route('/course_map', methods=['GET','POST'])
def course_map():

    #updates to coursemap for sundeep info pass
    #html_data = request.form['enter_value']
    if request.method == 'POST':



        student_name = request.form['Student_name']
        waived_courses = request.form.getlist('Waived_course')
        completed_courses = request.form.getlist('Completed_course')
        semesters = request.form['Semesters']
        summer = request.form.get('Summer', '')  
        starting_season = request.form['Starting_season']
        credits_per_sem = request.form['credits_persem']
        html_data=student_name

        user_interface = UserInterface(student_name, waived_courses, completed_courses,
                                       semesters, summer, starting_season, credits_per_sem)
        
        process_user_interface_data(user_interface)

        calendar1=priority_sorter.run_project(user_interface.semesters,
                                              user_interface.starting_season,
                                              user_interface.summer,
                                              user_interface.credits,
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

@app.route('/user_info', methods = ['GET','POST'])
def home():

    return render_template('submission_form.html',items=items,starting_season=starting_season)

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

