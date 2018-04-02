from flask import Flask, render_template
from collections import Counter, defaultdict

app = Flask(__name__)

test = {
    'a' : {'a1': 'apple value_a1','a2': 'angry apple value_a2'},
    'b' : {'key_2': 'value_2'},
    'c' : 'big baby apple always',
    'd' : 'cuddly cute big baby apple',
    'e' : {'e1': {'e11' : 'welcome to the basement', 'e12' : 'dark'}, 'e2': 'happy' },
    'f' : 'funny you looked'
        }

# Need to have line spaces printed?
def print_dictionary(d, i=1):
        """ Prints a nested-dictionary using a pretty + format"""
        output = ""
        for k, v in d.items():
            output += ('+' * i + ' ' + str(k) + ': ')
            if isinstance(v, dict):
                output += '\n\n' + print_dictionary(v, i+1)
            else:
                output+= ' ' + str(v)
        return output

@app.route('/set/<key>/<value>')
def set(key=None, value=None):
    test[key] = value
    return render_template('set.html', key=key, value=value)

@app.route('/del/<key>')
def delete(key=None):
    try:
        removed = test.pop(key)
        return render_template('del.html', key=key)
    except:
        return '<h1>Element %s does not exist</h1>' % key


@app.route('/')
def index():
    #return render_template('del.html', name=key)
    return render_template('index.html', text=test)
    #print_dictionary(test)

# @app.route('/hello')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)  ## DO NOT KEEP TRUE WHEN PUBLISHING
