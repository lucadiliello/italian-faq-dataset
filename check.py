import os
import argparse
import csv
import random
import shutil
import itertools
from tabulate import tabulate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check if there are sentences in common between the provided files')
    parser.add_argument("-i", "--input_files", required=True, type=str, nargs="+",
                        help="Input files to be checked")

    args = parser.parse_args()

    # parse input arguments
    input_files = args.input_files

    # checks...
    assert all([os.path.isfile(input_file) for input_file in input_files]), f"One of {input_files} does not exists"

    # open the input csv
    def open_file(file_name):
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            return list(csv_reader)

    data = {}
    for input_file in input_files:
        data[input_file] = open_file(input_file)

    # return sentences in common between two lists of sentence pairs
    def compare(data1, data2):
        res1 = set()
        for a, b, _ in data1:
            res1.add(a.strip())
            res1.add(b.strip())

        res2 = set()
        for a, b, _ in data2:
            res2.add(a.strip())
            res2.add(b.strip())

        return res1.intersection(res2)

    keys = list(data.keys())

    for i in range(len(keys) - 1):
        for j in range(i + 1, len(keys)):
            value1 = data[keys[i]]
            value2 = data[keys[j]]

            common = compare(value1, value2)
            print(f"Between {keys[i]} and {keys[j]} there are {len(common)} sentences in common...")
            if len(common):
                for a in common:
                    print(f"\t\t{a}")


    print("Done!")