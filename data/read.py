import ast
import os

with open('contents.jsonl', 'r') as f:
    data = f.readlines()

    for l in data:
        print(ast.literal_eval(l))
        input()
        os.system('clear')
