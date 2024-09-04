from flask import Flask, render_template


app = Flask(__name__)

#Testing list option for listing variables in html list


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None,new_list=None):
    return render_template('hello.html', name=name,new_list=new_list)

@app.route('/')
def index():
    return render_template(
        'index.html',
        data=[{'gender': 'Gender'}, {'gender': 'female'}, {'gender': 'male'}],
        data1=[{'noc': 'Number of Children'}, {'noc': 0}, {'noc': 1}, {'noc': 2}, {'noc': 3}, {'noc': 4}, {'noc': 5}],
        data2=[{'smoke': 'Smoking Status'}, {'smoke': 'yes'}, {'smoke': 'no'}],
        data3=[{'region': "Region"}, {'region': "northeast"}, {'region': "northwest"},
               {'region': 'southeast'}, {'region': "southwest"}])