import sys
#!/usr/bin/env python

for line in sys.stdin:
    label, title = line.strip().split('\t')
    print(f"{label}\t{title}")
