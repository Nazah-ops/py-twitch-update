from uuid import uuid4

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from integrations.pexel import Orientation, Pexel
from integrations.reddit import Trend, get_post
from integrations.spotify import SpotifyClientHandler
from utils.globals import work_dir
from video_editor import VideoEditor


def make_reel():
    reddit_image, title = get_post("TwoSentenceHorror", trend=Trend.TOP)
    
    spotyHandler = SpotifyClientHandler()
    soundeffect = spotyHandler.get_song_for_reel()

    background = get_background_video()
    
    return compose(image=reddit_image, background_video=background, sound=soundeffect), title

def get_background_video():
    pexel = Pexel()
    pexel_video = pexel.get_video("dark", Orientation.PORTRAIT)
    
    return pexel_video

def compose(image, background_video, sound):
    
    result = work_dir(f"result.mp4")
    
    editor = VideoEditor()
    video_with_image = editor.image_to_center(video=background_video, image=image)
    final_video = editor.merge_audio_with_video(video_with_image, sound)

    ffmpeg_extract_subclip(final_video, 0, 15, targetname=result)

    return result
