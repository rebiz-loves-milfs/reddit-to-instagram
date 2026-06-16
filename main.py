import datetime
import logging
import os
import random
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from instagrapi import Client
import praw
from prawcore.exceptions import Forbidden
import requests
import wget
import yt_dlp

# Set up clean logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

SUBREDDITS = [
    "AnimalsBeingDerps", "Dogelore", "Indiandankmemes", "comedymemes", "wholesomememes", "funny",
    "funnyvideos", "memes", "okbuddyretard", "youtubehaiku", "ComedyCemetery", "mealtimevideos",
    "Whatcouldgowrong", "CatsMurderingToddlers", "dankvideos", "funniestvideos", "notimanderic",
    "wellthatsucks", "thathappened", "atbge", "ProgrammerHumor", "terriblefacebookmemes",
    "im14andthisisdeep", "IndianDankMemes"
]

HASHTAGS = [
    "#meme", "#memes", "#funny", "#dankmemes", "#memesdaily", "#funnymemes", "#lol", "#humor",
    "#follow", "#dank", "#love", "#like", "#memepage", "#comedy", "#instagram", "#dankmeme",
    "#lmao", "#dailymemes", "#fun", "#edgymemes", "#ol", "#offensivememes", "#memestagram",
    "#funnymeme", "#bhfyp", "#instagood", "#memer", "#doge", "#dogememe", "#dogememes",
    "#cheems", "#dogecoin", "#cheemsmeme", "#dogelore", "#doggo", "#doggomeme", "#cheemsmemes",
    "#explore"
]

STORY_SUBREDDITS = [
    "funnyvideos", "tiktokcringe", "PlayItAgainSam", "dankvideos", "funniestvideos"
]

def download_video(url, output_name):
    """Downloads a video using yt-dlp."""
    logger.info(f"Downloading video from {url}...")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_name}.%(ext)s',
        'no_warnings': True,
        'ignoreerrors': True,
        'playlistend': 1,
        'http_chunk_size': 20097152,
        'writethumbnail': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def add_watermark(image_path, text="@whyknotmemes", font_path="font.ttf"):
    """Adds a simple watermark to the image at (0, 0)."""
    try:
        with Image.open(image_path).convert('RGB') as img:
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype(font_path, 25)
            except IOError:
                font = ImageFont.load_default()
            draw.text((10, 10), text=text, font=font, fill=(255, 255, 255))
            watermarked_path = "picture.jpg"
            img.save(watermarked_path)
            return watermarked_path
    except Exception as e:
        logger.error(f"Error watermarking image: {e}")
        return None

def run_bot_cycle():
    """Runs a single iteration of the bot (fetch, process, upload, sleep)."""
    # Pick a random subreddit
    sub_name = random.choice(SUBREDDITS)
    logger.info(f"Selected subreddit: r/{sub_name}")

    # Generate hashtags
    selected_tags = random.sample(HASHTAGS, min(5, len(HASHTAGS)))
    tags_str = " ".join(selected_tags)

    # Load Instagram credentials
    ig_user = os.environ.get("USERNAME")
    ig_pass = os.environ.get("PASS")
    if not ig_user or not ig_pass:
        logger.error("Instagram credentials (USERNAME, PASS) are missing!")
        return

    # Initialize Reddit client
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent=os.environ.get("REDDIT_USER_AGENT", "instaddit"),
        username=os.environ.get("REDDIT_USERNAME"),
        password=os.environ.get("REDDIT_PASSWORD"),
    )

    try:
        subreddit_obj = reddit.subreddit(sub_name)
        memes = subreddit_obj.random()
        if not memes or not hasattr(memes, "title") or not hasattr(memes, "url"):
            logger.warning("Failed to fetch a random post (got None or missing properties).")
            return
    except Forbidden:
        logger.warning(f"Access forbidden to r/{sub_name}")
        return
    except Exception as e:
        logger.error(f"Error fetching from Reddit: {e}")
        return

    title = memes.title
    url = memes.url
    logger.info(f"Fetched post: '{title}' - URL: {url}")

    # Validate post URL via redirect check
    try:
        r = requests.get(url, headers={'User-Agent': '18277'}, timeout=15)
        media_url = r.url
    except Exception as e:
        logger.error(f"Error checking URL {url}: {e}")
        return

    pics_extensions = (".png", ".jpg", ".jpeg")
    videos_keywords = ("v.redd.it", "youtube.com", "youtu.be")

    cl = Client()
    temp_files = []

    try:
        is_pic = any(ext in media_url.lower() for ext in pics_extensions)
        is_vid = any(vid in media_url.lower() for vid in videos_keywords)

        if is_pic:
            logger.info("Processing as image...")
            downloaded_file = wget.download(media_url)
            temp_files.append(downloaded_file)
            
            watermarked_file = add_watermark(downloaded_file)
            if not watermarked_file:
                return
            temp_files.append(watermarked_file)

            logger.info("Logging into Instagram...")
            cl.login(ig_user, ig_pass)
            caption = f"{title}\n{tags_str}"
            cl.photo_upload(Path(watermarked_file), caption)
            logger.info("Successfully uploaded photo.")

        elif is_vid:
            logger.info("Processing as video...")
            video_id = str(random.randint(0, 999999))
            download_video(media_url, video_id)
            video_path = f"{video_id}.mp4"
            temp_files.append(video_path)

            if not os.path.exists(video_path):
                logger.warning("Video download failed / file not found.")
                return

            logger.info("Logging into Instagram...")
            cl.login(ig_user, ig_pass)
            caption = f"{title}\n{tags_str}"
            
            # Try upload strategies
            uploaded = False
            for upload_method, name in [
                (lambda: cl.clip_upload(Path(video_path), caption), "Reel"),
                (lambda: cl.video_upload(Path(video_path), caption), "Video"),
                (lambda: cl.igtv_upload(Path(video_path), title=title, caption=caption), "IGTV")
            ]:
                try:
                    logger.info(f"Attempting to upload as {name}...")
                    upload_method()
                    logger.info(f"Successfully uploaded as {name}.")
                    uploaded = True
                    break
                except Exception as upload_err:
                    logger.error(f"Upload as {name} failed: {upload_err}")
            
            if not uploaded:
                logger.error("All video upload strategies failed.")

        else:
            logger.warning(f"Unknown/unsupported URL: {media_url}")
            return

        # Upload story if count is non-zero
        story_count = random.randint(0, 10)
        if story_count != 0:
            logger.info("Uploading random story...")
            story_sub = random.choice(STORY_SUBREDDITS)
            try:
                story_subreddit = reddit.subreddit(story_sub)
                story_post = story_subreddit.random()
                if story_post and hasattr(story_post, "url") and hasattr(story_post, "title"):
                    story_id = str(random.randint(0, 999999))
                    download_video(story_post.url, story_id)
                    story_path = f"{story_id}.mp4"
                    temp_files.append(story_path)
                    
                    if os.path.exists(story_path):
                        cl.video_upload_to_story(Path(story_path), caption=story_post.title)
                        logger.info("Successfully uploaded story.")
            except Exception as story_err:
                logger.error(f"Failed to fetch/upload story: {story_err}")

    except Exception as e:
        logger.error(f"Cycle execution error: {e}")
    finally:
        # Log out of Instagram safely
        try:
            cl.logout()
            logger.info("Logged out of Instagram.")
        except Exception:
            pass

        # Clean up temporary files
        for f in temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
                    logger.info(f"Cleaned up temporary file: {f}")
            except Exception as clean_err:
                logger.error(f"Failed to remove file {f}: {clean_err}")

def main():
    logger.info("Starting instaddit bot...")
    while True:
        try:
            run_bot_cycle()
        except Exception as e:
            logger.error(f"Unhandled exception in main loop: {e}")
        
        sleep_hours = random.randint(4, 12)
        logger.info(f"Sleeping for {sleep_hours} hours...")
        time.sleep(3600 * sleep_hours)

if __name__ == "__main__":
    main()
