#!/usr/bin/env python

import sys

from tokenizer import tokenize

from parser import parse

from evaluator import evaluate

def main():
    environment = {}
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Filename provided, read and execute it
        with open(sys.argv[1], 'r') as f:
            source_code = f.read()
        try:
            tokens = tokenize(source_code)
            ast = parse(tokens)
            evaluate(ast, environment)
        except Exception as e:
            print(f"Error: {e}")


    else:
        # REPL loop
        while True:
            try:
                # Read input
                source_code = input('>> ')

                # Exit condition for the REPL loop
                if source_code.strip() in ['exit', 'quit']:
                    break

                # Tokenize, parse, and execute the code
                tokens = tokenize(source_code)
                ast = parse(tokens)
                evaluate(ast, environment)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()

