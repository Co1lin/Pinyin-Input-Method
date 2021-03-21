import argparse
import os
import numpy as np

def evaluate(output_path, ans_path):
    # get result
    output: list
    ans: list
    with open(output_path) as f:
        output = f.readlines()
    with open(ans_path) as f:
        ans = f.readlines()

    # compare and evaluate
    total, right = 0, 0
    for i in range(len(output)):
        x = np.array(list(output[i].strip()))
        y = np.array(list(ans[i].strip()))
        total += x.shape[0]
        try:
            right += np.sum(x == y)
        except ValueError as e:
            print(e)
            print(f'x: {x}')
            print(f'y: {y}')
            raise

    accuracy = right / total
    print(accuracy)
    return accuracy

if __name__ == '__main__':

    import params

    parser = argparse.ArgumentParser(
        prog='Accuracy Test for Pinyin Input Method',
        description='Test Script',
        allow_abbrev=True,
    )

    parser.add_argument('-i', '--input', dest='input_path', type=str, default=params.input_test_file)

    parser.add_argument('-a', '--ans', dest='ans_path', type=str, default=params.ans_file)

    parser.add_argument('-o', '--output', dest='output_path', type=str, default=params.output_test_file)

    parser.add_argument('-m', '--model', dest='model_path', type=str, default=params.model_path)

    parser.add_argument('-r', '--report', dest='report_path', type=str, default=params.report_path)

    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    ans_path = args.ans_path
    model_path = args.model_path
    report_path = args.report_path

    # run
    print(
        *os.popen(f'(/usr/bin/time -f"%e Sys: %S Usr: %U Mem: %M KB"\
         python pinyin.py -i {input_path} -o {output_path} -m {model_path} \
         ) 2>&1').readlines()
    )

    eva = evaluate(output_path, ans_path, report_path)
    print(eva)
    with open(report_path, 'w') as f:
        print(eva, file=f)