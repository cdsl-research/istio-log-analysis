import argparse
import csv
import pathlib


def csv_split(filename: str):
    log_messages = set()
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, skipinitialspace=True)
        next(spamreader)  # skip header
        for row in spamreader:
            try:
                log_body = row[2]
            except Exception as e:
                print(e)
                continue
            log_messages.add(log_body)

    with open(filename + ".out", mode="w") as f:
        f.writelines(log_messages)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=pathlib.Path, dest="filepath")
    args = parser.parse_args()
    csv_split(args.filepath)
