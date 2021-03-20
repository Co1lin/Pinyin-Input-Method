import os
import json
import argparse
import numpy as np
from tqdm import tqdm
from p_tqdm import p_map
from functools import partial

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
    :return: a model trained by only the given string
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

    return model

def _train_doc(doc_path, process_id, token):
    '''
    train the model using a single doc
    :param process_id: id of process
    :return: a model trained by only the given doc
    '''
    size = len(token)
    model = {
        'size': size,
        '1': np.zeros(size),
        '2': np.zeros([size, size]),
    }
    with open(doc_path) as doc_file:

        doc_lines = doc_file.readlines()
        for doc_line in tqdm(doc_lines, position=process_id, postfix=f"Process #{process_id}: {doc_path}"):
            doc_line = json.loads(doc_line)
            # read 'html' and 'title'
            _train_str(token, doc_line['title'], model)
            _train_str(token, doc_line['html'], model)
        # end process this doc
    # close this doc
    # save result of this process
    np.save(checkpoints_path + '/checkpoints_' + str(process_id) + '.npy', model)
    return model


def train(token, docs_path):
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
    # split the task into multi-processes by p_tqdm
    results = p_map(partial(_train_doc, token=token),
                    docs_path,
                    range(1, len(docs_path) + 1),
                    num_cpus=process_number)
    # merge the results
    for res in results:
        model['1'] += res['1']
        model['2'] += res['2']

    return model


docs_dir_path       = ''
keyword             = ''
token_path          = ''
model_path          = ''
checkpoints_path    = ''
process_number      = 0

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

    parser.add_argument('-c', '--checkpoints-path', dest='checkpoints_path', type=str, default='./checkpoints', help="path to checkpoints directory")

    parser.add_argument('-p', '--process-number', dest='process_number', type=int, default='4', help="number of processes simultaneously")

    # load args
    args = parser.parse_args()
    docs_dir_path = dir_path(args.docs_dir_path)
    keyword = args.keyword
    token_path = args.token_path
    model_path = args.model_path
    checkpoints_path = dir_path(args.checkpoints_path)
    process_number = args.process_number

    # preprocess
    docs = get_docs(docs_dir_path, keyword)
    token = {}
    with open(token_path) as token_file:
        token = json.load(token_file)

    # train
    model = train(token, docs)

    # save
    np.save(model_path, model)

    pass