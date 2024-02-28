# 对原始数据进行除杂操作，并分好训练集与测试集
'''
根据最初爬取的数据, 经分析后决定选取前十的标签
每个标签取200个
'''
import random
import re

def clean_text(text):
    cleaned_text = re.sub('[^a-zA-Z\s]', ' ', text)
    cleaned_text = cleaned_text.lower()
    return cleaned_text

with open('D:\\VSCode_code\\python\\file\\FBSxitong\\dataset\\original_data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

data = []
labels = []
for i in range(0, 10): # 取十个标签
    for j in range(0,200):
        label, title = lines[i * 200 + j].strip().split('\t')
        title = clean_text(title)
        if label not in labels:
            labels.append(label)
        data.append(f"{label}\t{title}") # 数据清洗

random.shuffle(data) # 随机打乱数据顺序

train_size = int(0.8 * len(data))
test_size = len(data) - train_size
train_data = sorted(data[:train_size])
test_data = sorted(data[train_size:])

with open('D:\\VSCode_code\\python\\file\\FBSxitong\\dataset\\train.txt', 'w', encoding='utf-8') as f: # 训练
    for line in train_data:
        f.writelines(line)
        f.writelines('\n')
print("训练集写入完毕！")

with open('D:\\VSCode_code\\python\\file\\FBSxitong\\dataset\\true_test.txt', 'w', encoding='utf-8') as f: # 核对用的测试文件
    for line in test_data:
        f.writelines(line)
        f.writelines('\n')
print("测试集(处理前)写入完毕！")

with open('D:\\VSCode_code\\python\\file\\FBSxitong\\dataset\\use_test.txt', 'w', encoding='utf-8') as f: # 预测用的测试文件
    for i, line in enumerate(test_data, start=1): # <label, <"Test", ID, title>>
        _, title = line.strip().split('\t')
        tail = f"{i} {title}"
        for label in labels:
            test_line = f"{label}\t{tail}"
            f.write(test_line)
            f.writelines('\n')
print("测试集(处理后)写入完毕！")