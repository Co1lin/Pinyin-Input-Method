import argparse
import os
import numpy as np

import params

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Accuracy Test for Pinyin Input Method',
        description='Test Script',
        allow_abbrev=True,
    )

    parser.add_argument('-i', '--input', dest='input_path', type=str, default='./test/input.txt')

    parser.add_argument('-a', '--ans', dest='ans_path', type=str, default='./test/ans.txt')

    parser.add_argument('-o', '--output', dest='output_path', type=str, default='./test/output.txt')

    parser.add_argument('-m', '--model', dest='model_path', type=str, default=params.model_path)

    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    ans_path = args.ans_path
    model_path = args.model_path

    # run
    os.popen(f'python pinyin.py -i {input_path} -o {output_path} -m {model_path}').readlines()

    # compare
    output  : list
    ans     : list
    with open(output_path) as f:
        output = f.readlines()
    with open(ans_path) as f:
        ans = f.readlines()

    total, right = 0, 0
    for i in range(len(output)):

        x = np.array(list(output[i].strip()))
        y = np.array(list(ans[i].strip()))
        total += x.shape[0]
        right += np.sum(x == y)

    print(right / total)