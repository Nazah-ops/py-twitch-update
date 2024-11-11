import os
from uuid import uuid4

import numpy as np
import PIL
from moviepy.editor import *
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import lum_contrast
from moviepy.video.tools.drawing import color_split

from utils.globals import work_dir


class VideoEditor:

    def __init__(self):
        pass

    def concat_fade(self, clips, transition_time):
        file_dir = work_dir("final_output.mp4")
        video_clips = [VideoFileClip(clips.pop(0))]

        for clip in clips:
            video_clips.append(VideoFileClip(
                clip).crossfadein(transition_time))

        video_faded = concatenate_videoclips(
            video_clips, padding=-transition_time, method="compose")
        video_faded.write_videofile(file_dir)
        return file_dir

    @staticmethod
    def intro_to_video(original_video: str, overlay_video: str):
        video_clip = VideoFileClip(
            (original_video), target_resolution=(1080, 1920))  # b .mp4 file
        overlay_clip = VideoFileClip((overlay_video), has_mask=True, target_resolution=(
            1080, 1920))  # .mov file with alpha channel

        final_video = CompositeVideoClip([video_clip, overlay_clip])

        final_video.write_videofile(
            os.environ.get("OUTPUT"),
            threads=6,
        )

    def image_to_center(self, video, image):
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
        videoFile = VideoFileClip(video)
        image = ImageClip(image).set_start(0).set_duration(videoFile.duration).set_pos(
            ("center", "center")).resize(height=videoFile.h * .26)

        target_dir = work_dir(f"{uuid4()}.mp4")
        videoclip_with_image = CompositeVideoClip([videoFile, image])
        videoclip_with_image.write_videofile(target_dir)
        return target_dir

    def merge_audio_with_video(self, video, audio):
        videoclip_without_audio = work_dir(f"{uuid4()}.mp4")

        # Togli l'audio esistente
        videoclip = VideoFileClip(video)
        new_clip = videoclip.without_audio()
        new_clip.write_videofile(videoclip_without_audio)

        target_dir = work_dir(f"{uuid4()}.mp4")

        # Aggiungi l'audio nuovo
        output_videoclip = VideoFileClip(videoclip_without_audio)
        audioclip = AudioFileClip(audio)
        new_audioclip = CompositeAudioClip([audioclip])

        output_videoclip.audio = new_audioclip
        output_videoclip.write_videofile(target_dir)
        return target_dir


    def vhs_effect(self, clip):
        # Aggiunge un effetto di rumore
        noise = (np.random.normal(size=(clip.h, clip.w, 3)) * 20).astype('uint8')
        noise_clip = clip.fl_image(lambda frame: np.clip(frame + noise, 0, 255).astype('uint8'))
        
        # Luminosità e contrasto per dare il look da VHS
        contrast_clip = lum_contrast(noise_clip, lum=60, contrast=80)

        # Separazione RGB manuale per creare un effetto di offset
        def rgb_split(image):
            # Separazione dei canali
            r = np.roll(image[:, :, 0], 1, axis=1)
            g = np.roll(image[:, :, 1], -1, axis=0)
            b = image[:, :, 2]
            # Ricombinazione dei canali con piccoli offset
            return np.stack([r, g, b], axis=2)
        
        # Applica l'offset RGB a ogni frame
        rgb_clip = contrast_clip.fl_image(rgb_split)
        
        return rgb_clip

