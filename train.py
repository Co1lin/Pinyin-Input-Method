import os
import json
import argparse
import numpy as np
from tqdm import tqdm
from p_tqdm import p_map
from functools import partial

from utils.tools import *
import utils.params as params

def update_dict(d, k):
    if k not in d:
        d[k] = 1
    else:
        d[k] += 1

def _train_str(string, model):
    '''
    update statistics in the model using the single line string
    :return: a model trained by only the given string
    '''
    for i in range(0, len(string)):
        model['1_total'] += 1
        update_dict(model[1], string[i])
        pair = string[i : i + 2]
        if len(pair) == 2:
            model['2_total'] += 1
            update_dict(model[2], pair)
            triple = string[i : i + 3]
            if len(triple) == 3:
                model['3_total'] += 1
                update_dict(model[3], triple)

    return model

def _train_datum(datum_path, process_id):
    '''
    train the model using a single doc
    :param process_id: id of process
    :return: a model trained by only the given doc
    '''
    model = {
        1: {},
        '1_total': 0,
        2: {},
        '2_total': 0,
        3: {},
        '3_total': 0,
    }
    with open(datum_path) as datum_file:

        datum_lines = datum_file.readlines()
        for datum_line in tqdm(datum_lines, position=process_id,
                               postfix=f"Process #{process_id}: {datum_path}"):
            _train_str(datum_line[:-1], model)
        # end process this line
    # close this datum_file
    # save result of this process
    np.savez_compressed(checkpoints_path + '/' + path2name(datum_path) + '.npz', model)
    return model


def train(data_path, alphas: list):
    '''
    train the model using docs from docs list
    :param token: token dict
    :param docs: docs filenames list (not)
    :return: a model in json format contains:
    '''
    model = {
        1: {},
        '1_total': 0,
        2: {},
        '2_total': 0,
        3: {},
        '3_total': 0,
    }
    if data_path: # is not empty
        # split the task into multi-processes by p_tqdm
        results = p_map(_train_datum,
                        data_path,
                        range(1, len(data_path) + 1),
                        num_cpus=process_number)
        # merge the results
        print('Merge results from all processes...')
        for res in tqdm(results):
            add_dict_(model, res)

    # select
    print(f'Selected top items according to alphas = {alphas} ...')
    for i in tqdm(range(1, 4)):
        length = len(model[i])
        model[i] = dict(sorted(model[i].items(),
                          key= lambda kv:(kv[1], kv[0]),
                          reverse=True)[:int(length * alphas[i - 1])]
                        )

    return model

data_dir_path       = ''
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

    parser.add_argument('-d', '--data-dir', dest='data_dir_path', type=str, default='./processed_data', help="preprocessed data file for training")

    parser.add_argument('-k', '--keyword', dest='keyword', type=str, default='2016', help='select files as docs only when their filename contain this keyword')

    parser.add_argument('-m', '--model-path', dest='model_path', type=str, default=params.model_path, help="model file path to save")

    parser.add_argument('-c', '--checkpoints-path', dest='checkpoints_path', type=str, default='./checkpoints', help="path to checkpoints directory")

    parser.add_argument('-p', '--process-number', dest='process_number', type=int, default='4', help="number of processes simultaneously")

    parser.add_argument('-a', '--alphas', dest='alphas', type=float, nargs=3, default=params.alphas, help="proportions of arguments to save for 1-, 2-, 3-gram")

    # load args
    args = parser.parse_args()
    data_dir_path = dir_path(args.data_dir_path)
    keyword = args.keyword
    model_path = args.model_path
    checkpoints_path = dir_path(args.checkpoints_path)
    process_number = args.process_number

    # preprocess
    data_path = get_docs(data_dir_path, keyword)

    # train
    model = train(data_path, args.alphas)

    # save
    model_path = model_path[:-4]
    model_path += f'_{args.alphas[0]}_{args.alphas[1]}_{args.alphas[2]}.npz'
    print(f'Saving {model_path} ...')
    np.savez_compressed(model_path, model)
