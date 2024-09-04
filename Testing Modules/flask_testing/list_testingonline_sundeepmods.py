from flask import Flask, render_template
from flask import request
import sys
sys.path.insert(0,'')
import priority_sorter_list_testing
# Added by Sundeep
import name

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

app = Flask(__name__)

#Testing list option for listing variables in html list


# Added by Sundeep
user_interface_data = None

def process_user_interface_data(user_interface):
    global user_interface_data
    user_interface_data = user_interface
    waived_courses = user_interface_data.waivedCourses
    user_interface_data.waivedCourses = [course.strip() for course in waived_courses[0].split(',')]
    completed_courses = user_interface_data.completedCourses
    user_interface_data.completedCourses = [course.strip() for course in completed_courses[0].split(',')]


if __name__ == '__main__':
    name.app.run(debug=True)

# Added by Sundeep

#updates for sundeep
items=[]
hours=[]
avail=priority_sorter_list_testing.pass_available()
for course in avail:
    items.append(course.class_deptnumber)
    hours.append(str(course.class_deptnumber)+", Credits: "+str(course.credits))
    #print("Course Online: ",course.online)


data_list=[]

@app.route('/course_map', methods=['GET','POST'])
def course_map():

    #updates to coursemap for sundeep info pass
    #html_data = request.form['enter_value']
    if request.method == 'POST':
        field1_data = request.form['Student_name']
        field2_data = request.form['Waived_course']
        field3_data = request.form['Completed_course']
        field4_data = request.form['Semesters']
        field5_data = request.form['Summers']
        field6_data = request.form['Starting_season']
        field7_data = request.form['credits_persem']
        html_data=field1_data
        data_list.append({'Student_name': field1_data, 'Waived_course': field2_data, 'Completed_course': field3_data,
                          'Semesters': field4_data, 'Summers': field5_data, 'Starting_season': field6_data,
                          'credits_persem': field7_data})
        calendar1=priority_sorter_list_testing.run_project(field4_data,field6_data,field5_data,field7_data)
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
                                                                                    'credits':i.sem_courses[j].credits,
                                                                                    'Online':i.sem_courses[j].online}
        #                 {str(j.class_deptnumber): {"dept":j.department},
        #                  }]                  
    return render_template(
        'list_testingonline_withdropdown.html',
        calendar=calendar,
        html_data=html_data,
        field1_data=field1_data, 
        field2_data=field2_data, 
        field3_data=field3_data,
        field4_data=field4_data,
        field5_data=field5_data, 
        field6_data=field6_data,
        field7_data=field7_data,
        items=items,
        hours=hours)

@app.route('/home', methods = ['GET','POST'])
def home():

    return render_template('submissionform.html',items=items)

@app.route('/course_map_edit', methods=['GET','POST'])
def course_map_edit():
    if request.method == 'POST':
        field1_data = request.form['semester1_']

    return render_template("")