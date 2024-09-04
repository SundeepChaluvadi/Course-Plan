from flask import Flask, render_template
import sys
sys.path.insert(0,'')
import priority_sorter_list_testing

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
app = Flask(__name__)

#Testing list option for listing variables in html list






@app.route('/course_map')
def index():
    return render_template(
        'list_testing.html',
        calendar=calendar)