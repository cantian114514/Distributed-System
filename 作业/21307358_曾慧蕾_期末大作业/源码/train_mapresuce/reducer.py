import sys
#!/usr/bin/env python

label = None
word = None
# current_count = 0
# count = 0

label_record = {}
word_record = {}

for line in sys.stdin:
    label, value = line.strip().split('\t')
    value = value.split()
    if len(value) == 4:
        word = value[2]
        word_count = int(value[3])
        
        if label not in label_record:
            label_record.setdefault(label, 0)

        if word in word_record:
            word_record[word][0] += word_count
        else:
            value = [word_count, label]
            word_record.setdefault(word, value)

    else:
        label_count = int(value[0])
        if label in label_record:
            label_record[label] += label_count
        else:
            label_record.setdefault(label, label_count)

# word的数量应该远多于label，所以遍历word_record并输出
for key, value in word_record.items():
    label = value[1]
    word_count = value[0]
    word = key
    label_count = label_record[label]
    f1 = f"{label} {label_count} {word} {word_count}"
    res = f"{label}\t{f1}"
    
    print(res)