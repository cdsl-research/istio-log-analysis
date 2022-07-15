import os
import csv
import json


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
            elif parsed_line["Path"].startswith("/fulltext/_search"):
                continue
            elif "minio-py" in parsed_line["UserAgent"]:
                continue

            reqid = parsed_line["ReqId"]
            reqid_lst = reqid_table.get(reqid, [])
            reqid_lst.append(parsed_line)
            reqid_table[reqid] = reqid_lst

    for reqid, lines in reqid_table.items():
        # ReqAuthorityに外部からのアクセスが含まれている場合
        candidates = ("34.84.68.226", "doktor.tak-cslab.org")
        match = list(filter(lambda x: x["ReqAuthority"] in candidates, lines))
        if match:
            endpoint_method = match[0]["Method"]
            endpoint_path = match[0]["Path"]
            # print(endpoint_method, endpoint_path)

            for line in lines:
                line["EndpointMethod"] = endpoint_method
                line["EndpointPath"] = endpoint_path
            # print(json.dumps(lines, indent=4))
            continue

        if len(lines) == 10:
            for line in lines:
                line["EndpointMethod"] = "GET"
                line["EndpointPath"] = "/"
            # print(json.dumps(lines, indent=4))
            continue

        # print(len(lines))
        # print(json.dumps(lines, indent=4))

    new_filename = filename.replace(".csv", "-ext.json")
    with open(new_filename, mode='w') as f:
        json.dump(reqid_table, f, indent=4)


if __name__ == "__main__":
    main()
