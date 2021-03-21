import json
import argparse
from tqdm import tqdm
from p_tqdm import p_map
from functools import partial

from tools import *
import params

def is_skip_sign(char):
    return char == '“' or char == '”' or char == ' '

def _process_str(string):
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

def _process_doc(doc_path, process_id):
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
            lines += _process_str(doc_line['title'])
            lines += _process_str(doc_line['html'])
        # end process this doc
    # close this doc
    output_file = output_dir + '/processed_' + path2name(doc_path)
    with open(output_file, 'w') as f:
        f.writelines(lines)

def process(docs_path):

    p_map(partial(_process_doc),
          docs_path,
          range(1, len(docs_path) + 1),
          num_cpus=process_number)


docs_dir_path       = ''
keyword             = ''
process_number      = 0
output_dir          = ''


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Data Preprocessing for Pinyin Input Method',
        description='Preprocess Script',
        allow_abbrev=True,
    )

    parser.add_argument('-docs', '--docs-dir', dest='docs_dir_path', type=str, default=params.docs_dir, help="docs file for training")

    parser.add_argument('-k', '--keyword', dest='keyword', type=str, default=params.docs_keyword, help='select files as docs only when their filename contain this keyword')

    parser.add_argument('-p', '--process-number', dest='process_number', type=int, default=params.process_number, help="number of processes simultaneously")

    parser.add_argument('-o', '--output-dir', dest='output_dir', type=str, default=params.processed_data, help="path to dir where to store the processed data")

    # load args
    args = parser.parse_args()
    docs_dir_path = dir_path(args.docs_dir_path)
    keyword = args.keyword
    process_number = args.process_number
    output_dir = dir_path(args.output_dir)

    # process
    docs_path = get_docs(docs_dir_path, keyword)
    process(docs_path)