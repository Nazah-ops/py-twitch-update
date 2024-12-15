import logging as logger
from uuid import uuid4

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from integrations.discord import send_video_via_webhook
from integrations.pexel import Orientation, get_video
from integrations.reddit import Trend, get_post
from integrations.spotify import SpotifyClientHandler
from utils.video_editor import VideoEditor


def generate_short_format_video():
    #Prende da reddit un screen di un post, restituisce il path e il titolo
    reddit_image, title = get_post("TwoSentenceHorror", trend=Trend.TOP)
    
    logger.info("Reddit post title: %s", title)
    
    #Inizializzazione del client di spoty ed esegue il fetch di una canzone di una data playlist (indicata su mongo), restituisce il path
    spotyHandler = SpotifyClientHandler()
    soundeffect = spotyHandler.get_song_for_reel()

    #Scarica un video dal sito PEXEL, con tema dato in input, restituisce il path
    video = get_video("dark", Orientation.PORTRAIT)
    
    #Aggrega tutti gli elementi e crea il video finale, e ritorna al main il path, titolo e i tag TODO: tag dinamici
    return compose(image=reddit_image, background_video=video, sound=soundeffect), title


def compose(image: str, background_video: str, sound: str):
    
    editor = VideoEditor()
    
    #Mette l'immagine al centro del video
    video_with_image = editor.image_to_center(video=background_video, image=image)
    
    #Muta l'audio
    video_without_audio = editor.mute_audio(video_with_image)
    
    #Manda il video senza audio su discord
    send_video_via_webhook(video_without_audio)
    
    #Compone insieme il video e la canzone
    final_video = editor.merge_audio_with_video(video_without_audio, sound)

    #Taglia il video e tiene i 15 secondi
    #ffmpeg_extract_subclip(final_video, 0, 15, targetname=result)

    logger.info("Video finale: %s", final_video)

    return final_video
    return final_video
