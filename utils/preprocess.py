import json
import argparse
from tqdm import tqdm
from p_tqdm import p_map
from functools import partial

from tools import *

def flag_sign(char):
    return  char == ',' or char == '，' or \
            char == '。' or char == '!' or char == '！' or \
            char == '…' or char == '?' or char == '？' or \
            char == ':' or char == '：' or \
            char == '\"' or char == '；'

def is_skip_sign(char):
    return char == '“' or char == '”' or char == ' '

def _process_str(string, token):
    '''
    process a single string
    :return: a list which is got by splitting the string by untokenized characters
    '''
    res = []
    start_sign = '>'
    while string:
        last_len = len(string)
        for i in range(0, last_len):
            if not is_chinese(string[i]):

                if is_skip_sign(string[i]):
                    string = string[:i] + string[i + 1:]
                    break

                substr = string[:i]
                if substr:
                    if len(substr) >= 5:
                        substr = '>' + substr + '<'
                    res.append(substr + '\n')
                string = string[i + 1:]
                break

        if  last_len == len(string):
            if string:
                if len(string) >= 5:
                    string = '>' + string + '<'
                res.append(string + '\n')
            break

    return res

def _process_doc(doc_path, process_id, token):
    '''
    delete untokenized characters and split the content into lines
    '''
    lines = []
    with open(doc_path) as doc:

        doc_lines = doc.readlines()
        for doc_line in tqdm(doc_lines, position=process_id,
                             postfix=f"Process #{process_id}: {doc_path}"):
            doc_line = json.loads(doc_line)
            # read 'html' and 'title'
            lines += _process_str(doc_line['title'], token)
            lines += _process_str(doc_line['html'], token)
        # end process this doc
    # close this doc
    output_file = output_dir + '/processed_' + path2name(doc_path)
    with open(output_file, 'w') as f:
        f.writelines(lines)

def process(docs_path, token):

    p_map(partial(_process_doc, token=token),
          docs_path,
          range(1, len(docs_path) + 1),
          num_cpus=process_number)


docs_dir_path       = ''
keyword             = ''
token_path          = ''
process_number      = 0
output_dir          = ''


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Data Preprocessing for Pinyin Input Method',
        description='Preprocess Script',
        allow_abbrev=True,
    )

    parser.add_argument('-docs', '--docs-dir', dest='docs_dir_path', type=str, default='./material/sina_news_gbk', help="docs file for training")

    parser.add_argument('-k', '--keyword', dest='keyword', type=str, default='2016', help='select files as docs only when their filename contain this keyword')

    parser.add_argument('-t', '--token-path', dest='token_path', type=str, default='./utils/token.json', help="path to token file")

    parser.add_argument('-p', '--process-number', dest='process_number', type=int, default='4', help="number of processes simultaneously")

    parser.add_argument('-o', '--output-dir', dest='output_dir', type=str, default='./processed_data', help="path to dir where to store the processed data")

    # load args
    args = parser.parse_args()
    docs_dir_path = dir_path(args.docs_dir_path)
    keyword = args.keyword
    process_number = args.process_number
    token_path = args.token_path
    output_dir = dir_path(args.output_dir)

    # process
    token = {}
    with open(token_path) as token_file:
        token = json.load(token_file)
    docs_path = get_docs(docs_dir_path, keyword)
    process(docs_path, token)