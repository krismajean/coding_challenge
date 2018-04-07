from flask import Flask, render_template, flash, session, redirect, url_for, request
from collections import Counter, defaultdict
import collections
import copy

from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

DEBUG = True

# FOR SECURITY
#
SECRET_KEY = 'secret'

class CommentForm(FlaskForm):
    key = StringField("Key", validators=[DataRequired()])


app = Flask(__name__)
app.config.from_object(__name__)

top_dictionary = {
    'a' : {'a1': 'apple value_a1','a2': 'angry apple value_a2'},
    'b' : {'key_2': 'value_2'},
    'c' : 'big baby apple always',
    'd' : 'cuddly cute big baby apple',
    'e' : {'e1': {'e11' : 'welcome to the basement', 'e12' : 'dark'}, 'e2': 'happy' },
    'f' : 'funny you looked'
        }

def build_dict(dictionary,key_list):
    if len(key_list) == 0:
        return dictionary #update_dictionary(top_dictionary,d)
    else:
        d0 = {}
        d0[key_list[-1]] = dictionary
        key_list.pop()
        return build_dict(d0,key_list)

def update_dictionary(dictionary,update):
    for key, value in update.items():
        if isinstance(value, collections.Mapping) and isinstance(dictionary.get(key), collections.Mapping):
            print("Into recursion")
            # if element exists: overwrites, if not exists: creates a new key
            dictionary[key] = update_dictionary(dictionary.get(key, {}), value)
            print("Out of recursion")
            print(dictionary)
        else:
            try:
                print("at the bottom now adding the final value")
                print(dictionary)

                print(key, value)
                dictionary[key] = value
                print(dictionary)
            except:
                del dictionary[key]
                dictionary[key] = value
                print("You cannot enter a dictionary in the same branch as the leaf")
    #print(dictionary)
    return dictionary

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

def get_dictionary_value_with_key_list(nested, key_list):
    if len(key_list) != 0 and isinstance(key_list,list) and key_list[0] in nested:
        for value in key_list:
            if value in nested:
                if isinstance(nested[value], dict):
                    nested = nested[value]
                elif value == key_list[-1]: #check if end of list
                    return nested[value]
                else:
                    return None
            else:
                return None
    else:
        return None

def delete_key_from_dictionary(dict_del, key_list):
    ''' Returns a dictionary with the final key in the key_list deleted'''
    #if get_dictionary_value_with_key_list(nested,key_list) == None: return nested
    #depth = len(key_list)
    if isinstance(dict_del[key_list[0]], dict):
        delete_key_from_dictionary(dict_del[key_list[0]], key_list[1:])
    if len(key_list) == 1:
        remove = key_list[0]
        del dict_del[remove]
    return dict_del

def del_key(dict_del, key_list):
    print(key_list)
    if len(key_list) == 1:
        remove = key_list[0]
        print("removing element")
        del dict_del[remove]
        return dict_del
    print(dict_del)
    print("checkig")
    if isinstance(dict_del[key_list[0]], dict):
        print("recursion")
        del_key(dict_del[key_list[0]], key_list[1:])
    return dict_del

@app.route('/')
def index(form=None, mostCommon=None):
    mostCommon = most_common_word(top_dictionary)
    if form is None:
        form = CommentForm()
    return render_template("index.html",
                            form=form,
                            mostCommon=mostCommon,
                            text=top_dictionary)

@app.route('/set/', methods=("POST","GET"))
@app.route('/set/<path:key_value>', methods=("POST","GET"))
def set(key_value=None,new_dict=top_dictionary):
    print(key_value)
    if key_value is None: return redirect(url_for("index"))
    print(key_value)
    key_list = key_value.split('/')
    if len(key_list) <= 1: return redirect(url_for("index")) # check for no value
    # Go set the value
    value = key_list.pop() # removes last element from key_list
    built = build_dict(value, key_list) # returns a {nested : {dictionary : value }}
    top_dictionary = update_dictionary(new_dict, built)
    #return redirect(url_for("index"))

@app.route('/del/<path:keys>', methods=("POST","GET"))
def delete(keys=None,dict_del=top_dictionary):
    key_list = keys.split('/')
    # Confirm element exist search for the element in the Dictionary
    if get_dictionary_value_with_key_list(dict_del, key_list) == None: redirect(url_for("index"))
    temp_dict = copy.deepcopy(dict_del)
    del_key(dict_del,key_list)
    #return redirect(url_for("index"))

@app.route('/handle_data', methods=['POST'])
def handle_data():
    command_key_value = request.form['command_key_value'].split()
    print(command_key_value)
    if command_key_value[0] == 'set':
        value = ' '.join(command_key_value[2:])
        key_list = command_key_value[1]
        key_value = key_list + '/' + value
        set(key_value)
        return redirect(url_for("index"))

## If del --> 1) Check if value exists Yes: Delete w/ dependents No: Err
    elif command_key_value[0] == 'del':
        key_list = command_key_value[1]
        delete(key_list)
        return redirect(url_for("index"))

    else:
        return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)  ## DO NOT KEEP TRUE WHEN PUBLISHING
