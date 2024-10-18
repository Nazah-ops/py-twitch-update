import google_auth_oauthlib
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class YoutubeAPI:

    def __init__(self) -> None:
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.category_id = "22"  # Category ID (22 is for 'People & Blogs')
        self.privacy_status = "public"  # Options: "public", "private", "unlisted"

        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', self.SCOPES)

        credentials = flow.run_local_server(port=0)
        self.youtube_api = build('youtube', 'v3', credentials=credentials)

        return

    def upload_video(self, video_file, title, description):
        # Create a request to upload the video
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": self.category_id
            },
            "status": {
                "privacyStatus": self.privacy_status
            }
        }
        media_body = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        request = self.youtube_api.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media_body)

        # Execute the request
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        return response

    def upload_thumbnail(self, video_id, file_path):
        request = self.youtube_api.thumbnails().set(
            videoId=video_id,
            media_body=file_path
        )
        response = request.execute()
        print('Thumbnail uploaded successfully:', response)

    def upload(self, video_file, title, description, thumbnail_file):
        try:
            upload_response = self.upload_video(video_file, title, description)
            self.upload_thumbnail(upload_response['id'], thumbnail_file)
            return True
        except Exception as e:
            print(f"Video non caricato: {e}")
            return False
