import requests
import os
import json
import datetime
import subprocess
import logging as logger

from os.path import join, dirname
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from moviepy.editor import *


#Loading environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logger.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def dump_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_twitch_token():
    payload = {
        'client_id' : os.environ.get("CLIENT_ID"),
        'client_secret': os.environ.get("CLIENT_SECRET"),
        'grant_type': 'client_credentials'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post("https://id.twitch.tv/oauth2/token", headers=headers, data=payload)

    return json.loads(response.text)["access_token"]


token = get_twitch_token()
headers = {'Authorization': f'Bearer {token}', 'Client-Id': os.environ.get("CLIENT_ID")}


def get_streamers():
    '''
    Retreive from a third party website the list of the most watched streamers
    Returns a list of strings
    '''
    results = []
    request = requests.get('https://www.twitchmetrics.net/channels/viewership?game=League+of+Legends&lang=en&page=1')
    parsed_html = BeautifulSoup(request.text)

    for name in parsed_html.body.find_all('h5', attrs={'class':'mr-2 mb-0'}):
        results.append(name.get_text())
    
    return results


def convert_name_to_id(name):
    '''
        Converts the basic name (e.g. Thebausffs) to the broadcaster id, which twitch uses to identify the streamer
        There are some exceptions with names, that involve whitespaces between them: only staff members can use them, and when putting
        the name in the endpoint will result in a error, so the name has to be stripped of it
    '''
    params = { "login" : "".join(name.split()) }
    request = requests.get(f'https://api.twitch.tv/helix/users', headers=headers, params=params)
    if request.ok:
        return json.loads(request.text)["data"][0]["id"]
    else:
        raise Exception(f'Error from twitch endpoint {request.text}')

def clips_from_broadcaster_id(id):
    '''Retreives the clips from a streamer, based also on timeframe, and sorted by views'''
    format_time = "%Y-%m-%dT%H:%M:%SZ"
    params = {
        "broadcaster_id" : id,
        "started_at" : (datetime.datetime.now() - datetime.timedelta(days=3)).strftime(format_time),
        "ended_at" : datetime.datetime.now().strftime(format_time)
    }
    request = requests.get(f'https://api.twitch.tv/helix/clips', headers=headers, params=params)
    return json.loads(request.text)["data"]

def download_clip(clip):
    path = f'files/clips/{clip["title"]}.mp4'
    index = clip["thumbnail_url"].find('-preview')
    clip_url = clip["thumbnail_url"][:index] + '.mp4'
    r = requests.get(clip_url)

    if r.headers['Content-Type'] == 'binary/octet-stream':
        if not os.path.exists('files/clips'): os.makedirs('files/clips')
        with open(path, 'wb') as f:
            f.write(r.content)
        return path
    else:
        print(f'Failed to download clip from thumb: {clip["thumbnail_url"]}')

def overlay_video(original_video, overlay_video):
    output_path="output.mp4"

    video_clip = VideoFileClip((original_video), target_resolution=(1080, 1920)) #b .mp4 file

    overlay_clip = VideoFileClip((overlay_video), has_mask=True, target_resolution=(1080, 1920)) #.mov file with alpha channel

    final_video = CompositeVideoClip([video_clip, overlay_clip])  


    final_video.write_videofile(
        output_path,
        threads = 6,
    )


def main():
    logger.info('Program started')
    logger.info('BRUH')

    time = 2 * 60
    video_time = 0

    clips = []

    streamers = get_streamers()

    for streamer in streamers:
        if streamer == "Riot Games":
            continue
        streamer_id = convert_name_to_id(streamer)
        clips_downloaded = clips_from_broadcaster_id(streamer_id)[:3]
        if video_time > time:
            break
        for clip in clips_downloaded:
            video_time += float(clip["duration"])
            clips.append(download_clip(clip))
    
    transition_time = 2
    video_clips = [VideoFileClip(clips.pop(0))]
    
    for clip in clips:
        video_clips.append(VideoFileClip(clip).crossfadein(transition_time))

    final = concatenate_videoclips(video_clips, padding=-transition_time, method="compose")
    final.write_videofile("files/clips/final_output.mp4")
    #Adding intro
    overlay_video("files/clips/final_output.mp4", "files/intro.mov")


main()
#combine_videos_with_transition(["files/clips/1.mp4", "files/clips/2.mp4", "files/clips/1.mp4"])

# clip1 = VideoFileClip("files/clips/1.mp4")
# clip2 = VideoFileClip("files/clips/2.mp4")
# final = concatenate_videoclips([clip1, clip2])
# final.write_videofile("files/clips/merged.mp4")

# overlay_intro("files/clips/1.mp4")

# overlap = 3
# final_clip = CompositeVideoClip([
#     clip1.crossfadeout(overlap),
#     clip2.set_start(clip1.duration - overlap).crossfadein(overlap)
# ])

# final_clip.write_videofile("files/clips/faded.mp4")