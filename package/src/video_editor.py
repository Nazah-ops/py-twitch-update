import os
import uuid

import PIL
from moviepy.editor import *


class VideoEditor:

    def __init__(self):
        pass

    def concat_fade(self, clips, transition_time):
        path_to_file = os.environ.get("BASE_PATH") + "/files/clips/final_output.mp4"
        video_clips = [VideoFileClip(clips.pop(0))]

        for clip in clips:
            video_clips.append(VideoFileClip(clip).crossfadein(transition_time))

        video_faded = concatenate_videoclips(video_clips, padding=-transition_time, method="compose")
        video_faded.write_videofile(os.environ.get("BASE_PATH") + "/files/clips/final_output.mp4")
        return path_to_file

    @staticmethod
    def intro_to_video(original_video: str, overlay_video: str):
        video_clip = VideoFileClip((original_video), target_resolution=(1080, 1920))  # b .mp4 file
        overlay_clip = VideoFileClip((overlay_video), has_mask=True, target_resolution=(1080, 1920))  # .mov file with alpha channel

        final_video = CompositeVideoClip([video_clip, overlay_clip])

        final_video.write_videofile(
            os.environ.get("OUTPUT"),
            threads=6,
        )

    def image_to_center(self, video, image):
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
        videoFile = VideoFileClip(video)

        title = ImageClip(image).set_start(0).set_duration(videoFile.duration).set_pos(("center","center")).resize(height=200)

        final = CompositeVideoClip([videoFile, title])
        final.write_videofile(f"/app/files/{uuid.uuid4().hex[:6].upper()}.mp4")
