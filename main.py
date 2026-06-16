from instagrapi import Client
import praw
from pathlib import Path
from prawcore.exceptions import Forbidden
import datetime
import threading
import requests
import yt_dlp
import asyncio
import random
import time
import json
import wget
import os
from PIL import Image, ImageDraw, ImageFont
 
#Creating Clients
cl = Client()
inti = str(random.randint(0, 999999))
hr = random.randint(4, 12)
count = random.randint(0, 10)
print("count is {}".format(count))



    

def download (url):
   global int
   ydl_opts_start = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', #This Method Need ffmpeg
            'outtmpl': f'{inti}.%(ext)s',
            'no_warnings': True,
            'ignoreerrors': True,
            'playlistend': 1,
            'http_chunk_size': 20097152,
            'writethumbnail': False
   }
   with yt_dlp.YoutubeDL(ydl_opts_start) as ydl:
      ydl.download([url])



def Auto():
  global count
  while True:

#English Subreddit
    subreddit = [
"AnimalsBeingDerps", "Dogelore","Indiandankmemes", "comedymemes", "wholesomememes", "funny",
"funnyvideos", "memes", "okbuddyretard",  'youtubehaiku',  "ComedyCemetery",  "mealtimevideos",  "Whatcouldgowrong",  "CatsMurderingToddlers",  "dankvideos", 
"funniestvideos", "notimanderic",  "wellthatsucks", "thathappened",  "atbge", "ProgrammerHumor",  "terriblefacebookmemes",  "im14andthisisdeep","IndianDankMemes"]


    test = ["funnyvideos", "funnyvideos"]

#Hindi_Subreddit
    
    hindi_only = [
   "Dogelore", "Dogelore", 
   "bakchodi", "chodi", "Hindimemes", "Mandirgang", 
   "Indiandankmemes", "dankinindia", "dankindianmemes",
   "dankmemes", "indiameme", "funnyvideos", "cringe", "facepalm",
    ]

    

#Random Tags
    hashtags = [ 
    "#meme", "#memes", "#funny", "#dankmemes",
    "#memesdaily", "#funnymemes", "#lol", "#humor",
    "#follow", "#dank", "#love", "#like", "#memepage",
    "#comedy", "#instagram", "#dankmeme", "#lmao", "#dailymemes", "#fun",
    "#edgymemes", "#ol", "#offensivememes", "#memestagram", "#funnymeme", "#bhfyp", "#instagood", "#memer", "#bhfyp",
    "#doge", "#dogememe", "#doge", "#dogememes",
    "#cheems", "#dogecoin", "#dankmemes", "#cheemsmeme",
    "#funny", "#dogelore", "#funnymemes", "#doggo", "#doggomeme", "#cheemsmemes", "#explore"]
    random.shuffle(hashtags)
    random.shuffle(hashtags)
    random.shuffle(hashtags)
    hash1 = random.choice(hashtags)
    hash2 = random.choice(hashtags)
    hash3 = random.choice(hashtags)
    hash4 = random.choice(hashtags)
    hash5 = random.choice(hashtags)

    user = os.environ.get("USERNAME")
    password = os.environ.get("PASS")
    random.shuffle(subreddit)    
    random.shuffle(subreddit)
    random.shuffle(subreddit)
    random.shuffle(subreddit)
    subreddit1 = random.choice(subreddit)      
    print(f"choosing {subreddit1}")
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        user_agent=os.environ.get("REDDIT_USER_AGENT", "instaddit"),
        username=os.environ.get("REDDIT_USERNAME"),
        password=os.environ.get("REDDIT_PASSWORD"),
    )
    subreddit = reddit.subreddit(subreddit1)
    try:
      memes = subreddit.random() 
    except Forbidden:
      Auto()
    try:
     title1 = memes.title
    except:
     Auto()
    url = (memes.url)
    r = requests.get(url, headers={'User-Agent':'18277'})
    video_url = r.url
    print(url)   
    pics = [".png", ".jpg", ".jpeg"]
    videos = ["https://v.redd.it", "v.redd.it", "youtube", "youtu.be"]
    data = f"""
This post was scrapped from r/{subreddit1}

Post Link: https://reddit.com{memes.permalink}
Credits go to: {memes.author} for posting the post.

The url of the post is {memes.url}.
Title is {memes.title}.
Post resent at {datetime.datetime.now()}.
I do not own any content. 
Please contact me if you want any content to get removed.


Mr. Meme"""

    data = {
    'api_dev_key': os.environ.get("PASTEBIN_API_KEY", ""),
    'api_paste_code': data,
    'api_option': 'paste',
    'api_paste_expire_date': 'N'
    }
    #response = requests.post('https://pastebin.com/api/api_post.php', data=data)
    #neko = (response.content).decode("utf-8")
    if any(pic in url for pic in pics):
         file = wget.download(url)
         print('downloaded')
         title = (f"{title1}\n{hash1} {hash2} {hash3} {hash4} {hash5}")
         image = Image.open(file).convert('RGB')
         color = (255, 255, 255)
         draw = ImageDraw.Draw(image)
         width, height = image.size
         text = "@whyknotmemes"
         font = ImageFont.truetype('font.ttf', 25)
         draw.text((0,0), text=text, font=font, fill=color)  
         time.sleep(20) 
         cl.login(user, password)        
         try:
           image.save("picture.jpg")           
           phot_path = "picture.jpg"
           phot_path = Path(phot_path)        
           media = cl.photo_upload(
                    phot_path,
                    (f"{title1}\n{hash1} {hash2} {hash3} {hash4} {hash5}"),
           )
           os.remove(phot_path)
         except Exception as e:
           Auto()
           
    elif any(video in url for video in videos):
          print("video")
          file = download(url=url)       
         
          try:       
           time.sleep(20)          
           cl.login(user, password)
           print("Power nap OVER!")
  
           try:
             media = cl.clip_upload(
                          path = f"{inti}.mp4", 
                        
                          caption = (f"{title1}\n{hash1} {hash2} {hash3} {hash4} {hash5}"),
             )
             print("Uploaded as reel")
             
           except Exception as e:
             print(e)


             try:
               media = cl.video_upload(
                          path = f"{inti}.mp4", 
                          
                          caption = (f"{title1}\n{hash1} {hash2} {hash3} {hash4} {hash5}")
               ) 
               print("Uploaded as video")
             except Exception as e:
               try: 
                media = cl.igtv_upload(
                          path = f"{inti}.mp4", 
                          
                          title=title1,
                          caption = (f"{title1}\n{hash1} {hash2} {hash3} {hash4} {hash5}")
                ) 
                print("Uploaded as igtv")
               except Exception as e:
                print(e)
          except Exception as e:
             print(e)  
             Auto()
          try:
            os.remove(f"{inti}.mp4") 
            
            print("uploaded")
          except Exception as e:
            print(e)
            Auto()
    else:
      print(f"Unknown post {url}")
      Auto()
    
    
    
    if count != 0:
     print("uploading story too")
     story_list = ["funnyvideos", "funnyvideos", "funnyvideos", "funnyvideos", "funnyvideos", "funnyvideos", "funnyvideos", "funnyvideos", "funnyvideos", "tiktokcringe", "tiktokcringe", "tiktokcringe", "PlayItAgainSam"
"dankvideos",
"funniestvideos"]
     story = random.choice(story_list)
     subreddit = reddit.subreddit(story)
     memes = subreddit.random() 
     title = memes.title
     url = (memes.url)
     r = requests.get(url, headers={'User-Agent':'18277'})
     video_url = r.url
     maki = str(random.randint(0, 999999))
     ydl_opts_start = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', #This Method Need ffmpeg
            'outtmpl': f'{maki}.%(ext)s',
            'no_warnings': True,
            'ignoreerrors': True,
            'playlistend': 1,
            'http_chunk_size': 20097152,
            'writethumbnail': False
     }
     with yt_dlp.YoutubeDL(ydl_opts_start) as ydl:
      ydl.download([url])
     
     cl.video_upload_to_story(path = f"{maki}.mp4", caption = title)
     print("new story")
     os.remove(f"{maki}.mp4") 
    else:
     print(f"Number was {count}")
     print("Skipping")
     pass

        
       
    
       
           
    
    
    
      
    
    cl.logout()
    print("Logged out!")
    print(f"sleeping {hr} hours")
    time.sleep(3600*hr)



if __name__ == "__main__":
   
   Auto()

else: 
   print("file not runned")
   os._exit(os.EX_OK) 
   
