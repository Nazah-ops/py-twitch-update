from uuid import uuid4

from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from integrations.pexel import Orientation, Pexel
from integrations.reddit import Reddit, Trend
from integrations.sound import Sound
from utils.globals import work_dir
from video_editor import VideoEditor


def make_reel():
    reddit = Reddit()
    reddit_image, title = reddit.get_image("TwoSentenceHorror", trend=Trend.TOP)
    
    sound = Sound()
    soundeffect = sound.download_sound("", "sinister")

    background = get_background_video()
    
    return compose(image=reddit_image, background_video=background, sound=soundeffect), title

def get_background_video():
    pexel = Pexel()
    pexel_video = pexel.get_video("dark", Orientation.PORTRAIT)
    editor = VideoEditor()
    
    edited = work_dir(f"{uuid4()}.mp4")
    
    # Carica il video
    clip = VideoFileClip(pexel_video)
    # Applica l'effetto VHS
    vhs_clip = editor.vhs_effect(clip)
    # Salva il risultato
    vhs_clip.write_videofile(edited)
    
    return edited

def compose(image, background_video, sound):
    
    result = work_dir(f"result.mp4")
    
    editor = VideoEditor()
    video_with_image = editor.image_to_center(
        video=background_video, image=image)
    final_video = editor.merge_audio_with_video(
        video_with_image, sound)


    ffmpeg_extract_subclip(final_video, 0, 10, targetname=result)

    return result
