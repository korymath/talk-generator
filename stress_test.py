import tqdm
import time
import random
import subprocess
import numpy as np


# get some random words
word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()
num_tests = 2
num_slides = 2
parallel = 'True'
open_ppt = 'False'

times = []
for i in tqdm(range(num_tests)):
    start_time = time.time()
    topic_word = random.choice(WORDS)
    bashCommand = 'python run.py --parallel={} --num_slides={} --topic={} --open_ppt={}'.format(
        parallel, num_slides, topic_word, open_ppt)
    print(bashCommand)
    process = subprocess.Popen(bashCommand.split() , stdout=subprocess.PIPE)
    output, error = process.communicate()
    times.append(time.time() - start_time)

print('Made {} talks with an average of {} seconds, std: {}'.format(
    num_tests, np.mean(times), np.std(times)))