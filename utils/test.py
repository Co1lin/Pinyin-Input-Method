from tools import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Train Pinyin Input Method',
        description='Train Script',
        allow_abbrev=True,
    )

    parser.add_argument('-a', '--alphas', dest='alphas', type=int, nargs=3, default=[1,2,3], help="proportions of arguments to save for 1, 2, 3 gram")

    args = parser.parse_args()

    print(args.alphas)