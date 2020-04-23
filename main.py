import os
import argparse
import csv
import random

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
    parser.add_argument("-n", "--n_negative", required=True, type=int,
                        help="Number of negative for each positive")

    args = parser.parse_args()

    # parse input arguments
    input_files = args.input_files
    output_file = args.output_file
    force = args.force
    ratio = args.ratio
    n_negative = args.n_negative
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
                row = [x.strip() for x in row if x.strip()]
                clusters.append(row)

    all_data = []
    _id = 0
    choices = list(range(len(clusters)))
    for c, cluster in enumerate(clusters):
        # with only 1 question we cannot create neither a single positive tuple
        if len(cluster) > 1:
            for i, q1 in enumerate(cluster):
                for j, q2 in enumerate(cluster):
                    if i != j:
                        all_data.append([_id, q1, q2, True])
                        for i in range(n_negative):
                            choices.remove(c)
                            res = random.choice(choices)
                            choices.append(c)
                            elem = random.choice(clusters[res])
                            all_data.append([_id, q1, elem, False])
                        _id += 1


    with open(output_file, mode='w') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for a in all_data:
            writer.writerow(a)

    print("Done!")
    