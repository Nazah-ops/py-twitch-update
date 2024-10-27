import os

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
    def add_intro_to_video(original_video: str, overlay_video: str):
        video_clip = VideoFileClip((original_video), target_resolution=(1080, 1920))  # b .mp4 file
        overlay_clip = VideoFileClip((overlay_video), has_mask=True, target_resolution=(1080, 1920))  # .mov file with alpha channel

        final_video = CompositeVideoClip([video_clip, overlay_clip])

        final_video.write_videofile(
            os.environ.get("OUTPUT"),
            threads=6,
        )
