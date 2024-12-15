import os

import requests

# URL del webhook
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_video_via_webhook(video_path):
    if WEBHOOK_URL is None:
        raise Exception("No discord webhook url detected")

    with open(video_path, "rb") as video_file:
        # Configura il payload della richiesta
        payload = {
            "content": "Ecco il tuo video!"
        }
        files = {
            "file": video_file  # Invia il video come file
        }
        # Invia la richiesta POST
        response = requests.post(WEBHOOK_URL, data=payload, files=files)

        # Controlla il risultato
        if response.status_code == 204:
            print("Video inviato con successo!")
        else:
            print(
                f"Errore nell'invio: {response.status_code} - {response.text}")
