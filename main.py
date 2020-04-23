import os
import argparse
import csv
import random
import shutil
import itertools
from tabulate import tabulate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split trenitalia dataset and prepare it for training')
    parser.add_argument("-i", "--input_files", required=True, type=str, nargs="+",
                        help="Input file")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Output file")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force overwrite of output folder")
    parser.add_argument("-r", "--ratio", required=False, type=float, default=1.0,
                        help="Ration between positive and negative couples")
    parser.add_argument("--keep_inverted", action="store_true",
                        help="Use also tuples inverted: [a, b] -> [b, a]")

    args = parser.parse_args()

    # parse input arguments
    input_files = args.input_files
    output_file = args.output_file
    force = args.force
    ratio = args.ratio
    keep_inverted = args.keep_inverted
    random.seed(999)

    # checks...
    assert all([os.path.isfile(input_file) for input_file in input_files]), f"One of {input_files} does not exists"

    # create output folder if it does not exists
    if os.path.exists(output_file):
        assert force, f"file {output_file} does already exists, use -f to force overwrite"
        os.remove(output_file)

    # open the input csv
    clusters = []
    for input_file in input_files:
        with open(input_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                row = [x.strip() for x in row]
                clusters.append(row)

    positives = []
    for cluster in clusters:
        # with only 1 question we cannot create neither a single positive tuple
        if len(cluster) > 1:
            for i, q1 in enumerate(cluster[:-1]):
                for j, q2 in enumerate(cluster[i + 1:]):
                    positives.append([q1, q2, True])
                    if keep_inverted:
                        positives.append([q2, q1, True])
    
    all_negatives = []
    for i, cluster1 in enumerate(clusters[:-1]):
        for j, cluster2 in enumerate(clusters[i + 1:]):
            for q1 in cluster1:
                for q2 in cluster2:
                    all_negatives.append([q1, q2, False])
                    if keep_inverted:
                        all_negatives.append([q2, q1, False])

    # shuffle 
    negatives_number = int(len(positives) * ratio)

    random.shuffle(all_negatives)
    negatives = all_negatives[:negatives_number]

    all_data = positives + negatives

    # shuffle again in case they will be used for training...
    random.shuffle(all_data)

    with open(output_file, mode='w') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for a in all_data:
            writer.writerow(a)

    print("Done!")
    