import os
import sys

if len(sys.argv) != 2:
    print("Usage: python3 create_directories.py <state-name>")
state = sys.argv[1]

folders = ['ceron', 'ceron/results', 'oconnor', 'oconnor/results', 'raw_tweets', 'tumasjan', 'tumasjan/results']
state_path = os.path.join('data', state)

try:
    os.mkdir(state_path)
    for folder in folders:
        os.mkdir(os.path.join(state_path, folder))
except OSError:
    print("Creation of the directories failed.")
else:
    print("Successfully created the directories!")
