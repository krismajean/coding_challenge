######
# del function - fix to be deep
# put online with Firebase

import collections
from collections import Counter, defaultdict

data = {
'a' : {'a1': 'apple value_a1','a2': 'angry apple value_a2'},
'b' : {'key_2': 'value_2'},
'c' : 'big baby apple always',
'd' : 'cuddly cute big baby apple',
'e' : {'e1': {'e11' : 'welcome to the basement', 'e12' : 'dark'}, 'e2': 'happy' },
'f' : 'funny you looked'
}

#globally declared deep_list
def word_list(dl,d):
    ## TO DO: get items from deep search to add to the dl
    for k, v in iter(d.items()):
        if isinstance(v, dict):
                word_list(dl,v)
        else:
            ## split string and extend list
            dl.extend(v.split())
    return dl

def most_common_word(d):
    wordcount = {}
    ## create a dictionary of words from d1 and generate frequency count
    dl =[]
    wordlist = word_list(dl,d)
    return Counter(wordlist).most_common(1)[0][0]

def print_dictionary(d, i=1):
    for k, v in d.items():
        a = ('+' * i + ' ' + str(k) + ': ')
        if isinstance(v, dict):
            print('+' * i + ' ' + str(k) +': ')
            print_dictionary(v, i+1)
        else:
            print(a + ' ' + str(v))

def set_list(user, element = None):
    #local = data
    #print(local)
    #temp = {}
    final = ' '.join(user[2:])
    #key_list = user[1].split('/').join(final)
    print(key_list)
    #for f in user[1].split('/'):


    #    local[f] = {}
    #    local = local[f]
    #print(local)
    #print(data)

    #for i in reversed(key_list):

    #print(i)
    #for k, v in d.items():
    #data[key_list[0]] = ' '.join(user[2:]) #turns the last words into a string value #

def build_dictionary(d,k):
    if len(k) == 0:
        return update_dictionary(data,d)
    else:
        d0 = {}
        d0[k[-1]] = d
        k.pop()
        build_dictionary(d0,k)

def update_dictionary(d,u):
    #print("Entered updated")
    #print(u)
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update_dictionary(d.get(k, {}), v)
        else:
            try:
                d[k] = v    ## FAILS when adding a dictionary deeper than you defined
            except:
                print("You cannot enter a dictionary in the same branch as the leaf")
    return d

def delete_branch(d,u):
    return
######
#
#   Runtime code
#

print("\nYou can modify the dictionary with 'set key/key2/etc value' or 'del key'.  Type 'quit' to exit\n")
while True:
## Print Dictionary in
    print_dictionary(data)
    #print(data)
## Print word that occurs the most:
    print("\nMost common word:", most_common_word(data))
## Prompt user
    user = input("\nInput a command: ").split()
## Confirm input to set or del
    if user[0] == 'quit':
        print("Thanks for playing.")
        exit()
## If set --> modify / add the value
    elif user[0] == 'set':
        ## Error check for no value
        ## Create final dictionary element
        value = ' '.join(user[2:])
        ## ERROR: if spaces in key key_list ... incorrect parsing
        ## Pass value to add Dictionary
        key_list = user[1].split('/')
        last_dictionary_element = {key_list[-1]: value}
        key_list.pop()
        new_dict = build_dictionary(last_dictionary_element, key_list)

## If del --> 1) Check if value exists Yes: Delete w/ dependents No: Err
    elif user[0] == 'del':
        if data.get(user[1]) != None:
            key_list = user[1].split('/')
            del data[user[1]]
    else:
        print("Please input a valid command")
