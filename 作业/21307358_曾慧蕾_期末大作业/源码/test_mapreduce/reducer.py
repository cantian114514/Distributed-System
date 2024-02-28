import sys
import math
#!/usr/bin/env python

def get_p(test_title, label, labels, total, k=1): # k是平滑系数
    label_prob = labels[label]['total'] / total # 计算P(label)

    # 分割test_title，计算每个词出现的概率
    words = test_title[:]
    word_probs = [((labels[label].get(word, 0) + k) / (labels[label]['total'] + k * len(labels[label]))) for word in words]

    p_test_label = math.prod(word_probs)  # 计算P(test_title | label)
    p_label_test = p_test_label * label_prob  # 计算P(label | test_title) = P(test_title | label) * P(label)

    return p_label_test

labels = {}
test_id = ""
test_title = ""
probabilities = []
total = 0

# 先训练
for line in sys.stdin:
    label, value = line.strip().split("\t")
    value = value.split()
    if value[0] == "module:": # 训练数据
        _, label, label_count, word, word_count = value[0], value[1], value[2], value[3], value[4]
        label_count = int(label_count)
        word_count = int(word_count)
        if label not in labels:
            labels[label] = {'total': 0}

        labels[label]['total'] = label_count # label出现次数
        total += label_count
        labels[label][word] = labels[label].get(word, 0) + word_count # label下word出现次数
    else:
        continue

# 后测试
for line in sys.stdin:
    label, value = line.strip().split("\t")
    value = value.split()
    if value[0] != "module:":  # 测试数据
        test_id = value[0]
        test_title = value[1:]
        # 计算test_title属于当前label的概率
        p = get_p(test_title, label[8:], labels, total)
        probabilities.append((test_id, label, p))
    else:
        continue

pro_set = {}
for prob in probabilities:
    id, label, p = int(prob[0]), prob[1], prob[2]
    if id not in pro_set:
        pro_set[id] = []
    pro_set[id].append((label, p))
    pro_set[id] = sorted(pro_set[id], key=lambda x:x[1], reverse=True) # 把概率最高的标签摆在最前面

for id, value in pro_set.items():
    output = f"{test_id}\t{value[0][0]}"
    print(output)