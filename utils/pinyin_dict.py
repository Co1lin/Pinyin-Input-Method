import argparse
import json
from tqdm import tqdm

def generate(pinyin_dict_path):
    '''
    Generate pinyin to character dict
    :return: a dict
    '''
    with open(pinyin_dict_path) as pinyin_dict:
        res = {}
        for line in tqdm(pinyin_dict):
            line = line.split()
            chars = line[1:]
            res[line[0]] = chars

        res['start'] = '>'
        res['end'] = '<'
        return res

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Generate pinyin to character dict',
        description='Dict Generation Script',
        allow_abbrev=True,
    )

    parser.add_argument('--pinyin-dict', dest='pinyin_dict_path', type=str, default='./material/pinyin_dict.txt',
                        help="path to dir where to store the processed data")

    parser.add_argument('-o', '--output-path', dest='output_path', type=str, default='./utils/pinyin_dict.json',
                        help="path to where to save the dict")

    # load args
    args = parser.parse_args()
    pinyin_dict_path = args.pinyin_dict_path
    output_path = args.output_path

    # generate
    res = generate(pinyin_dict_path)

    # save
    with open(output_path, 'w') as f:
        json.dump(res, f, ensure_ascii=False)
