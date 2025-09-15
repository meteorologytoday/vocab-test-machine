import numpy as np
import pandas as pd
from typing import Union

class VocabDatabase:

    def __init__(self, data_file, delimiter="|"):

        self.data_file = data_file
        self.database = pd.read_csv(data_file, delimiter=delimiter)

        numbering = pd.DataFrame( dict(numbering = np.arange(len(self.database)) ))
        self.database = self.database.join(numbering)


def drawExcept(
    full_N : int,
    draw_N : int,
    except_for : int,
):

    if draw_N > full_N - 1:
        raise Exception(f"draw_N ({draw_N}) must be less than full_N ({full_N:d})")

    numbering = np.arange(full_N)
    numbering = np.concatenate( (numbering[:except_for], numbering[except_for+1:]) )    
    np.random.shuffle(numbering)

    return numbering[:draw_N]
    


def askQuestion(
    pool,
    numbering : int,
    qtype,
    prefix = "",
):

    s = pool.iloc[numbering]
    
    if qtype == "def":

        other_ans = drawExcept(len(pool), 3, except_for = s['numbering'])

        true_ans_idx = int(np.floor(np.random.rand() * ( len(other_ans) + 1 ) )) 
        all_ans = np.concatenate( ( other_ans[:true_ans_idx] , [numbering,], other_ans[true_ans_idx:] ) ) 
        
        print(f"{prefix:s}What is \"{s['vocab']:s}\" ?")
        for i, k in enumerate(all_ans):
            _s = pool.iloc[k]
            print("(%s) %s" % (
                "abcdefghijklmn"[i],
                _s['definition'],
            ))

        print("True ans: %s" % ("abcdefghijklmn"[true_ans_idx],))
        
    else:
        raise Exception(f"Unknown qtype \"{qtype:s}\"")

    
    result = np.random.rand() > 0.5

    return result


def testMe(
    v : VocabDatabase,
    tests_per_batch  : int = 5,
    batches_per_test : int = 3,
    refresh_set_freq : int = 1,
    qtype = "def",
):

    print(f"There are {len(v.database):d} vocabs")
    print(f"- Tests per batch: {tests_per_batch:d}")
    print(f"- batches_per_test: {batches_per_test:d}")

    db = v.database
    sub_db = db
    for b in range(batches_per_test):
        N_vocab = len(v.database)
        print(f"# Batch {b+1:d}")

        shuffled_order = np.arange(N_vocab)
        np.random.shuffle(shuffled_order)
        shuffled_order = shuffled_order[:tests_per_batch]
        
        for i, _order in enumerate(shuffled_order):

            print(f"    ## Test {i+1:d}:")
            s = sub_db.iloc[_order]
            result = askQuestion(
                db,
                s.numbering,
                qtype = qtype,
                prefix = "    ",
            )

            if result is None:
                print("Unknown result: ", result)
            else:
                if result == True:
                    print("----> Congrats! You are correct!")
                else:
                    print("----> Oh-oh!")
        
        # check error record and decide what to do
        if b % refresh_set_freq == 0:

            
            

