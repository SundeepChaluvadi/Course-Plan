from flask import Flask, render_template, request, redirect, url_for
# from run_server import process_user_interface_data
from priority_sorter import available

app = Flask(__name__)
app.static_folder = 'static'


class UserInterface:
    def __init__(self,name,waivedCourses,completedCourses,semesters,summer,starting_season,credits):
        self.student_name = name
        self.waivedCourses = waivedCourses
        self.completedCourses = completedCourses
        self.semesters = semesters
        self.summer = summer
        self.starting_season = starting_season
        self.credits = credits

items = available.names_list

""" items = ['CMP SCI 1000',
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
                 'ENGLISH 1100'] """

starting_season = ['FALL', 'SPRING', 'SUMMER']

@app.route('/')
def index():
    name = "Sundeep Chaluvadi"
    return render_template('form.html', name=name, items=items, starting_season=starting_season)

@app.route('/data/', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        student_name = request.form['Student_name']
        waived_courses = request.form.getlist('Waived_course')
        completed_courses = request.form.getlist('Completed_course')
        semesters = request.form['Semesters']
        summer = request.form.get('Summer', '')  
        starting_season = request.form['Starting_season']
        credits_per_sem = request.form['credits_persem']

        user_interface = UserInterface(student_name, waived_courses, completed_courses,
                                       semesters, summer, starting_season, credits_per_sem)
        
        process_user_interface_data(user_interface)
        
        return redirect(url_for('success'))
        
        """ return redirect(url_for('display_results', student_name=student_name,
                                waived_courses=waived_courses, completed_courses=completed_courses,
                                semesters=semesters, summer=summer, starting_season=starting_season,
                                credits_per_sem=credits_per_sem)) """    
        

    """ else:
        return render_template('form.html') """
    

@app.route('/success')
def success():
    return "Data processed successfully!"


""" @app.route('/results/')
def display_results():
    student_name = request.args.get('student_name')
    waived_courses = request.args.getlist('waived_courses')
    completed_courses = request.args.getlist('completed_courses')
    semesters = request.args.get('semesters')
    summer = request.args.get('summer')
    starting_season = request.args.get('starting_season')
    credits_per_sem = request.args.get('credits_per_sem')

    return render_template('results.html', student_name=student_name, waived_courses=waived_courses,
                           completed_courses=completed_courses, semesters=semesters, summer=summer,
                           starting_season=starting_season, credits_per_sem=credits_per_sem) """




if __name__ == "__main__":
    app.run(debug=True)

    


    
