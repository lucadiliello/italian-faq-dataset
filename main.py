import os
import argparse
import csv
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split itafaq dataset and prepare it for training')
    parser.add_argument("-i", "--input_files", required=True, type=str, nargs="+",
                        help="Input file")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Output file")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force overwrite of output folder")
    parser.add_argument("-k", "--samples_per_query", type=int, required=False, default=10,
                        help="The number of negatives that should be generated for each query")
    parser.add_argument("--seed", type=int, required=False, default=999,
                        help="Seed for random shuffling")

    args = parser.parse_args()

    # parse input arguments
    input_files = args.input_files
    output_file = args.output_file
    force = args.force
    samples_per_query = args.samples_per_query
    random.seed(args.seed)

    # checks...
    assert all([os.path.isfile(input_file) for input_file in input_files]), f"One of {input_files} does not exists"

    # create output folder if it does not exists
    if os.path.exists(output_file):
        assert force, f"file {output_file} does already exists, use -f to force overwrite"
        os.remove(output_file)

    # open the input csv
    topics = []
    for input_file in input_files:
        topic = []
        with open(input_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                row = [x.strip() for x in row if x.strip()]
                topic.append(row)
            assert len(topic) >= 10
        topics.append(topic)

    all_data = []
    # give a different id to each question on the left
    _id = 0
    """
    For each file
        For each cluster in a file
            Compare all the question apart from the first with all the first of 
            all the other clusters limited to samples_per_query
    """
    for topic in topics:
        for i, cluster in enumerate(topic):
            for retrival_question in cluster[1:]:
                negatives = random.sample(
                    [cluster_2[0] for j, cluster_2 in enumerate(topic) if j != i],
                    k=samples_per_query - 1
                )
                positive = cluster[0]

                # add pos
                all_data.append([_id, retrival_question, positive, True])
                # add negs
                for negative in negatives:
                    all_data.append([_id, retrival_question, negative, False])
                _id += 1

    # Write results to file
    with open(output_file, mode='w') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for a in all_data:
            writer.writerow(a)

    print("Done!")
    