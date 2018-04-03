from flask import Flask, render_template, flash, session, redirect, url_for
from collections import Counter, defaultdict

from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
#from flask_wtf.recaptcha import RecaptchaField

DEBUG = True
SECRET_KEY = 'secret'


app = Flask(__name__)
app.config.from_object(__name__)

class CommentForm(FlaskForm):
    comment = StringField("Comment", validators=[DataRequired()])
    key = StringField("Key", validators=[DataRequired()])
    value = StringField("Value", validators=[DataRequired()])

class DeleteForm(FlaskForm):
    comment = StringField("Comment", validators=[DataRequired()])
    key = StringField("Key", validators=[DataRequired()])


dictionary = {
    'a' : {'a1': 'apple value_a1','a2': 'angry apple value_a2'},
    'b' : {'key_2': 'value_2'},
    'c' : 'big baby apple always',
    'd' : 'cuddly cute big baby apple',
    'e' : {'e1': {'e11' : 'welcome to the basement', 'e12' : 'dark'}, 'e2': 'happy' },
    'f' : 'funny you looked'
        }

# Need to have line spaces printed?
# Not being used in current set up
# def print_dictionary(d, i=1):
#         """ Prints a nested-dictionary using a pretty + format"""
#         output = ""
#         for k, v in d.items():
#             output += ('+' * i + ' ' + str(k) + ': ')
#             if isinstance(v, dict):
#                 output += '\n\n' + print_dictionary(v, i+1)
#             else:
#                 output+= ' ' + str(v)
#         return output

def build_dictionary(d,k):
    if len(k) == 0:
        return update_dictionary(global_dictionary,d)
    else:
        d0 = {}
        d0[k[-1]] = d
        k.pop()
        build_dictionary(d0,k)

def update_dictionary(d,u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update_dictionary(d.get(k, {}), v)
        else:
            try:
                d[k] = v    ## FAILS when adding a dictionary deeper than you defined
            except:
                print("You cannot enter a dictionary in the same branch as the leaf")
    return d

def word_list(wordBank,dictionary):
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

@app.route('/set/', methods=("POST",))
@app.route('/set/<key>/', methods=("POST",))
@app.route('/set/<key>/<value>', methods=("POST",))
def set(key=None, value=None):
    form = CommentForm()
    if form.validate_on_submit():
        #comments = session.pop('key', [])
        #comments.append(form.comment.data)
        #session['comments'] = comments
        flash("You have added a new comment")
        return redirect(url_for("index"))
    #try:
    #    dictionary[key] = value
    #    return render_template('set.html', title="Set Key Value",key=key, value=value)
    #except:
    #    return

@app.route('/del')
@app.route('/del/<key>')
def delete(key=None):
    try:
        removed = dictionary.pop(key)
        return render_template('del.html', title="Delete Key", key=key)
    except:
        return '<h1>Element %s does not exist</h1>' % key

@app.route('/')
def index(form=None, mostCommon=None):
    #mostCommon = most_common_word(dictionary) # causing problems
    if form is None:
        form = CommentForm()
    comments = session.get("comments", [])
    return render_template("index.html",
                            comments=comments,
                            form=form,
                            mostCommon=mostCommon,
                            text=dictionary)
    #return render_template('index.html', text=dictionary, mostCommon=mostCommon)

@app.route("/add/", methods=("POST",))
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comments = session.pop('comments', [])
        comments.append(form.comment.data)
        session['comments'] = comments
        flash("You have added a new comment")
        return redirect(url_for("testform"))
    return testform(form)

@app.route('/pretty')
def pretty():
    return render_template('pretty.html', text=dictionary)

@app.route('/working')
def working():
    return render_template('working.html')


if __name__ == '__main__':
    app.run(debug=True)  ## DO NOT KEEP TRUE WHEN PUBLISHING
