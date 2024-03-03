from moviepy.editor import *


class Movie:
    
    def __init__(self, transition_time: int) -> None:
        self.transition_time = transition_time
        
    def fade_all_video(self, clips: [str]):
        video_clips = [VideoFileClip("/app/files/clips/" + clips.pop(0))]
        
        for clip in clips:
            video_clips.append(VideoFileClip("/app/files/clips/" + clip).crossfadein(self.transition_time))

        final = concatenate_videoclips(video_clips, padding=-self.transition_time, method="compose")
        final.write_videofile("files/clips/final_output.mp4")

    @staticmethod
    def overlay_video(original_video: str, overlay_video: str):
        output_path = "/app/files/output.mp4"

        video_clip = VideoFileClip((original_video), target_resolution=(1080, 1920)) #b .mp4 file

        overlay_clip = VideoFileClip((overlay_video), has_mask=True, target_resolution=(1080, 1920)) #.mov file with alpha channel

        final_video = CompositeVideoClip([video_clip, overlay_clip])  

        final_video.write_videofile(
            output_path,
            threads = 6,
        )