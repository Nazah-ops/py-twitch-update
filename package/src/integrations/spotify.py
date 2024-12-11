import os
from dataclasses import asdict, dataclass
from typing import List, Optional
from uuid import uuid4

import librosa
import numpy as np
from pydub import AudioSegment
from pymongo import MongoClient
from spotdl.download.downloader import Downloader
from spotdl.types.playlist import Playlist
from spotdl.types.song import Song
from spotdl.utils.spotify import SpotifyClient

from utils.globals import work_dir
from utils.mongo import get_mongo_client, get_unused_id_dict


@dataclass
class SongMetaData:
    name: str
    artists: List[str]
    artist: str
    genres: List[str]
    disc_number: int
    disc_count: int
    album_name: str
    album_artist: str
    duration: int
    year: int
    date: str
    track_number: int
    tracks_count: int
    song_id: str
    explicit: bool
    publisher: str
    url: str
    isrc: str
    cover_url: str
    copyright_text: str
    download_url: Optional[str]
    lyrics: Optional[str]
    popularity: int
    album_id: str
    list_name: Optional[str]
    list_url: Optional[str]
    list_position: Optional[int]
    list_length: Optional[int]
    artist_id: str
    album_type: str

@dataclass
class SpotifyData:
    urls: List[str]
    songs: List[Song]

class SpotifyClientHandler:
    
    def __init__(self):
        SpotifyClient.init(
            client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
            client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET') ,
            user_auth=False
        )

    # Funzione per scaricare un brano
    def download_song(self, spotify_url):
        # Configura il downloader
        config = {
            "output": work_dir(""),  # Nome del file di output
            "ytm_search": True,                  # Usa YouTube Music per il download
            "log_level": "INFO",                 # Livello di log
            "ffmpeg": None                       # Assicurati che FFmpeg sia installato e nel PATH
        }
        downloader = Downloader(config)
        # Crea un oggetto Song dal link Spotify
        song = Song.from_url(spotify_url)

        # Scarica la canzone
        audio, path = downloader.download_song(song)
        return str(path.absolute())

    def segment_music_drop(self, audio_path, destination):
        sec_before = 10
        sec_after = 5
        
        y, sr = librosa.load(audio_path, sr=None)

        # Calcola l'energia RMS
        frame_length = 2048
        hop_length = 512
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

        # Trova il punto con l'energia più alta (potenziale drop)
        max_rms_frame = np.argmax(rms)
        max_rms_time = librosa.frames_to_time(max_rms_frame, sr=sr, hop_length=hop_length)

        # Definisci l'intervallo di estrazione (es. 5 secondi prima e dopo il drop)
        start_time = max(0, max_rms_time - sec_before)  # 5 secondi prima del drop
        end_time = min(librosa.get_duration(y=y, sr=sr), max_rms_time + sec_after)  # 5 secondi dopo il drop

        # Carica l'intero file con pydub per l'esportazione
        audio_path = AudioSegment.from_file(audio_path)

        # Estrai il segmento (converti il tempo da secondi a millisecondi)
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)
        segment = audio_path[start_ms:end_ms]

        segment.export(destination, format="mp3")


    def get_song_for_reel(self):
        # URL della playlist da cui recuperare le canzoni
        mongoClient: MongoClient = get_mongo_client()["db"]["source"]
        url = mongoClient.find_one({"source": "spotify"})["playlist_link"]
        playlist = Playlist.from_url(url)
        
        sorted_songs: List[SongMetaData] = sorted(playlist.songs, key=lambda song: song.popularity, reverse=True)
        
        # Seleziona una canzone non ancora utilizzata
        # La funzione get_unused_id verifica che la canzone non sia già stata utilizzata
        song_url: str = get_unused_id_dict({"source" : "spotify", "query": url}, [asdict(song) for song in sorted_songs], 'url')["url"]
        path = self.download_song(song_url)
        
        final_path = work_dir(f"{uuid4()}.mp3")
        self.segment_music_drop(audio_path=path, destination=final_path)
        return final_path
