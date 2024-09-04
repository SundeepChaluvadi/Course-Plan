from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def welcome_page():
    return render_template("file1.html")

@app.route("/file2", methods=['POST'])
def second_page():
    html_data = request.form["enter_value"]
    html_data1 = request.form["enter_value1"]
    return render_template("file2.html", 
                           html_data=html_data,
                           html_data1=html_data1)

# request form from id in html file

if __name__== '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)