import numpy as np
from numpy.linalg import norm
from datetime import datetime
import pandas as pd
import subprocess
import sys
import os

cos_sim = lambda a,b : np.dot(a, b)/(norm(a)*norm(b))
cos_dist = lambda a,b : 1 - cos_sim(a,b)

def generate_embedding(time_frame=None,**arg_dict):
    output = "./trained_embeddings/vecs_{p1}_{p2}.txt".format(**arg_dict)
    if time_frame:
        subprocess.run("mkdir -p trained_embeddings/temporal/{}".format(time_frame), shell=True)
        output = "./trained_embeddings/temporal/{}/{}_vecs_{p1}_{p2}.txt".format(time_frame,time_frame,**arg_dict)
    command = "./word2vecf/word2vecfadapted -output {} -train {file_data} -wvocab {file_wv} -cvocab {file_cv} -threads 100 -alpha {alpha} -size {size} -{param1} {p1} -{param2} {p2}".format(output,**arg_dict)
    if not os.path.exists(output):
        print("\t * Starting {}".format(output))
        subprocess.run(command, shell=True)
    return output

def load_embedding(filepath,split=True, **kwargs):
    embedding = pd.read_csv(filepath, sep=' ', header=None, skiprows=1, **kwargs)
    embedding.set_index(0)
    embedding = embedding.rename(columns={0: 'subreddit'})
    subreddits, vectors = embedding.iloc[:, 0], embedding.iloc[:, 1:151]
    vectors = vectors.divide(np.linalg.norm(vectors, axis=1), axis=0)
    if split:
        return subreddits, vectors
    embedding = pd.concat([subreddits, vectors], axis=1).set_index("subreddit")
    return embedding

def parse_tup(tup):
    to_tup = tup.strip('()').split(',')
    to_tup[1] = datetime.strptime(to_tup[1], "%Y-%m-%d")
    return to_tup