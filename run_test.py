import vocab
import argparse
import pandas as pd
import tools

def convertGoogleIdToCSVLink(
    id : str,
    gid : str = "0",
):

    return f"https://docs.google.com/spreadsheets/d/{id:s}/export?format=csv&gid={gid:s}"


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file in csv format. You can specify delimiter with `--delimiter` option. ", default="vocab_list.csv")
    parser.add_argument("--delimiter", type=str, help="Delimiter for csv file. ", default="|")
    parser.add_argument("--test-type", type=str, help="Type of test you want to take.", default="def", choices=["def",])
    parser.add_argument("--file-opener", action="store_true", help="If set, then ignore `--input`, and open a GUI file selector for input file. ")
    parser.add_argument("--google-spreadsheet", type=str, help="The hash id for google spreadsheet (https://docs.google.com/spreadsheets/d/[hash_id]/...). If set, then ignore `--file-opener` and `--input`. Also `--delimiter` will be set to ','.", default=None)
    parser.add_argument("--google-spreadsheet-gid", type=str, help="The sheet gid.", default="0")
    parser.add_argument("--subset-name", type=str, help="The subset name. For example, you have a column named 'week', and you want to test only week 3. In this case, set `--subset-name=week` and `--subset-value=3`. You might also want to speficy the type in `--subset-type`.", default=None)
    parser.add_argument("--subset-value", type=str, help="The subset value.", default=None)
    parser.add_argument("--subset-type", type=str, help="The subset type.", default="str")
    
    parser.add_argument("--batches", type=int, help="How many batches in this test", default=3)
    parser.add_argument("--questions-per-batch", type=int, help="Questions per batch", default=5)


    args = parser.parse_args()
    print(args)


    if args.google_spreadsheet is not None:
        import requests
        from io import StringIO

        google_link = convertGoogleIdToCSVLink(id=args.google_spreadsheet, gid=args.google_spreadsheet_gid)
        response = requests.get(google_link)
        response.encoding = "utf-8"
        response.raise_for_status()  # make sure the request succeeded
        input_file = StringIO(response.text)
        args.delimiter = ","

    elif args.file_opener:
        import tkinter as tk
        from tkinter import filedialog
        tk_root = tk.Tk()
        tk_root.withdraw()
        input_file = filedialog.askopenfilename()
    else:
        input_file = args.input

    if args.google_spreadsheet is not None:
        print(f"# Load google spreadsheet hash id: {args.google_spreadsheet:s}")
        print(f"       google link: {google_link:s}")
    else:
        print(f"# Input file: {input_file:s}")
    
    print(f"# Delimiter : {args.delimiter:s}")
    print(f"# Test type : {args.test_type:s}")

    df = pd.read_csv(input_file, delimiter=args.delimiter)

    if args.subset_name is not None:
        import builtins
        
        subset_type = getattr(builtins, args.subset_type)
        subset_value = subset_type(args.subset_value)
        print(f"## Subset name: {args.subset_name:s}")
        print(f"## Subset type: {args.subset_type:s}")
        print(f"## Subset value: {args.subset_value:s}")

        df = df[df[args.subset_name] == subset_value]
    
    
    print(f"## Number of vocab: {len(df):d}")
   
    v = vocab.VocabDatabase(database=df)

    print()
    tools.block("Get ready!") 
    vocab.testMe(
        v,
        qtype = args.test_type,
        batches = args.batches,
        questions_per_batch = args.questions_per_batch,    
    )
