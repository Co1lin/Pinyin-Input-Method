import argparse
import json
import numpy as np
from utils.viterbi import viterbi

from utils import params

input_file_path     = ''
output_file_path    = ''
model_path          = ''

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Pinyin Input Method',
        description='Pinyin to Chinese.',
        allow_abbrev=True,
    )

    parser.add_argument('-i', '--input-file', dest='input_file_path', type=str, default='input.txt', help="Input file")

    parser.add_argument('-o', '--output-file', dest='output_file_path', type=str, default='output.txt', help="Output file")

    parser.add_argument('-m', '--model-file', dest='model_path', type=str, default=params.model_path,
                        help="path to model")

    parser.add_argument('--pinyin-dict', dest='pinyin_dict_path', type=str, default='utils/pinyin_dict.json',
                        help="path to pinyin dict")

    parser.add_argument('-b', '--betas', dest='betas', type=float, nargs=2, default=[0.8, 0.8],
                        help="betas")

    # Load args
    args = parser.parse_args()
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path
    model_path = args.model_path
    pinyin_dict_path = args.pinyin_dict_path

    # loading
    pinyin_dict: dict
    with open(pinyin_dict_path) as f:
        pinyin_dict = json.load(f)
    model: dict
    with open(model_path) as f:
        print('Loading model...')
        model = dict(np.load(model_path, allow_pickle=True))['arr_0'][()]
        print('Model loaded!')

    # process the input
    with open(input_file_path) as input_file:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:

            lines = input_file.readlines()
            for line in lines:
                res = viterbi(line.strip().lower(), pinyin_dict, model, args.betas)
                output_file.write(res)
                output_file.write('\n')
