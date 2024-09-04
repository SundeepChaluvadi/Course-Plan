from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('intropage_ht.html')
@app.route('/submission_form', methods=['GET'])
def submission_form():
    return render_template('submission_form.html')

if __name__ == '__main__':
    app.run(debug=True)
