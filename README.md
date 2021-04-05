# Pinyin-Input-Method

Pinyin input method in Python. Homework of Intro. to AI course, 2021 Spring @THU.

## Usage

The easiest way to convert pinyin to Chinese is running the following command in the root directory of this repo:

```shell
python pinyin.py
```

while the input file is `input.txt` which should look like:

```
qing hua da xue ji suan ji xi
wo shang xue qu le
jin tian hui jia bi jiao wan
liang hui zai bei jing zhao kai
```

and the model file `model_0.7_0.6_0.3.npz` should exist in the root directory, and `pinyin_dict.json` should exist in `utils` directory. Then, you can get an output like:

```
清华大学计算机系
我上学去了
今天回家比较晚
两会在北京召开
```

Most of the programs in this repo can be run with specific parameters, such as `python pinyin.py -i input.txt -o output.txt -m model_0.7_0.6_0.3.npz`. The default parameters are defined in `utils/params.py`. Use command line argument `-h` to get help.

## Details

The main files are shown below.

```shell
.
├── LICENSE
├── README.md
├── checkpoints
├── input.txt
├── material
│   ├── chars.txt
│   ├── pinyin_dict.txt
│   ├── sina_news_gbk
│   └── val.txt
├── model_0.7_0.6_0.3.npz   # model file
├── output.txt
├── pinyin.py               # main program for pinyin to Chinese conversion
├── pinyin_eva.py           # Conversion program for evaluation purpose
├── processed_data          # preprocessed data
├── test                    # test dataset
│   ├── ans.txt
│   ├── input.txt
│   ├── output.txt
│   ├── report.txt
│   └── val_bak.txt
├── test_data
│   ├── gen_val.py          # generate input and ans for testing
│   ├── input.txt
│   ├── society
│   ├── test_ans.txt
│   └── test_data.txt
├── train.py                # training program, output model
└── utils
    ├── __init__.py
    ├── evaluate.py         # evaluate accuracy
    ├── merge.py            # merge statistics in different checkpoints (which may be computed in different processes
    ├── params.py           # define some parameters
    ├── pinyin_dict.json
    ├── pinyin_dict.py
    ├── preprocess.py       # preprocess the sina_news dataset
    ├── tools.py
    └── viterbi.py          # viterbi algorithm
```

The main process to complete the whole task is:

1. Prepare the corpus for training.
2. Use `utils/preprocess.py` to preprocess data.
3. Generate dictionary from pinyin to Chinese character by running `utils/pinyin_dict.py` with provided `material/pinyin_dict.txt`.
4. Train the model with `train.py` and preprocessed data in `processed_data`.
5. Run `pinyin.py` for conversion tasks.
6. Use `pinyin_eva.py` to find the best parameters ($\beta_0, \beta_1$) for better performance.

