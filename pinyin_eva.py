import argparse
import json
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool

from utils.viterbi import viterbi

from utils import params
from utils.tools import *

from utils.evaluate import evaluate

input_file_path     = ''
output_file_path    = ''
model_path          = ''
pinyin_dict:        dict
model:              dict

def worker(lines: list, b1, b2):
    this_out = output_file_path + f'_{round(b1, 1)}_{round(b2, 1)}.txt'
    with open(this_out, 'w', encoding='utf-8') as output_file:
        for line in lines:
            res = viterbi(line.strip().lower(), pinyin_dict, model,
                          [b1, b2])
            print(res, file=output_file)
    # close output file
    eval = [round(b1, 1), round(b2, 1),
            evaluate(params.ans_file, this_out)
    ]
    print(eval, sep=' ')
    return eval


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Pinyin Input Method',
        description='Pinyin to Chinese.',
        allow_abbrev=True,
    )

    parser.add_argument('-i', '--input-file', dest='input_file_path', type=str, default=params.input_test_file, help="Input file")

    parser.add_argument('-o', '--output-file', dest='output_file_path', type=str, default=params.output_test_file, help="Output file")

    parser.add_argument('-m', '--model-file', dest='model_path', type=str, default=params.model_path, help="path to model")

    parser.add_argument('--pinyin-dict', dest='pinyin_dict_path', type=str, default=params.pinyin_dict_json, help="path to pinyin dict")

    parser.add_argument('-b', '--betas', dest='betas', type=float, nargs=2, default=params.betas, help="betas")

    parser.add_argument('-p', '--process-number', dest='process_number', type=int, default=params.process_number, help="number of processes simultaneously")

    # Load args
    args = parser.parse_args()
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path
    model_path = args.model_path
    pinyin_dict_path = args.pinyin_dict_path
    process_number = args.process_number

    # loading
    with open(pinyin_dict_path) as f:
        pinyin_dict = json.load(f)
    model = load_model(model_path)

    output_file_path = './test/output'
    # process the input
    with open('report.txt', 'w') as rep:
        results = []
        pool = Pool(processes=process_number)
        with open(input_file_path) as input_file:
            lines = input_file.readlines()
            for b1 in np.arange(0.1, 1.0, 0.1):
                for b2 in tqdm(np.arange(0.1, 1.0 - b1, 0.1)):
                    if round(b1, 1) + round(b2, 1) > 0.99:
                        continue
                    results.append(pool.apply_async(
                        worker, args=(lines, b1, b2))
                    )
            pool.close()
            pool.join()
        # completed
        for r in results:
            print(r.get(), file=rep)
        #print(*[r.get() for r in results], sep='\n', file=rep)
