# reddit-to-instagram

A Python bot that scrapes media from a rotating set of Reddit subreddits and
auto-posts it to an Instagram account as photos, reels, videos, and stories. It
watermarks images, attaches randomized hashtags, and sleeps for a random number
of hours between runs.

> ⚠️ Educational / hobby project. Automating posting may violate Reddit's and
> Instagram's Terms of Service and content licensing. Use responsibly and only
> with content you have the right to repost.

## How it works

1. Picks a random subreddit and pulls a random post via [PRAW](https://praw.readthedocs.io/).
2. Downloads the media (images directly, videos via `yt-dlp`).
3. For images, overlays a watermark using Pillow.
4. Logs into Instagram via [instagrapi](https://github.com/subzeroid/instagrapi)
   and uploads as a photo / reel / video / IGTV, and optionally a story.
5. Logs out and sleeps before the next cycle.

## Requirements

- Python 3.10
- `ffmpeg` available on your `PATH`
- The packages in [`requirements.txt`](./requirements.txt)

```bash
pip install -r requirements.txt
```

## Configuration

All credentials are read from environment variables. Copy the example file and
fill in your own values:

```bash
cp .env.example .env
# edit .env
```

| Variable | Description |
|----------|-------------|
| `REDDIT_CLIENT_ID` | Reddit app client id |
| `REDDIT_CLIENT_SECRET` | Reddit app client secret |
| `REDDIT_USERNAME` | Reddit account username |
| `REDDIT_PASSWORD` | Reddit account password |
| `REDDIT_USER_AGENT` | Reddit user agent string (optional) |
| `USERNAME` | Instagram username |
| `PASS` | Instagram password |
| `PASTEBIN_API_KEY` | Pastebin API key (optional; only for the disabled paste feature) |

## Running

```bash
python main.py
```

`Procfile`, `runtime.txt`, and `okteto-pipeline.yml` are included for deploying
as a worker (Heroku-style / Okteto).

## License

[MIT](./LICENSE)
