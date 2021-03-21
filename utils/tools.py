'''
some useful functions
'''
import os
import numpy as np

def is_chinese(char):
    return '\u4e00' <= char <= '\u9fa5'

def dir_path(path):
    if path[-1] == '/':
        path = path[:-1]
    return path

def path2name(path):
    return path.split('/')[-1]

def get_docs(docs_dir_path, keyword):
    '''
    :param docs_dir_path: path of dir containing docs needed
    :param keyword: only the files whose names contain the keyword will be returned
    :return: a list of filename
    '''
    docs_list = os.listdir(docs_dir_path)

    for i in range(len(docs_list) - 1, -1, -1):
        if keyword not in docs_list[i]:
            docs_list.pop(i)
        else:
            docs_list[i] = docs_dir_path + '/' + docs_list[i]

    return docs_list

def add_dict_(x, y):
    '''
    merge model y to model x
    :return: merged model x
    '''
    for key in set(x) | set(y):
        if key in x:
            if isinstance(x[key], dict):
                add_dict_(x[key], y[key])
            else:
                x[key] += y.get(key, 0)
        else:
            x[key] = y[key]

def load_model(model_path):
    print('Loading model...')
    model = dict(np.load(model_path, allow_pickle=True))['arr_0'][()]
    print('Model loaded!')
    return model