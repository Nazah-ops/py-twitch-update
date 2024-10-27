import http.client
import json
import urllib.parse
import uuid
from enum import Enum


class ORIENTATION(Enum):
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    SQUARE = "square"

class Pexel:
    def __init__(self):
        pass

    def get_video(self, topic,  orientation: ORIENTATION):
        url = self.get_video_query(topic,  orientation)[0]["video_files"][0]["link"]
        # Parsing dell'URL per ottenere il dominio e il percorso
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path

        # Connessione al server
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", path)

        # Risposta del server
        response = conn.getresponse()

        # Verifica che la richiesta sia andata a buon fine
        if response.status != 200:
            raise Exception("Errore durante download del video pexel (background): ", response.status, response.reason)
        
        video_name = f"{uuid.uuid4().hex[:6].upper()}.mp4"
        
        with open(video_name, "wb") as file:
            # Leggi i dati in blocchi per evitare di sovraccaricare la memoria
            while True:
                data = response.read(8192)
                if not data:
                    break
                file.write(data)
        print("Video scaricato con successo!")
        # Chiudi la connessione
        conn.close()
        return video_name

    def get_video_query(self, topic,  orientation: ORIENTATION):
        conn = http.client.HTTPSConnection("api.pexels.com")
        headers = {
            'Authorization': 'yL7ewVOVKa8nh1pR7koTTlntKO1IkNvWMoQRP4I0ANfFr0ev1F0mIAjo',
        }
        conn.request("GET", f"/videos/search?query={topic}&per_page=5&orientation={orientation}", {}, headers)
        data = conn.getresponse().read().decode("utf-8")
        return json.loads(data)["videos"]
                        
