from flask import Flask, request, render_template
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

def word_list(wordBank,dictionary):
    ## TO DO: get items from deep search to add to the dl
    for key, value in iter(dictionary.items()):
        if isinstance(value, dict):
                word_list(wordBank,value)
        else:
            ## split string and extend list
            wordBank.extend(value.split())
    return wordBank

def most_common_word(nested_dictionary):
    empty_word_list =[]
    wordlist = word_list(empty_word_list,nested_dictionary)
    return Counter(wordlist).most_common(1)[0][0]

@app.route('/set/<key>/<value>')
def set(key=None, value=None):
    test[key] = value
    return render_template('set.html', title="Set Key",key=key, value=value)

@app.route('/del/<key>')
def delete(key=None):
    try:
        removed = test.pop(key)
        return render_template('del.html', title="Delete Key", key=key)
    except:
        return '<h1>Element %s does not exist</h1>' % key

@app.route('/')
def index():
    #return render_template('del.html', name=key)
    mostCommon = most_common_word(test)
    return render_template('index.html', text=test, mostCommon=mostCommon)

@app.route('/pretty')
def pretty():
    return render_template('pretty.html', text=test)

@app.route('/working')
def working():
    return render_template('working.html')


if __name__ == '__main__':
    app.run(debug=True)  ## DO NOT KEEP TRUE WHEN PUBLISHING
