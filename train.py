import os
import json
import argparse
import numpy as np
from tqdm import tqdm

from utils.tools import *

def get_docs(docs_dir_path, keyword):
    '''
    :param docs_dir_path: path of dir containing docs for training
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

def generate_dict(dict_path):
    '''
    :param path to dict_path:
    :return: a dict: character -> index number
    '''
    token_dict = {}
    with open(dict_path) as dict_file:

        chars = dict_file.read()
        for i in range(0, len(chars)):
            token_dict[chars[i]] = i

    return token_dict

def _train_str(token, string, model):
    '''
    update statistics in the model using the string
    :param string:
    :return: nothing
    '''
    last_char_token = -1
    for char in string:

        if is_chinese(char):
            # number of single character occurrence
            char_token = -1
            try:
                char_token = token[char]
            except KeyError:
                pass
            except Exception as e:
                print(e)
                raise
            else:
                model['1'][char_token] += 1
                # number of simultaneous occurrence of two characters
                if last_char_token >= 0:  # is a Chinese character
                    model['2'][last_char_token][char_token] += 1
                last_char_token = char_token
        else:
            last_char_token = -1


def train(token, docs):
    '''

    :param token: token dict
    :param docs: docs filenames list (not)
    :return: a model in json format contains:
    '''
    size = len(token)
    model = {
        'size': size,
        '1':    np.zeros(size),
        '2':    np.zeros([size, size]),
    }
    for doc in tqdm(docs):

        with open(doc) as doc_file:
            print("Processing: ", doc)
            doc_lines = doc_file.readlines()
            for doc_line in tqdm(doc_lines, leave=False):
                doc_line = json.loads(doc_line)
                # read 'html' and 'title'
                _train_str(token, doc_line['title'], model)
                _train_str(token, doc_line['html'], model)
            # end process this doc
        # close this doc
    #end loop docs
    return model


docs_dir_path   = ''
dict_path       = ''
token_path      = ''
model_path      = ''
keyword         = ''

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='Train Pinyin Input Method',
        description='Train Script',
        allow_abbrev=True,
    )

    parser.add_argument('-docs', '--docs-dir', dest='docs_dir_path', type=str, default='./material/sina_news_gbk', help="docs file for training")

    parser.add_argument('-k', '--keyword', dest='keyword', type=str, default='2016', help='select files as docs only when their filename contain this keyword')

    parser.add_argument('-dict', '--dict-path', dest='dict_path', type=str, default='./material/chars.txt', help="dictionary file (contains characters in one line) path")

    parser.add_argument('-v', '--token-path', dest='token_path', type=str, default='token.json', help="token file path to save")

    parser.add_argument('-m', '--model-path', dest='model_path', type=str, default='model.npy', help="model file path to save")

    # load args
    args = parser.parse_args()
    docs_dir_path = args.docs_dir_path
    keyword = args.keyword
    dict_path = args.dict_path
    if dict_path[-1] == '/':
        dict_path = dict_path[:-1]
    token_path = args.token_path
    model_path = model_path

    # preprocess
    docs = get_docs(docs_dir_path, keyword)
    token = generate_dict(dict_path)

    # train
    model = train(token, docs)

    pass