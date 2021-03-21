import argparse
import numpy as np

from tools import *

def merge(checkpoints):
    '''
    merge checkpoints to a model
    :return: a model
    '''
    model = {
        1: {},
        '1_total': 0,
        2: {},
        '2_total': 0,
        3: {},
        '3_total': 0,
    }

    for checkpoint_npz in checkpoints:
        print('Load:', checkpoint_npz)
        checkpoint = load_model(checkpoint_npz)
        print('Merge...', checkpoint_npz)
        add_dict_(model, checkpoint)

    print('Merge completed!')

    return model

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='Merge models of Pinyin Input Method',
        description='Merge Script',
        allow_abbrev=True,
    )

    parser.add_argument('-c', '--checkpoints-dir', dest='checkpoints_dir_path', type=str, default='./checkpoints', help="path to dir containing checkpoints")

    parser.add_argument('-k', '--keyword', dest='keyword', type=str, default='processed',
                        help='select files as checkpoints only when their filename contain this keyword')

    parser.add_argument('-m', '--model-path', dest='model_path', type=str, default='./checkpoints/model.npy',
                        help="model file path to save")

    # load args
    args = parser.parse_args()
    checkpoints_dir_path = dir_path(args.checkpoints_dir_path)
    keyword = args.keyword
    model_path = args.model_path

    # get checkpoints
    checkpoints = get_docs(checkpoints_dir_path, keyword)

    # merge
    model = merge(checkpoints)
    print('Merge completed: ')

    # save
    np.savez_compressed(model_path, model)
