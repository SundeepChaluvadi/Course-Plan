import name

user_interface_data = None

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
    
    """ courses = user_interface_data.waivedCourses
    courses_list = [course.strip() for course in courses[0].split(',')]
    for course in courses_list:
        print(course) """

if __name__ == '__main__':
    name.app.run(debug=True)
