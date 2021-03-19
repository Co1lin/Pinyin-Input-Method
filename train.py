import os
import json
import argparse
import numpy as np
from tqdm import tqdm

from utils.tools import *
import utils.params as params


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


def _train_str(token, string, model):
    '''
    update statistics in the model using the string
    :param string:
    :return: nothing (model passed as reference, so it is modified in this function)
    '''
    last_char_token = params.START_TOKEN # 0 corresponds to the starting sign
    for char in string:

        if is_chinese(char):
            # number of single character occurrence
            char_token = -1
            try:
                char_token = token[char]
            except KeyError:    # char is not in dictionary, ignore it
                pass
            except Exception as e:  # unexpected error
                print(e)
                raise
            else:   # char is in dictionary
                model['1'][char_token] += 1
                # number of simultaneous occurrence of two characters
                if last_char_token >= 0:  # is a Chinese character
                    model['2'][last_char_token][char_token] += 1
                last_char_token = char_token
        else:
            last_char_token = -1
    # end loop of string
    # deal with the ending sign (token: 1)
    if last_char_token >= 0:
        model['2'][last_char_token][params.END_TOKEN] += 1


def train(token, docs, model_path):
    '''
    train the model using docs from docs list
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
    i = 0
    for doc in tqdm(docs):
        i += 1
        with open(doc) as doc_file:
            print("Processing: ", doc)
            doc_lines = doc_file.readlines()
            for doc_line in tqdm(doc_lines):
                doc_line = json.loads(doc_line)
                # read 'html' and 'title'
                _train_str(token, doc_line['title'], model)
                _train_str(token, doc_line['html'], model)
            # end process this doc
        # close this doc
        np.save(model_path + '.' + str(i), model)
    # end loop docs
    return model


docs_dir_path   = ''
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

    parser.add_argument('-t', '--token-path', dest='token_path', type=str, default='token.json', help="path to token file")

    parser.add_argument('-m', '--model-path', dest='model_path', type=str, default='model.npy', help="model file path to save")

    # load args
    args = parser.parse_args()
    docs_dir_path = args.docs_dir_path
    keyword = args.keyword
    token_path = args.token_path
    model_path = args.model_path

    # preprocess
    docs = get_docs(docs_dir_path, keyword)
    token = {}
    with open(token_path) as token_file:
        token = json.load(token_file)

    # train
    model = train(token, docs, model_path)

    # save
    np.save(model_path, model)

    pass