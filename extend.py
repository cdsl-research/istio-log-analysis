import os
import csv

from parser import parser

from yaml import parse


def main():
    filename = os.getenv("FILE", "v2-logs/30min.csv")
    reqid_table = {}

    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, skipinitialspace=True)
        next(spamreader)  # skip header
        for row in spamreader:
            try:
                log_body = row[2]
            except Exception as e:
                print(e)
                continue

            parsed_line = parser(log_body)
            if parsed_line is None:
                continue
            elif parsed_line["UpstreamCluster"].startswith("inbound"):
                continue
            elif parsed_line["Path"].startswith("/fulltext/_search"):
                continue

            # parsed_line["EndpointMethod"] = "GET"
            # parsed_line["EndpointPath"] = "/"

            reqid = parsed_line["ReqId"]
            reqid_lst = reqid_table.get(reqid, [])
            reqid_lst.append(parsed_line)
            reqid_table[reqid] = reqid_lst

    import json
    print(json.dumps(reqid_table, indent=4))


if __name__ == "__main__":
    main()
