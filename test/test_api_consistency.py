import unittest
import fbpagefeed
from fbpagefeed.cli import get_input
import sys, os

access_token = get_input("FB_ACCESS_TOKEN")

class QualityTest(unittest.TestCase):
    def test_missing_healthranger_post(self):
        feed = fbpagefeed.get(
            account_id=35590531315,
            access_token=access_token,
            extra_params={
                "until": "2012-09-18T15:00:00+0000"
            },
            max_results=1
        )
        post = list(feed)[0]
        assert post["id"] == "35590531315_455891227789720"

    def test_reactions(self):
        feed = fbpagefeed.get(
            account_id=35590531315,
            access_token=access_token,
            extra_params={
                "until": "2017-01-01"
            },
            max_results=1
        )
        post = list(feed)[0]
        assert post["reactions"] > 0
        assert post["reactions"] == sum([
            post["reactions_like"],
            post["reactions_love"],
            post["reactions_wow"],
            post["reactions_haha"],
            post["reactions_sad"],
            post["reactions_angry"],
        ])

if __name__ == '__main__':
    unittest.main()
