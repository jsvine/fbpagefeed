[![Version](https://img.shields.io/pypi/v/fbpagefeed.svg)](https://pypi.python.org/pypi/fbpagefeed) [![License](https://img.shields.io/pypi/l/fbpagefeed.svg)](https://pypi.python.org/pypi/fbpagefeed)

# fbpagefeed

A simple library/CLI for getting all posts from a given Facebook Page.

## Installation

```sh
pip install fbpagefeed
```

## Usage

### Command-line usage

Installing `fbpagefeed` gives you the `fbpagefeed` command-line tool. Use it like so:

```sh
fbpagefeed {facebook-page-id} [--my-param x] [--my-other-param y] > my-output.csv
```

... where the keyword params correspond to the optional parameters in Facebook's Graph API. (See "Default params" below.) For example:

```sh
fbpagefeed 91414372270 --since 2017-03-01 --until 2017-03-02 > my-output.csv
```

You can also use the page's spelled-out ID:

```sh
fbpagefeed BuzzFeedNews --since 2017-03-01 --until 2017-03-02 > my-output.csv
```

You can supply your FB access token one of three ways:

- Passing it to the `--access_token` flag
- Setting it as the `FB_ACCESS_TOKEN` environment variable
- Waiting for `fbpagefeed` to prompt you to enter it


### Library usage

Example:

```python
import fbpagefeed
import os

feed = fbpagefeed.get(
    "BuzzFeedNews",
    os.environ["FB_ACCESS_TOKEN"],
    extra_params={
        "since": "2017-05-01",
        "until": "2017-05-02"
    }
)

for post in feed:
    print(post)
```

### Default params

By default, `fbpagefeed` passes these parameters to the Facebook API:

```python
{
    "limit": 100,
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
```
