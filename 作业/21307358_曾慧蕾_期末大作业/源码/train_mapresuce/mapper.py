import sys
#!/usr/bin/env python
for line in sys.stdin:
    # 去除首尾空格并分割单词
    label, title = line.strip().split('\t')
    title = title.split()

    # 对每个单词生成键值对
    for word in title:
        label_ = f"{label}"
        word_ = f"{word} 1"
        tail = f"{label_} {word_}"
        print(f"{label}\t{tail}")
    print(f"{label}\t1")