import numpy as np
import pandas as pd
import time
from typing import Union

import tools

class VocabDatabase:

    def __init__(self, database):

        self.database = database
        self.database["error_count"] = 0
        self.database["asked"] = 0
        
        if len(database) == 0:
            raise Exception(f"Error: Database is empty.")
            
            
        for _index in [
            "vocab",
            "definition",
        ]:
            if _index not in database.columns:
                raise Exception(f"Database needs to have column `{_index:s}`.")


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
            user_ans = input("Your answer (type exit to end test): ")
            try:

                if user_ans.strip() == "":
                    continue
                elif user_ans.upper() == "EXIT":
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
    
    df_err = df[df["error_count"] > 0][ ["vocab", "definition", "error_count"] ]
    df_err = df_err.sort_values(by=["error_count", "vocab"], ascending=False)
    
    df_notasked = (df[df["asked"] == 0][ ["vocab", "definition"] ]).sort_values(by=["vocab"])
    

    if len(df_err) > 0:
        
        print("# Here are your errors: ")
        print(str(tools.convertDataFrameToPrettyTable(df_err)))

    else:

        print("Congrats! You have no errors! ") 

    if len(df_notasked) > 0:
       
        print() 
        print() 
        print("# Here are vocabs that have not been tested: ")
        print(str(tools.convertDataFrameToPrettyTable(df_notasked)))


def testMe(
    v : VocabDatabase,
    questions_per_batch  : int = 5,
    batches : int = 3,
    refresh_set_freq : int = 1,
    qtype = "def",
    pause: float = 1.0,
):

    print(f"There are {len(v.database):d} vocabs")
    print(f"- Batches: {batches:d}")
    print(f"- Questions per batch: {questions_per_batch:d}")

    db = v.database
    sub_db = db



    end_flag = False
    for b in range(batches):
            
        tools.clearWindow()
        print(f"# Here comes batch {b+1:d} !")
        time.sleep(2.0)

        N_vocab = len(v.database)

        for i in range(questions_per_batch):
            
            tools.clearWindow()

            print(f"# Batch {b+1:d}:")
            print(f"# Test  {i+1:d} / {questions_per_batch:d}:")
            s = sub_db.sample()
            result = askQuestion(
                db,
                s.index[0],
                qtype = qtype,
                prefix = "",
            )
                    
            sub_db.loc[s.index[0], "asked"] += 1

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
                        print(str(tools.convertDataFrameToPrettyTable(s)))
                        tools.block()

 
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
            
            

