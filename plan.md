## 训练

单个字出现的概率（次数）

语料库中相邻二字同时出现的概率

平滑处理

任意两个字之间有向边的权值

## 计算

建立图

动态规划求最短路

import numpy as np

model = np.load('model.npy', allow_pickle=True).item()

准备数据 material 下的文件夹里
python utils/preprocess.py
生成到processed_data里

准备拼音到汉字关系的 './material/pinyin_dict.txt'
python utils/pinyin_dict.py
生成拼音到汉字的字典 './utils/pinyin_dict.json'

python train.py

python pinyin.py

python utils/evaluate.py

