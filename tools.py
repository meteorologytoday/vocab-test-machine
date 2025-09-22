
from prettytable import PrettyTable
import os

def block(msg=None):

    if msg is not None:
        print(msg)

    print()
    input("<Press any key to continue>")


def clearWindow():
    os.system("clear")


def convertDataFrameToPrettyTable(df):
    
    table = PrettyTable()

    for col in df.columns:
        table.add_column(col, df[col].tolist())

    return table

