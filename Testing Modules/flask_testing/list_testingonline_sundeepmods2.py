from flask import Flask, render_template
from flask import request
import sys
sys.path.insert(0,'')
import priority_sorter_list_testing

'''
calendar1=priority_sorter_list_testing.run_project()
print(calendar1.semesters[1].sem_courses[1].class_deptnumber)
print(calendar1.semesters[1].year)
calendar={}
for i in calendar1.semesters:
    #calendar["semester_"+str(i.position)]
    #for j in i.sem_courses:
    calendar["semester_"+str(i.position+1)]={'name':('Semester '+str(i.position+1)),
                                             'season':i.season,
                                             'position':str(i.position+1),
                                             'hours':i.hours,
                                             'year':i.year,
                                             'courses':{}}
    
    print(len(i.sem_courses))
    for j in range(len(i.sem_courses)):
        calendar["semester_"+str(i.position+1)]['courses']["course_"+str(j)]={'course_name':i.sem_courses[j].class_deptnumber,
                                                                              'credits':i.sem_courses[j].credits}
#                 {str(j.class_deptnumber): {"dept":j.department},
#                  }]

print(calendar)
'''

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
    global user_interface_data
    user_interface_data = user_interface
    print_user_interface_data()

def print_user_interface_data():
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

#Testing list option for listing variables in html list

#updates for sundeep
items=[]
hours=[]
avail=priority_sorter_list_testing.pass_available()
for course in avail:
    items.append(course.class_deptnumber)
    hours.append(str(course.class_deptnumber)+", Credits: "+str(course.credits)+",")
    #print("Course Online: ",course.online)


data_list=[]
starting_season = ['FA', 'SP', 'SU']
@app.route('/course_map', methods=['GET','POST'])
def course_map():

    #updates to coursemap for sundeep info pass
    #html_data = request.form['enter_value']
    if request.method == 'POST':
        '''
        field1_data = request.form['Student_name']
        field2_data = request.form['Waived_course']
        field3_data = request.form['Completed_course']
        field4_data = request.form['Semesters']
        field5_data = request.form['Summers']
        field6_data = request.form['Starting_season']
        field7_data = request.form['credits_persem']
        '''


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
        print("pre:",waived_courses)
        print("post:",user_interface.waivedCourses)
        calendar1=priority_sorter_list_testing.run_project(semesters,starting_season,summer,credits_per_sem,user_interface.waivedCourses,user_interface.completedCourses)
        #print(calendar1.semesters[1].sem_courses[1].class_deptnumber)
        #print(calendar1.semesters[1].year)
        calendar={}
        for i in calendar1.semesters:
            #calendar["semester_"+str(i.position)]
            #for j in i.sem_courses:
            calendar["semester_"+str(i.position+1)]={'name':('Semester '+str(i.position+1)),
                                                    'season':i.season,
                                                    'position':str(i.position+1),
                                                    'hours':i.hours,
                                                    'year':i.year,
                                                    'courses':{}}
            
            print(len(i.sem_courses))
            for j in range(len(i.sem_courses)):
                calendar["semester_"+str(i.position+1)]['courses']["course_"+str(j)]={'course_name':i.sem_courses[j].class_deptnumber,
                                                                                    'credits':i.sem_courses[j].credits,
                                                                                    'online':i.sem_courses[j].online,
                                                                                    'season_available':{}}
                for k in range(len(i.sem_courses[j].sem_availability)):
                    print(i.sem_courses[j].class_deptnumber)
                    print(i.sem_courses[j].sem_availability[k])
                    sea=str(i.sem_courses[j].sem_availability[k])
                    print("length: ", i.sem_courses[j].online)
                    if len(i.sem_courses[j].online)==0:
                        onl='-'
                    else:
                        onl=str(i.sem_courses[j].online[k])
                    print(sea)
                    print(onl)
                    calendar["semester_"+str(i.position+1)]['courses']["course_"+str(j)]['season_available'][sea]=onl
        #                 {str(j.class_deptnumber): {"dept":j.department},
        #                  }]    
        print(calendar)              
    return render_template(
        'list_testingonline_withdropdown2.html',
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
        hours=hours)

@app.route('/home', methods = ['GET','POST'])
def home():

    return render_template('submissionform2.html',items=items,starting_season=starting_season)

@app.route('/course_map_edit', methods=['GET','POST'])
def course_map_edit():
    if request.method == 'POST':
        field1_data = request.form['semester1_']

    return render_template("")