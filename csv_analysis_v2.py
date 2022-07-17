import csv
import os
import json
from datetime import datetime as dt

from typing import Dict


def round_datetime(datetime_text: str) -> str:
    my_dt = dt.strptime(datetime_text, "%Y-%m-%dT%H:%M:%S.%fZ")
    my_dt_round = my_dt.replace(minute=my_dt.minute - (my_dt.minute % 30),
                                second=0, microsecond=0)
    return my_dt_round.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def main():
    filename = os.getenv("FILE", "v2-logs/30min-ext.csv")
    print("open file=", filename)

    log_table: Dict[str, int] = {}  # 特徴ごとにログ件数を集計する
    log_example: Dict[str, str] = {}  # 集計したログの代表ログを記録する
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            # round datetime
            row["DateTime"] = round_datetime(row["DateTime"])

            _key = (
                row["DateTime"],
                row["EndpointMethod"],
                row["EndpointPath"],
                row["ServiceTracing"],
            )
            log_table[_key] = log_table.get(_key, 0) + 1
            log_example[_key] = json.dumps(row)

    # 結果を件数が多い順に並べ替え
    log_table = sorted(log_table.items(), key=lambda x: x[1], reverse=True)

    # 1000件以上のログに絞り込み
    # log_table = list(filter(lambda x: x[1] > 1000, log_table))

    for l in log_table:
        _key = l[0]
        _val = l[1]
        _log = log_example[_key]
        print(_val, "\t", "\t".join(_key))

    # Debug出力
    # print(json.dumps(log_table, sort_keys=True, indent=4))


if __name__ == "__main__":
    main()
