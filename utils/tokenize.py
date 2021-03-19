'''
Tokenizer
Read in dictionary file, and
save token file
'''
import json
import argparse
import tqdm

def tokenize(dict_path):
    '''
    :param path to dict_path:
    :return: a dict: character -> index number
    '''
    token_dict = {}
    with open(dict_path) as dict_file:

        chars = dict_file.read()
        print("Tokenizing...")
        token_dict['START'] = 0
        token_dict['END'] = 1
        for i in tqdm( range(0, len(chars)) ):
            token_dict[chars[i]] = i + 2

    return token_dict


dict_path       = ''
token_file_path       = ''

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Tokenizer for Pinyin Input Method',
        description='Tokenization Script',
        allow_abbrev=True,
    )

    parser.add_argument('-dict', '--dict-path', dest='dict_path', type=str, default='./material/chars.txt', help="dictionary file (contains characters in one line) path")

    parser.add_argument('-o', '--output-token-path', dest='token_file_path', type=str, default='./material/token.json', help="path to save token file")

    # load args
    args = parser.parse_args()
    dict_path = args.dict_path
    token_file_path = args.token_file_path

    # processing
    token_dict = tokenize(dict_path)

    # saving
    with open(token_file_path) as token_file:
        json.dump(token_dict, token_file)

