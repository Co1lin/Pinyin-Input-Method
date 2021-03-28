import json
import argparse
from tqdm import tqdm
from p_tqdm import p_map
from functools import partial

from ChineseTone import *

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
print(sys.path)
from utils.tools import *

def is_skip_sign(char):
    return char == '“' or char == '”' or char == ' '

def _process_str(string):
    '''
    process a single string
    :return: a list which is got by splitting the string by untokenized characters
    '''
    res = []
    while string:
        last_len = len(string)
        for i in range(0, last_len):
            if not is_chinese(string[i]):
                if is_skip_sign(string[i]):
                    string = string[:i] + string[i + 1:]
                    break

                substr = string[:i]
                if len(substr) > 3:
                    res.append(substr + '\n')
                string = string[i + 1:]
                break

        if  last_len == len(string):
            if len(string) > 3:
                res.append(string + '\n')
            break

    return res

def process(docs_path):

    results = []
    for doc_path in tqdm(docs_path):
        with open(doc_path) as doc:
            lines = doc.readlines()
            for line in lines:
                results += _process_str(line)
        # close doc
    # save ans data
    with open(ans_path, 'w') as f:
        f.writelines(results)

    # generate test data
    with open(output_path, 'w') as f:
        for line in tqdm(results):
            print(
                *(PinyinHelper.convertToPinyinFromSentence(
                    line[:-1], pinyinFormat=PinyinFormat.WITHOUT_TONE
                )), file=f
            )


docs_dir_path       = ''
keyword             = ''
output_path         = ''
ans_path            = ''

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Generate Test Data for Pinyin Input Method',
        description='Test Data Generation Script',
        allow_abbrev=True,
    )

    parser.add_argument('-docs', '--docs-dir', dest='docs_dir_path', type=str, default='test_data/society')

    parser.add_argument('-k', '--keyword', dest='keyword', type=str, default='4')

    parser.add_argument('-o', '--output', dest='output_path', type=str, default='test_data/test_data.txt')

    parser.add_argument('-a', '--ans', dest='ans_path', type=str, default='test_data/test_ans.txt')

    # load args
    args = parser.parse_args()
    docs_dir_path = dir_path(args.docs_dir_path)
    keyword = args.keyword
    output_path = args.output_path
    ans_path = args.ans_path

    # process
    docs_path = get_docs(docs_dir_path, keyword)
    process(docs_path)