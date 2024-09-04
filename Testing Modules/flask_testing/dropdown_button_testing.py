from flask import Flask, render_template, request
#import xml.etree.cElementTree as ET
#Import XML Parser from Project5500/Aaron_Testing/xml_parser
import sys
sys.path.insert(0, '../xml_parser/')
import xml_parser

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def dropdown():
    return render_template('dropdown_button_testing.html')

if __name__ == "__main__":
    app.run()