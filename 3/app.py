import os
from typing import List, Dict
print("Enter a path to directory with subject lists:")
directory = input()

unpassed_subjects: Dict[str, List[str]] = dict()

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        # print(filename)
        file = open(directory + "/" + filename)
        filename = filename[:len(filename)-4]

        for position, line in enumerate(file):
            parts = line.split()
            if len(parts) != 2:
                raise Exception(
                    "Subject list must contain only 2 values(name and subject mark) at {} line".format(position)
                )
            name = str(parts[0])
            try:
                mark = int(parts[1])
            except ValueError:
                raise Exception("Second value in line must be valid integer, error at {} line".format(position))
            if mark >= 50:
                continue

            if name not in unpassed_subjects:
                unpassed_subjects[name] = [filename]
            else:
                unpassed_subjects[name].append(filename)

print("!!!SHAME ON YOU!!!")
for name, subjects in unpassed_subjects.items():
    print(name, subjects)
