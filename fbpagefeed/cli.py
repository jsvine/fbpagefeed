#!/usr/bin/env python
import sys, os
import getpass
import json
import csv
import argparse
from . import feed

def get_input(key, secret=True):
    stream = getpass.getpass if secret else input
    return os.environ.get(key) or stream(key + ": ")

CSV_HEADERS = [
    "id",
    "type",
    "created_time",
    "message",
    "link",
    "shares",
    "comments",
    "reactions",
    "reactions_like",
    "reactions_love",
    "reactions_wow",
    "reactions_haha",
    "reactions_sad",
    "reactions_angry",
]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("account_id")
    parser.add_argument("--access-token", help="Facebook API access token. Alternatively, you can set the FB_ACCESS_TOKEN environment variable in your terminal.")
    parser.add_argument("--api-version", default=feed.DEFAULT_API_VERSION)
    parsed, unknown = parser.parse_known_args()
    for arg in unknown:
        if arg.startswith(("-", "--")):
            parser.add_argument(arg)
    args = parser.parse_args()
    return args

def write_csv(results):
    writer = csv.DictWriter(sys.stdout, fieldnames=CSV_HEADERS)
    writer.writeheader()
    for r in results:
        writer.writerow(r)

def main():
    args = vars(parse_args())
    account_id = args.pop("account_id")
    access_token = args.pop("access_token")
    if access_token is None:
        access_token = get_input("FB_ACCESS_TOKEN")
    results = feed.get(account_id, access_token, extra_params=args)
    write_csv(results)

if __name__ == "__main__":
    main()
