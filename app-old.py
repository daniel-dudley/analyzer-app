import sys
from flask import Flask, render_template
from analyzer import analyze

#print(sys.getrecursionlimit())
#sys.setrecursionlimit(1500)

app = Flask(__name__)

'''
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
'''

#app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'


@app.route('/about/')
def about():
    return '<h3>This is a Flask web application.</h3>'


@app.route('/analyze/')
def dynamic_page():
    return analyze()
    #return f'{ analyze()[0] }, { analyze()[1] }'


    #return f"Hello, {escape(name)}!"
    
#rgb_concentration_left, rgb_concentration_right = analyze()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)


#c,d = SUB.SUM_POWER(3,4)