import sys

for line in sys.stdin:
    if line.strip():
        sys.stdout.write(line)
