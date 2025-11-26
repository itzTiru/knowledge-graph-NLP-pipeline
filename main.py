import argparse
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Knowledge Graph Extraction System")
    parser.add_argument("--input", type=str, help="Path to input document")
    args = parser.parse_args()

    if args.input:
        print(f"Processing {args.input}...")
    else:
        print("Please provide an input file using --input")

if __name__ == "__main__":
    main()
