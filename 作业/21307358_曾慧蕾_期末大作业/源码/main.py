# 用于最终统计每个标签的正确率以及总正确率
test_path = "D:\\VSCode_code\\python\\file\\FBSxitong\\dataset\\true_test.txt"
predict_path = "D:\\VSCode_code\\python\\file\\FBSxitong\\test_result.txt"
sum_total = 0
sum_correct = 0

with open(test_path, "r", encoding="utf-8") as f:
    test_data = f.readlines()

labels = {}
for line in test_data:
    label, _ = line.strip().split('\t')
    labels[label] = {'total': 0, 'correct': 0}

with open(predict_path, "r", encoding="utf-8") as f:
    predict_data = f.readlines()

for line in predict_data: # <ID, <label, p>>
    test_id, predict_label = line.strip().split('\t')
    true_label, _ = test_data[int(test_id)-1].strip().split('\t')

    if true_label not in labels:
        labels[true_label] = {'total': 0, 'correct': 0}

    labels[true_label]['total'] += 1
    sum_total += 1
    if true_label == predict_label:
        labels[true_label]['correct'] += 1
        sum_correct += 1

for label, info in labels.items():
    total = info['total']
    correct = info['correct']
    accuracy = correct / total if total != 0 else 0
    print(f"{label}: Total: {total}, Correct: {correct}, Accuracy: {accuracy:.4f}")

print(f"ALL: Total:{sum_total}, Correct:{sum_correct}, Accuracy:{(sum_correct / sum_total):.4f}")