'''
Parameters
'''

#global
process_number      = 10

# preprocess
docs_dir            = './material/sina_news_gbk'
docs_keyword        = '2016'
processed_data      = './processed_data'

# pinyin_dict
pinyin_dict_txt     = './material/pinyin_dict.txt'
pinyin_dict_json    = './utils/pinyin_dict.json'

# trainingf
data_keyword        = docs_keyword
alphas              = [0.7, 0.6, 0.3]
model_path          = f'model_{alphas[0]}_{alphas[1]}_{alphas[2]}.npz'
checkpoints_path    = './checkpoints'

# usage
input_file          = 'input.txt'
output_file         = 'output.txt'
betas               = [0.8, 0.8]

# test accuracy
input_test_file     = './test/input.txt'
output_test_file    = './test/output.txt'
ans_file            = './test/ans.txt'
report_path         = './test/report.txt'
