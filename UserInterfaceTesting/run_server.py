import name
import priority_sorter
from flask import Flask, render_template, request, redirect, url_for
from run_server import process_user_interface_data
# import priority_sorter
import xml.etree.cElementTree as ET
import json


app = Flask(__name__)
user_interface_data = None

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
    
    

if __name__ == '__main__':
    name.app.run(debug=True)



