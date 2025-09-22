import numpy as np
import pandas as pd
import time
import os
from typing import Union
from prettytable import PrettyTable

class VocabDatabase:

    def __init__(self, database):

        self.database = database
        #print("Length of database: ", len(self.database))
        #numbering = pd.DataFrame( dict(numbering = np.arange(len(self.database)) ))
        #self.database = self.database.join(numbering)

        print(self.database)


def convertDataFrameToPrettyTable(df):
    
    table = PrettyTable()

    for col in df.columns:
        table.add_column(col, df[col].tolist())

    return table

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
    
def cleanText(s):
    s = s.strip()
    return s

def askQuestion(
    pool,
    index : int,
    qtype,
    prefix = "",
):

   


 
    s = pool.loc[index]
    result = None
    
    if qtype == "def":

        other_ans = pool[pool.index != index].sample(n=3)        
        all_ans = pd.concat([other_ans, s.to_frame().T])
        all_ans = all_ans.sample(frac=1)

        #print("True answer: ", s)
        print(f"{prefix:s}What is \"{s['vocab']:s}\" ?")

        true_ans_option = None
        for i in range(len(all_ans)):
            
            _s = all_ans.iloc[i]
            _s_index = all_ans.index[i]
            
            print("(%d) %s" % (
                i+1,
                _s['definition'],
            ))

            if _s_index == index:
                true_ans_option = i+1

        
        while result is None:
            user_ans = input("Your answer: ")
            try:

                if user_ans.upper() == "EXIT":
                    result = "EXIT"
                else:
                    user_ans = int(user_ans)
                    result = user_ans == true_ans_option
            
            except Exception as e:
                print(e)
                print("Only integer numbers are allowed")


        



 
    else:
        raise Exception(f"Unknown qtype \"{qtype:s}\"")

    if result is None:
        raise Exception(f"Result is None. Please check.")
    
    return result


def printStatistic(df):
    
    df = df[df["error_count"] > 0][ ["vocab", "definition", "error_count"] ]
    df = df.sort_values(by=["error_count", "vocab"], ascending=False)

    if len(df) > 0:
        
        print("Here are your errors: ")
        print(str(convertDataFrameToPrettyTable(df)))

    else:

        print("Congrats! You have no errors! ") 

def testMe(
    v : VocabDatabase,
    tests_per_batch  : int = 5,
    batches_per_test : int = 3,
    refresh_set_freq : int = 1,
    qtype = "def",
    pause: float = 1.0,
):

    print(f"There are {len(v.database):d} vocabs")
    print(f"- Tests per batch: {tests_per_batch:d}")
    print(f"- batches_per_test: {batches_per_test:d}")

    db = v.database
    sub_db = db
    sub_db = sub_db.assign(error_count=0)


    end_flag = False
    for b in range(batches_per_test):
        N_vocab = len(v.database)
        print(f"# Batch {b+1:d}")

        for i in range(N_vocab):
            
            os.system("clear")
                
            print(f"## Test {i+1:d}:")
            s = sub_db.sample()
            result = askQuestion(
                db,
                s.index[0],
                qtype = qtype,
                prefix = "",
            )

            if result is None:

                print("Unknown result: ", result)

            else:

                if result == True:
                    print()
                    print("----> Congrats! You are correct! :)")
                    print()
                    time.sleep(pause)

                elif result == False:
                    print()
                    print("----> Oh no :( ")
                    print()
                   
                    if qtype == "def":
                        
                        time.sleep(pause)
                    
                        print("Let us see the definition: ")
                        print(str(convertDataFrameToPrettyTable(s)))
                        input("<Press anything to continue>")

 
                    sub_db.loc[s.index[0], "error_count"] += 1
                
                elif result == "EXIT":

                    end_flag = True
                    print("EXIT the test.")                    
            
            if end_flag:
                break
    

        
        if end_flag:
            break
        # check error record and decide what to do
        #if b % refresh_set_freq == 0:

    printStatistic(sub_db)    
            
            

