import csv
import re
import os
from datetime import datetime as dt


def round_datetime(datetime_text: str) -> str:
    my_dt = dt.strptime(datetime_text, "%Y-%m-%dT%H:%M:%S.%fZ")
    my_dt_round = my_dt.replace(minute=my_dt.minute - (my_dt.minute % 30),
                                second=0, microsecond=0)
    return my_dt_round.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def parser(raw_text: str):
    match_pattern = (
        # '[2022-05-12T00:57:09.548Z]'
        r"\[(?P<DateTime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)]"
        r' "(?P<Method>\w+)'  # 'GET'
        r" (?P<Path>[^ ]+)"  # '/author'
        r' (?P<Protocol>[^ ]+)"'  # 'HTTP/1.1'
        r" (?P<Status>\d{,3})"  # '200'
        r' (?P<_Details>[^ ]+ [^ ]+ [^ ]+ "-")'  # '- via_upstream - "-"'
        r" (?P<_Sizes>[-\d]+ [-\d]+ [-\d]+ [-\d]+)"  # '0 11462 7 7'
        r' "(?P<XForwardFor>[\.,\-\w]+)"'  # "192.168.200.1,10.42.0.0"
        r' "(?P<UserAgent>[^"]+)"'  # "Python/3.9 aiohttp/3.8.1"
        r' "(?P<ReqId>[\-\w]+)"'  # '"ef217580-7229-9d84-b9b2-8d7bd3dfcca4"'
        r' "(?P<ReqAuthority>[\-\:\.\w]+)"'  # '"paper-app.paper:4000"'
        r' "(?P<UpstreamHost>[\-\:\.\d]+)"'  # '"10.42.3.158:8000"'
        # 'outbound|4000||paper-app.paper.svc.cluster.local'
        r" (?P<UpstreamCluster>\w+\|\d+\|\w*\|[\-\.\w]*)"
        r" (?P<UpstreamLocalAddr>[\-\:\.\w]+)"  # '10.42.3.121:58312'
        r" (?P<DownstreamLocalAddr>[\:\.\w-]+)"  # '10.43.148.153:9200'
        r" (?P<DownstreamRemoteAddr>[\:\.\w-]+)"  # '10.42.3.163:47890'
        # 'outbound_.8000_._.httpbin.foo.svc.cluster.local'
        r" (?P<ReqServerName>[^ ]+)"
        r" (?P<RouteName>[^ ]+)"  # 'default'
        # r' "(?P<EndpointMethod>\w+)'
        # r' (?P<EndpointPath>[^ ]+)"'
        # r" (?P<ServiceTracing>([_\w\d\-]+\(\d+\)\|)+)"
    )
    matched = re.match(match_pattern, raw_text)
    if matched is None:
        return None
    return matched.groupdict()


def main():
    # filename = "find-istio-proxy-anomaly.csv"
    # filename = "find-istio-proxy-normal.csv"
    filename = os.getenv("FILE", "v1-logs/find-istio-proxy-anomaly.csv")
    print("open file=", filename)

    log_table = {}
    log_example = {}
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

            # exclude inbound log
            if parsed_line["UpstreamCluster"].startswith("inbound"):
                continue
            elif parsed_line["Path"].startswith("/.kibana") or \
                    parsed_line["Path"].startswith("/_") or \
                    parsed_line["Path"].startswith("/."):
                continue

            # round datetime
            parsed_line["DateTime"] = round_datetime(parsed_line["DateTime"])

            _key = (
                parsed_line['DateTime'],
                parsed_line["Method"],
                parsed_line["Status"],
                parsed_line["Path"],
                parsed_line["ReqAuthority"],
            )
            log_table[_key] = log_table.get(_key, 0) + 1
            log_example[_key] = log_body

            # import json
            # print(log_body)
            # print(json.dumps(parsed_line, indent=2))
            # return

    log_table = sorted(log_table.items(), key=lambda x: x[1], reverse=True)
    # log_table = list(filter(lambda x: x[1] > 1000, log_table))
    for l in log_table:
        _key = l[0]
        _val = l[1]
        _log = log_example[_key]
        print(_val, "\t", "\t".join(_key))
        # print(_log)

# log_table = list(
#     filter(lambda x: x[0][3] == "fulltext-elastic.fulltext:9200" and x[0][1] == "/fulltext/_search", log_table))

    # import json
    # print(json.dumps(log_table, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
