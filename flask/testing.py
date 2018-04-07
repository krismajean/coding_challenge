

d = {
    'a' : {'a1': 'apple value_a1','a2': 'angry apple value_a2'},
    'b' : {'key_2': 'value_2'},
    'c' : 'big baby apple always',
    'd' : 'cuddly cute big baby apple',
    'e' : {'e1': {'e11' : 'welcome to the basement', 'e12' : 'dark'}, 'e2': 'happy' },
    'f' : 'funny you looked'
        }

test = dictionary.get('d')
print(test)

if dictionary.get('d') != None:
    print("Found it")
else:
    print("Can't find it")


assert get({'a': 'b'}, 'c') is None
assert get({'a': 'b'}, ['c']) is None
assert get({'a': 'b'}, ['c', 'd']) is None
assert get({'a': 'b'}, ['a', 'c']) is None
assert get({'a': 'b'}, []) is None
assert get({'a': 'b'}, ['a']) is'b'
assert get({'a': {'b': 'c'}}, ['a', 'c']) is None
assert get({'a': {'b': 'c'}}, ['a', 'b']) is 'c'

assert search({'a': 'b'}, 'c') is None
assert search({'a': 'b'}, ['c']) is None
assert search({'a': 'b'}, ['c', 'd']) is None
assert search({'a': 'b'}, ['a', 'c']) is None
assert search({'a': 'b'}, []) is None
assert search({'a': 'b'}, ['a']) is'b'
assert search({'a': {'b': 'c'}}, ['a', 'c']) is None
assert search({'a': {'b': 'c'}}, ['a', 'b']) is 'c'

y = ['a','a1']
n = ['f','g']
o = ['bitch']

def get(dictionary, list_of_keys):
    try:
        return dictionary[list_of_keys]
    except:
        return None


def get(dictionary, list_of_keys):
    if len(list_of_keys) != 0 and isinstance(list_of_keys,list) and list_of_keys[0] in dictionary:
        v = dictionary[list_of_keys[0]]
        if isinstance(v, dict):
            return get(v,list_of_keys[1:])
        if len(list_of_keys) == 1:
            return v
        else:
            return None
    return None

def search(dictionary, list_of_keys):
    if len(list_of_keys) != 0 and isinstance(list_of_keys,list) and list_of_keys[0] in dictionary:
        for counter, value in enumerate(list_of_keys):
            if value in dictionary:
                if isinstance(dictionary[value], dict):
                    dictionary = dictionary[value]
                elif value == list_of_keys[-1]: #check if end of list
                    return dictionary[value]
                else:
                    return None
            else:
                return None
    else:
        return None

test = {'a': {'b': {'c': 'd'}}}
search({'a': {'b': {'c': 'd'}}}, ['a','b','c'])

delete_key({'a': {'b': {'c': 'd'}}}, ['c'])
print(search({'a': {'b': {'c': 'd'}}}, ['a','b','c']))

def delete_keys(dict_del, lst_keys):
    for k in lst_keys:
        try:
            dict_del.pop(k)
        except KeyError:
            pass
    for v in dict_del.values():
        if isinstance(v, dict):
            delete_keys_from_dict(v, lst_keys)
    return dict_del

def delete_key(dictionary, list_of_keys):
    if len(list_of_keys) != 0 and isinstance(list_of_keys,list) and list_of_keys[0] in dictionary:
        for value in list_of_keys:
            if value in dictionary:
                if isinstance(dictionary[value], dict):
                    dictionary = dictionary[value]
                elif value == list_of_keys[-1]: #check if end of list
                    del dictionary[value]
                    print("Deleted value and returning remaining dictionary")
                    return dictionary
                else:
                    print("")
                    return None
            else:
                return None
    else:
        return dictionary

delete_keys_from_dict({'a': {'b': {'c': 'd'}}}, ['a','b','c'])

def delete_key_from_dict(dict_del, list_keys):
    for i in list_of_keys:
        dict_del[i]
    for key, value in dict_del.items():
        if isinstance(value, dict):
            delete_keys_from_dict(value, lst_keys)
    return dict_del


assert False is False
assert None is None
assert False is None


ab = {'a': {'b': {'c': 'd'}}, 'a2': ''}
ab.get()

search({'a': 'b'}, ['a', 'c'])

get({'a': {'b': {'c': 'd'}}}, ['a','b','c'])


should return either the nested value, or Non


key=['a','b']
value=['e']

building = {1}

def build(key_list,value):
    d = {}
    for key in reversed(key_list):
        d[key] = value
        value = key
    print(d)
    #return d

print(build(['a','b'],['c']))




delete_keys_from_dictionary({'a':{'b':'c'}},['a','b'])

def delete_key_from_dictionary(nested, key_list):
    ''' Returns a dictionary with the final key in the key_list deleted'''
    #if get_dictionary_value_with_key_list(dict_del,key_list) == None: return dict_del
    for key, value in iter(nested.items()):

    for counter, key in enumerate(key_list):
        if key in nested and counter != depth:

        try:
            dict_del.pop(key)
        except KeyError:
            pass
    for value in dict_del.values():
        if isinstance(value, dict):
            delete_keys_from_dictionary(value, key_list)





def delete_keys_from_dict(dict_del, lst_keys):
    for k in lst_keys:
        try:
            del dict_del[k]
        except KeyError:
            pass
    for v in dict_del.values():
        if isinstance(v, dict):
            delete_keys_from_dict(v, lst_keys)
    return dict_del


def del_key(dict_del, key_list):
    if len(key_list) == 1:
        print(dict_del)
        print(key_list[0])
        remove = key_list[0]
        del dict_del[remove]
    if isinstance(dict_del[key_list[0]], dict):
        del_key(dict_del[key_list[0]], key_list[1:])
    return dict_del

del_key({'1':{'2':'3','2a':'3a'}},['1','2a'])


y = {'2':'3','2a':'3a'}
