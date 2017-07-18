#!/usr/bin/env python
import fbiter
import requests
import sys
import time
import json
import itertools

DEFAULT_API_VERSION = "v2.9"
DEFAULT_MAX_RESULTS = None

def get(account_id, access_token,
    api_version=DEFAULT_API_VERSION,
    extra_params={},
    max_results=DEFAULT_MAX_RESULTS):

    path = "{}/{}/posts".format(api_version, account_id)

    if max_results is not None:
        limit = max_results
    elif extra_params.get("limit") is not None:
        limit = extra_params.get("limit")
    else:
        limit = 100

    params = {
        "access_token": access_token,
        "limit": limit,
        "fields": ",".join([
            "type",
            "created_time",
            "message",
            "link",
            "shares",
            "comments.limit(0).summary(true)",
            "reactions.limit(0).summary(true)",
            "reactions.type(LIKE).limit(0).summary(total_count).as(reactions_like)",
            "reactions.type(LOVE).limit(0).summary(total_count).as(reactions_love)",
            "reactions.type(WOW).limit(0).summary(total_count).as(reactions_wow)",
            "reactions.type(HAHA).limit(0).summary(total_count).as(reactions_haha)",
            "reactions.type(SAD).limit(0).summary(total_count).as(reactions_sad)",
            "reactions.type(ANGRY).limit(0).summary(total_count).as(reactions_angry)",
        ])
    }
    params.update(extra_params)
    endpoint = fbiter.Endpoint(path, params)
    results = endpoint.iter_results(max_results=max_results)

    for r in results:
        r["shares"] = r.get("shares", {}).get("count")
        r["comments"] = r.get("comments", {}).get("summary", {}).get("total_count")
        for key, value in r.items():
            if type(value) == dict:
                if "summary" in value:
                    if "total_count" in value["summary"]:
                        r[key] = value["summary"]["total_count"]
        yield r
